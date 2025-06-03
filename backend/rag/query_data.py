import os
import logging
from pathlib import Path
import re
from typing import Optional
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")


from langchain_chroma import Chroma

from rag.embedding import embedding

from rag.utils.query_formulator import formulate_query, QueryStatus
from rag.utils.prompt_system import PROMPT_TEMPLATES

load_dotenv()
CHROMA_PERSIST_PATH = os.getenv("CHROMA_PERSIST_PATH")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
CHAT_MODEL = os.getenv("CHAT_MODEL")
CHAT_MODEL_TEMPERATURE = os.getenv("CHAT_MODEL_TEMPERATURE")
OLLAMA_BASE_URL = os.getenv("VITE_OLLAMA_BASE_URL")
RETRIEVING_THRESHOLD = float(os.getenv("RETRIEVING_THRESHOLD"))
TOP_K = int(os.getenv("TOP_K"))


PROMPT_TEMPLATE = PROMPT_TEMPLATES["simple_rag_template_fr"]

# Get project root directory (for reliable path references)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

log_dir = PROJECT_ROOT / "rag" / "output"
log_dir.mkdir(parents=True, exist_ok=True)


if not logging.root.handlers:
    logging.basicConfig(
        filename=str(log_dir / "rag_ask.log"),
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


async def query_rag_async(
    query_text: str,
    vector_store=None,
    model_name=None,
    stream=False,
    collection_name: str = COLLECTION_NAME,
):
    status, processed_query = formulate_query(query_text)

    # Handle query based on its status
    if status == QueryStatus.VALID:
        # Valid query, proceed directly
        pass  # Continue with processing
    elif status in [QueryStatus.NEEDS_REFORMULATION, QueryStatus.NEEDS_CORRECTION]:
        # Query needs improvement but is relevant
        suggested_query = extract_suggestion(processed_query)
        print(f'Suggestion extraite: "{suggested_query}"')
        return f'Je n\'ai pas compris votre question. Peut-être que vous vouliez dire : "{suggested_query}" ?'

    elif status == QueryStatus.NON_RELEVANT or status == QueryStatus.TOO_SHORT:
        # Non-relevant query or too short - just show the explanation
        print(processed_query)
        logging.info(f"Query: {query_text}")
        logging.info(f"Non-relevant query or too short")
        return processed_query

    # Prepare the DB if not provided
    if vector_store is None:
        embedding_function = embedding()
        current_collection_name = (
            collection_name if collection_name else COLLECTION_NAME
        )
        vector_store = Chroma(
            persist_directory="./rag/" + CHROMA_PERSIST_PATH,
            collection_name=current_collection_name,
            embedding_function=embedding_function,
        )

    # Search the DB.
    results = vector_store.similarity_search_with_relevance_scores(query_text, k=TOP_K)
    if len(results) == 0 or results[0][1] < RETRIEVING_THRESHOLD:
        # If no results or the best result is not relevant, return a standard message
        print("No relevant results found.")
        # Logging exactly as in the original code
        logging.info(f"Query: {query_text}")
        if not results:
            print("No results found.")

        # Preserving original logging
        logging.info(f"Scores: {[score for doc, score in results]}")
        return "Je n'ai pas d'information sur ce sujet. Vous pouvez me poser des questions sur les normes suivantes:\n- IEC 61557-12: Norme de mesure électrique\n- IEC 60688: Norme convertisseur de mesure\n- IEC 61850: Norme protocole de communication poste numérique\n- IEC 60051-X: Norme indicateur analogique\n- IEC 61869-X: Norme transformateur de courant\n- IEC 62053-X: Norme compteur électrique\n- EN50470-X: Norme compteur électrique MID\n- IEC 61810-X: Norme Relais"

    # Log the query and results
    logging.info(f"Query: {query_text}")
    logging.info(f"Scores: {[score for doc, score in results]}")

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    used_model = model_name if model_name else CHAT_MODEL
    logging.info(f"Using model: {used_model}")

    model = OllamaLLM(
        base_url=OLLAMA_BASE_URL,
        model=used_model,
        temperature=CHAT_MODEL_TEMPERATURE,
        num_predict=8192,
        num_ctx=10500,
    )

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    sources_md = format_sources_as_markdown(sources)

    if stream:
        # For streaming mode, return an async generator that yields chunks
        async def response_generator():
            response_chunks = []
            async for chunk in model.astream(prompt):
                yield {"type": "content", "data": chunk}
                response_chunks.append(chunk)

            # After all chunks are yielded, yield the sources
            yield {"type": "sources", "data": sources_md}

        return response_generator()
    else:
        # For non-streaming mode, use the original approach
        response_text = model.invoke(prompt)

        # Make sure to always return a string value
        if not response_text:
            return "No response could be generated for this query."

        # Combine response text with formatted sources
        formatted_response = f"{response_text}{sources_md}"

        return formatted_response


def extract_suggestion(processed_query):
    """Extract a suggestion from the processed query using multiple patterns."""
    suggested_query = None

    # Method 1: Look for text in double quotes (most reliable approach)
    quoted_text = re.findall(r'"([^"]*)"', processed_query)
    if quoted_text:
        # Take the last quoted text, as it's most likely to be the suggestion
        raw_suggestion = quoted_text[-1]

        # Check if this contains a nested example with concrete information
        nested_example = re.search(r"'([^']*)'", raw_suggestion)
        if nested_example and "[Norme]" in raw_suggestion:
            # If there's a nested example and placeholder text, use the example instead
            suggested_query = nested_example.group(1)
            return suggested_query

        # Check if this contains placeholder text
        if "[Norme]" in raw_suggestion:
            # Look for a specific standard mentioned in the message
            standard_match = re.search(r"la norme ([A-Z]+ \d+[\-\d]*)", processed_query)
            if standard_match:
                standard = standard_match.group(1)
                # Replace placeholder with actual standard
                suggested_query = raw_suggestion.replace("[Norme]", standard)
                return suggested_query
            else:
                # Fallback to a common standard if no specific one is mentioned
                return "Quels sont les principaux aspects de la norme IEC 61850 ?"

        # Use the raw suggestion if no placeholders detected
        return raw_suggestion

    # Rest of the extraction methods remain unchanged
    # Method 2: Look for text after specific phrases if no quotes found
    patterns = [
        r"Essayez plutôt:\s*(.*)",
        r"plutôt:\s*(.*)",
        r"essayez:\s*(.*)",
        r"parler de la norme\s*\'([^\']*)",  # For standard name corrections
    ]

    for pattern in patterns:
        matches = re.search(pattern, processed_query, re.IGNORECASE)
        if matches:
            suggested_query = matches.group(1).strip().strip("\"'")
            return suggested_query

    # Method 3: For correction cases with standard names
    if "Vouliez-vous parler de la norme" in processed_query:
        standard_match = re.search(r"la norme '([^']*)'", processed_query)
        if standard_match:
            standard = standard_match.group(1)
            return f"Information sur la norme {standard}"

    # Method 4: Extract any IEC standard mentioned as last resort
    iec_match = re.search(r"(IEC \d+[\-\d]*)", processed_query)
    if iec_match:
        standard = iec_match.group(1)
        return f"Expliquez la norme {standard}"

    return None


def format_sources_as_markdown(sources):
    """
    Format a list of source IDs as Markdown bullet points with improved styling.
    Makes filenames bold and page numbers italic for better readability.

    Args:
        sources: List of source IDs (e.g., "path/to/filename.pdf:141:0")

    Returns:
        String with styled Markdown bullet points of unique filenames and their pages.
    """
    if not sources:
        return ""

    # Use a dictionary to group pages by filename
    file_pages = {}

    for source_id in sources:
        if not source_id:
            continue

        parts = source_id.split(":")
        if not parts:
            continue

        filename_with_path = parts[0]
        filename = os.path.basename(filename_with_path)

        if not filename:
            continue

        page_number = None
        if len(parts) >= 2 and parts[1].isdigit():
            page_number = int(parts[1])

        if filename not in file_pages:
            file_pages[filename] = set()

        if page_number is not None:
            file_pages[filename].add(page_number)

    if not file_pages:
        return ""

    formatted_lines = []
    # Sort filenames for consistent output
    for filename in sorted(file_pages.keys()):
        pages = sorted(list(file_pages[filename]))
        if pages:
            page_str = ", ".join(map(str, pages))
            if len(pages) > 1:
                formatted_lines.append(f"* **{filename}**, pages *{page_str}*")
            else:
                formatted_lines.append(f"* **{filename}**, page *{page_str}*")
        else:
            # Fallback if a file was listed but had no valid page numbers
            formatted_lines.append(f"* **{filename}**")

    if not formatted_lines:
        return ""

    sources_md = "\n\n**Sources:**\n" + "\n".join(formatted_lines)
    return sources_md
