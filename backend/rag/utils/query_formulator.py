import os
import re
from dotenv import load_dotenv
from langchain_ollama.llms import OllamaLLM
from enum import Enum

load_dotenv()
OLLAMA_BASE_URL = os.getenv("VITE_OLLAMA_BASE_URL")
FORMULATOR_MODEL = os.getenv(
    "FORMULATOR_MODEL", "mistral:7b"
)  # Default to a smaller model

# Define query status types
class QueryStatus(Enum):
    VALID = "valid"              # Query is valid and can proceed
    NEEDS_REFORMULATION = "reformulation"  # Query needs better wording but is on-topic
    NEEDS_CORRECTION = "correction"      # Query has incorrect standard reference
    NON_RELEVANT = "non_relevant"      # Query is off-topic
    TOO_SHORT = "too_short"          # Query is too short to process

# Standards scope for validation
SUPPORTED_STANDARDS = [
    "IEC 61557-12",
    "IEC 60688",
    "IEC 61850",
    "IEC 60051",
    "IEC 61869",
    "IEC 62053",
    "EN50470",
    "IEC 61810",
]


def formulate_query(query_text: str):
    """
    Checks if a query is well-formed and relevant to supported standards.
    Returns a tuple of (status, result) where:
    - status: QueryStatus enum indicating query validity type
    - result: Either the original query (if valid) or a suggestion/explanation.
    """
    # Skip processing for very short queries
    if len(query_text.strip()) < 3:
        return QueryStatus.TOO_SHORT, "Votre requête est trop courte. Veuillez fournir plus de détails."

    # Create a prompt for the formulator model
    prompt = f"""Évaluez la pertinence et la clarté de la requête utilisateur : "{query_text}"
    CONCERNE : Normes électriques.
    NORMES_SUPPORTÉES : {', '.join(SUPPORTED_STANDARDS)}.
    TERMES_TECHNIQUES_COURANTS (exemples) : "Logical Nodes", "GOOSE", "SCL", "IED" (souvent IEC 61850); "PMD" (IEC 61557-12); "transducteur" (IEC 60688).
    
    Répondez UNIQUEMENT avec l'un des formats suivants. Soyez concis. AUCUNE explication supplémentaire.
    
    1.  `VALIDE : {query_text}`
        -   Si la requête est claire, directement exploitable ET concerne une NORME_SUPPORTÉE (explicitement ou via TERMES_TECHNIQUES_COURANTS). Ceci inclut les requêtes longues et détaillées si elles sont pertinentes.
        -   Exemple (requête claire et pertinente): "Parlez-moi de la norme IEC 61850" -> `VALIDE : Parlez-moi de la norme IEC 61850`
        -   Exemple (requête longue et pertinente): "Pour les attributs de qualité selon la norme IEC 61850, proposez un tableau..." -> `VALIDE : Pour les attributs de qualité selon la norme IEC 61850, proposez un tableau...`
    
    2.  `SUGGESTION_REFORMULATION : [suggestion pour clarifier/préciser]`
        -   Si la requête concerne une NORME_SUPPORTÉE (ou ses termes) MAIS est vague, imprécise, ou pourrait être mieux formulée.
        -   Exemple (norme vague): "IEC 61850 ?" -> `SUGGESTION_REFORMULATION : Quelles informations spécifiques recherchez-vous concernant IEC 61850 ?`
        -   Exemple (terme technique seul): "Infos sur GOOSE" -> `SUGGESTION_REFORMULATION : Votre question sur "GOOSE" semble se rapporter à IEC 61850. Pouvez-vous confirmer ou préciser ?`
        -   Exemple (besoin de clarification): "Tu peux m'expliquer comme fonctionne la 60688" -> `SUGGESTION_REFORMULATION : Pouvez-vous préciser quels aspects du fonctionnement de la norme IEC 60688 vous intéressent ?`
    
    3.  `SUGGESTION_CORRECTION : [Norme supportée corrigée] | Votre requête : {query_text}`
        -   Si la requête mentionne une norme qui est une faute de frappe ou une variation évidente d'une NORME_SUPPORTÉE.
        -   Exemple: "Expliquez 62850" -> `SUGGESTION_CORRECTION : IEC 61850 | Votre requête : Expliquez 62850`
    
    4.  `NON_PERTINENT`
        -   Si la requête ne concerne AUCUNE NORME_SUPPORTÉE ni TERMES_TECHNIQUES_COURANTS, ou est manifestement hors sujet.
        -   Exemple: "Quel temps fait-il ?" -> `NON_PERTINENT`
        -   Exemple: "Informations sur la norme ISO 9001" -> `NON_PERTINENT`
    """

    # Initialize the smaller model
    model = OllamaLLM(base_url=OLLAMA_BASE_URL, model=FORMULATOR_MODEL, temperature=0)

    # Get response from model
    response = model.invoke(prompt).strip()
    # remove all thinking tokens if presents betwwen '<think> </think>'
    response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    # print(f"Réponse du formulateur : {response}")

    if response.upper().startswith("VALIDE :"):
        return QueryStatus.VALID, query_text
    elif response.upper().startswith("SUGGESTION_REFORMULATION :"):
        suggestion = response.replace(response.split(":", 1)[0] + ":", "", 1).strip()
        return QueryStatus.NEEDS_REFORMULATION, f'Votre requête pourrait être plus claire. Essayez plutôt: "{suggestion}"'
    elif response.upper().startswith("SUGGESTION_CORRECTION :"):
        content = response.replace(response.split(":", 1)[0] + ":", "", 1).strip()
        if " | Votre requête : " in content:
            corrected_standard_part, original_query_part = content.split(" | Votre requête : ", 1)
            proposed_query = f"Quels sont les principaux aspects de la norme {corrected_standard_part.strip()} ?"
            return QueryStatus.NEEDS_CORRECTION, f'Vouliez-vous parler de la norme \'{corrected_standard_part.strip()}\' ? Votre requête originale était : "{original_query_part.strip()}". Si oui, essayez: "{proposed_query}"'
        else:
            # Fallback if parsing the specific format fails
            print(f"AVERTISSEMENT : Format SUGGESTION_CORRECTION du formulateur inattendu : '{response}'")
            return QueryStatus.NEEDS_CORRECTION, f'Votre requête mentionne une norme qui pourrait être incorrecte ou mal formulée. Veuillez vérifier et essayer: "Information sur les normes supportées"'
    elif "NON_PERTINENT".upper() in response.upper():  # Case-insensitive match
        standards_list = "\n- ".join(SUPPORTED_STANDARDS)
        return QueryStatus.NON_RELEVANT, f'Votre question ne semble pas concerner les normes prises en charge. Vous pouvez poser des questions sur les normes suivantes:\n- {standards_list}\n\nEssayez par exemple: "Expliquez la norme IEC 61850"'
    else:
        # Fallback with warning - if nothing matches, assume the query is valid (original behavior)
        # Consider making this fallback stricter if issues persist.
        print(f"AVERTISSEMENT : Le formulateur a retourné un format inattendu : '{response}'")
        return QueryStatus.VALID, query_text