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
    NEEDS_CORRECTION = "correction"      # Query has incorrect reference
    NON_RELEVANT = "non_relevant"      # Query is off-topic
    TOO_SHORT = "too_short"          # Query is too short to process

# Generic document types and categories for validation
SUPPORTED_DOCUMENT_TYPES = [
    "Technical specifications",
    "User manuals",
    "Installation guides", 
    "Process documentation",
    "Policy documents",
    "Research papers",
    "Standards and regulations",
    "API documentation",
    "Configuration guides",
    "Training materials"
]


def formulate_query(query_text: str):
    """
    Checks if a query is well-formed and relevant to technical documentation.
    Returns a tuple of (status, result) where:
    - status: QueryStatus enum indicating query validity type
    - result: Either the original query (if valid) or a suggestion/explanation.
    """
    # Skip processing for very short queries
    if len(query_text.strip()) < 3:
        return QueryStatus.TOO_SHORT, "Votre requête est trop courte. Veuillez fournir plus de détails."

    # Create a prompt for the formulator model
    prompt = f"""Évaluez la pertinence et la clarté de la requête utilisateur : "{query_text}"
    CONCERNE : Documentation technique et analyse de documents.
    TYPES_SUPPORTÉS : {', '.join(SUPPORTED_DOCUMENT_TYPES)}.
    TERMES_TECHNIQUES_COURANTS : API, configuration, procédures, spécifications, installation, manuel, guide, documentation.
    
    Répondez UNIQUEMENT avec l'un des formats suivants. Soyez concis. AUCUNE explication supplémentaire.
    
    1.  `VALIDE : {query_text}`
        -   Si la requête est claire, directement exploitable ET concerne de la documentation technique ou l'analyse de documents. Ceci inclut les requêtes longues et détaillées si elles sont pertinentes.
        -   Exemple (requête claire et pertinente): "Expliquez la procédure d'installation" -> `VALIDE : Expliquez la procédure d'installation`
        -   Exemple (requête longue et pertinente): "Quels sont les paramètres de configuration pour l'API..." -> `VALIDE : Quels sont les paramètres de configuration pour l'API...`
    
    2.  `SUGGESTION_REFORMULATION : [suggestion pour clarifier/préciser]`
        -   Si la requête concerne de la documentation technique MAIS est vague, imprécise, ou pourrait être mieux formulée.
        -   Exemple (requête vague): "Comment ça marche ?" -> `SUGGESTION_REFORMULATION : Pouvez-vous préciser quel processus ou système vous souhaitez comprendre ?`
        -   Exemple (terme technique seul): "API" -> `SUGGESTION_REFORMULATION : Quelles informations spécifiques recherchez-vous concernant l'API ?`
        -   Exemple (besoin de clarification): "Expliquez le truc" -> `SUGGESTION_REFORMULATION : Pouvez-vous préciser quel élément ou concept vous voulez que j'explique ?`
    
    3.  `SUGGESTION_CORRECTION : [Terme corrigé] | Votre requête : {query_text}`
        -   Si la requête mentionne un terme qui semble être une faute de frappe ou une variation d'un terme technique courant.
        -   Exemple: "configurashun" -> `SUGGESTION_CORRECTION : configuration | Votre requête : configurashun`
    
    4.  `NON_PERTINENT`
        -   Si la requête ne concerne pas la documentation technique, l'analyse de documents, ou est manifestement hors sujet.
        -   Exemple: "Quel temps fait-il ?" -> `NON_PERTINENT`
        -   Exemple: "Recette de cuisine" -> `NON_PERTINENT`
    """

    # Initialize the smaller model
    model = OllamaLLM(base_url=OLLAMA_BASE_URL, model=FORMULATOR_MODEL, temperature=0)

    # Get response from model
    response = model.invoke(prompt).strip()
    # remove all thinking tokens if presents between '<think> </think>'
    response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

    if response.upper().startswith("VALIDE :"):
        return QueryStatus.VALID, query_text
    elif response.upper().startswith("SUGGESTION_REFORMULATION :"):
        suggestion = response.replace(response.split(":", 1)[0] + ":", "", 1).strip()
        return QueryStatus.NEEDS_REFORMULATION, f'Votre requête pourrait être plus claire. Essayez plutôt: "{suggestion}"'
    elif response.upper().startswith("SUGGESTION_CORRECTION :"):
        content = response.replace(response.split(":", 1)[0] + ":", "", 1).strip()
        if " | Votre requête : " in content:
            corrected_term_part, original_query_part = content.split(" | Votre requête : ", 1)
            proposed_query = f"Informations sur {corrected_term_part.strip()}"
            return QueryStatus.NEEDS_CORRECTION, f'Vouliez-vous parler de \'{corrected_term_part.strip()}\' ? Votre requête originale était : "{original_query_part.strip()}". Si oui, essayez: "{proposed_query}"'
        else:
            # Fallback if parsing the specific format fails
            print(f"AVERTISSEMENT : Format SUGGESTION_CORRECTION du formulateur inattendu : '{response}'")
            return QueryStatus.NEEDS_CORRECTION, f'Votre requête semble contenir une erreur. Veuillez vérifier et reformuler votre question.'
    elif "NON_PERTINENT".upper() in response.upper():  # Case-insensitive match
        document_types_list = "\n- ".join(SUPPORTED_DOCUMENT_TYPES)
        return QueryStatus.NON_RELEVANT, f'Votre question ne semble pas concerner l\'analyse de documents techniques. Je peux vous aider avec les types de documents suivants:\n- {document_types_list}\n\nEssayez par exemple: "Expliquez la procédure décrite dans le document" ou "Quels sont les points clés de ce manuel ?"'
    else:
        # Fallback with warning - if nothing matches, assume the query is valid (original behavior)
        print(f"AVERTISSEMENT : Le formulateur a retourné un format inattendu : '{response}'")
        return QueryStatus.VALID, query_text