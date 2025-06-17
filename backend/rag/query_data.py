import asyncio
import html
import os
import logging
from pathlib import Path
import re
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

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
COMPARISON_TOP_K = int(os.getenv("COMPARISON_TOP_K", TOP_K))


PROMPT_TEMPLATE = PROMPT_TEMPLATES["simple_rag_template_fr"]

# Use comparison templates from centralized prompt system
COMPARISON_TEMPLATES = PROMPT_TEMPLATES["comparison_templates_fr"]

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

# def stop_model(model_id):
#     try:
#         subprocess.run(["ollama", "stop", model_id], check=True)
#         print(f"Model {model_id} stopped successfully.")
#     except subprocess.CalledProcessError:
#         print(f"Failed to stop model {model_id}.")


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
        logging.info(f"Scores: {[_score for doc, _score in results]}")
        return "Je n'ai pas d'information sur ce sujet. Vous pouvez me poser des questions sur les normes suivantes:\n- IEC 61557-12: Norme de mesure électrique\n- IEC 60688: Norme convertisseur de mesure\n- IEC 61850: Norme protocole de communication poste numérique\n- IEC 60051-X: Norme indicateur analogique\n- IEC 61869-X: Norme transformateur de courant\n- IEC 62053-X: Norme compteur électrique\n- EN50470-X: Norme compteur électrique MID\n- IEC 61810-X: Norme Relais"

    # Log the query and results
    logging.info(f"Query: {query_text}")
    logging.info(f"Scores: {[_score for doc, _score in results]}")

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
            # set a timer of 5 seconds to stop the model
            # stop_model(model_name)
            # await asyncio.sleep(5)

            # Start streaming the response
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


async def compare_standards_async(
    file1_content: str,
    file1_name: str,
    file2_content: str,
    file2_name: str,
    mode: str,
    vector_store=None,
    model_name=None,
    stream=False,
    collection_name: str = COLLECTION_NAME,
):
    """
    Compare two electrical standards documents using RAG context and specialized prompts.

    Args:
        file1_content: Content of the first standard document
        file1_name: Name of the first standard document
        file2_content: Content of the second standard document
        file2_name: Name of the second standard document
        mode: Comparison mode (technical, compliance, differences, similarities)
        vector_store: Optional vector store instance
        model_name: Optional model name override
        stream: Whether to stream the response
        collection_name: Vector store collection name

    Returns:
        Generated comparison response or async generator for streaming
    """

    # Validate mode
    if mode not in COMPARISON_TEMPLATES:
        raise ValueError(
            f"Invalid comparison mode: {mode}. Must be one of: {list(COMPARISON_TEMPLATES.keys())}"
        )

    # Clean the file contents first
    cleaned_file1_content = clean_text(file1_content, file1_name)
    cleaned_file2_content = clean_text(file2_content, file2_name)

    # Prepare the vector store if not provided
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

    # Create a query to retrieve relevant context from both documents
    combined_query = f"Compare electrical standards {file1_name} and {file2_name} technical specifications requirements compliance"

    # Search the vector store for relevant context
    results = vector_store.similarity_search_with_relevance_scores(
        combined_query, k=COMPARISON_TOP_K
    )

    # Build context from retrieved documents
    if results and results[0][1] >= RETRIEVING_THRESHOLD:
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = [doc.metadata.get("id", None) for doc, _score in results]
    else:
        # If no relevant context found, use minimal context
        context_text = "No specific context found in knowledge base."
        sources = []

    # Log the comparison request
    logging.info(f"Standards comparison: {file1_name} vs {file2_name}, mode: {mode}")
    logging.info(
        f"Context results scores: {[_score for doc, _score in results] if results else 'No results'}"
    )

    # Get the appropriate prompt template for the mode
    prompt_template_text = COMPARISON_TEMPLATES[mode]

    # Truncate cleaned file contents if they're too long (to fit in context window)
    max_content_tokens = 10000  # Reserve tokens for each file content
    max_content_length = (
        max_content_tokens * 4
    )  # Approximate token length for English text
    truncated_file1 = (
        cleaned_file1_content[:max_content_length] + "..."
        if len(cleaned_file1_content) > max_content_length
        else cleaned_file1_content
    )
    truncated_file2 = (
        cleaned_file2_content[:max_content_length] + "..."
        if len(cleaned_file2_content) > max_content_length
        else cleaned_file2_content
    )

    # Format the prompt with all variables
    prompt_template = ChatPromptTemplate.from_template(prompt_template_text)
    prompt = prompt_template.format(
        context=context_text,
        file1_name=file1_name,
        file1_content=truncated_file1,
        file2_name=file2_name,
        file2_content=truncated_file2,
    )

    # Set up the model
    used_model = model_name if model_name else CHAT_MODEL
    logging.info(f"Using model for comparison: {used_model}")

    model = OllamaLLM(
        base_url=OLLAMA_BASE_URL,
        model=used_model,
        temperature=float(CHAT_MODEL_TEMPERATURE),
        num_predict=8192,
        num_ctx=16384,  # Use large context window for comparison
    )

    # Format sources
    sources_md = format_sources_as_markdown(sources)

    if stream:
        # For streaming mode, return an async generator
        async def response_generator():
            response_chunks = []
            async for chunk in model.astream(prompt):
                yield {"type": "content", "data": chunk}
                response_chunks.append(chunk)

            # After all chunks are yielded, yield the sources
            yield {"type": "sources", "data": sources_md}

        return response_generator()
    else:
        # For non-streaming mode
        response_text = model.invoke(prompt)

        if not response_text:
            return "No comparison could be generated for these documents."

        # Combine response with sources
        formatted_response = f"{response_text}{sources_md}"
        return formatted_response


async def query_rag_with_file_async(
    query_text: str, pdf_file_path: str, model_name=None
):
    """
    Query the RAG system with an uploaded PDF file.
    This function will extract text from the PDF and use it as additional context.
    """
    try:
        # Load and process the PDF file
        loader = fitz.open(pdf_file_path)
        documents = []
        for page in loader:
            text = page.get_text()
            if text.strip():  # Avoid adding empty documents
                documents.append(
                    Document(page_content=text, metadata={"id": pdf_file_path})
                )

        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        pdf_chunks = text_splitter.split_documents(documents)

        # Extract text content from PDF chunks
        pdf_context = "\n\n".join([chunk.page_content for chunk in pdf_chunks])

        # Get existing vector store results
        embedding_function = embedding()
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory="./rag/" + COLLECTION_NAME,
            embedding_function=embedding_function,
        )

        # Search the existing vector store
        results = vector_store.similarity_search_with_relevance_scores(
            query_text, k=TOP_K
        )

        # Combine PDF content with vector store results
        existing_context = ""
        if results and results[0][1] >= RETRIEVING_THRESHOLD:
            existing_context = "\n\n---\n\n".join(
                [doc.page_content for doc, _score in results]
            )

        # Create combined context with PDF content prioritized
        combined_context = f"UPLOADED DOCUMENT CONTENT:\n{pdf_context}\n\n"
        if existing_context:
            combined_context += f"ADDITIONAL REFERENCE MATERIALS:\n{existing_context}"

        # Create a modified prompt template for file-based queries
        file_prompt_template = """
**QUESTION DE L'UTILISATEUR:**
{question}

**CONTEXTE À UTILISER (Documents fournis et base de connaissances):**
{context}

---

**INSTRUCTIONS SPÉCIALES POUR DOCUMENTS TÉLÉCHARGÉS:**
Vous avez accès à un document PDF téléchargé par l'utilisateur. Utilisez PRIORITAIREMENT le contenu de ce document pour répondre à la question. Si le document ne contient pas suffisamment d'informations, vous pouvez compléter avec les matériaux de référence supplémentaires.

**RÔLE ET DIRECTIVES STRICTES:**
Tu es un assistant technique spécialisé. Analyse le document téléchargé et les références pour fournir une réponse précise et complète. Tu dois répondre UNIQUEMENT en français.

**INSTRUCTIONS DE RÉPONSE:**
1. Analysez d'abord le contenu du document téléchargé
2. Identifiez les éléments pertinents pour répondre à la question
3. Complétez avec les références si nécessaire
4. Fournissez une réponse structurée et détaillée
5. Citez les sources du document téléchargé quand vous les utilisez

Répondez de manière complète et technique, en utilisant le contenu du document comme source principale.
"""

        prompt_template = ChatPromptTemplate.from_template(file_prompt_template)
        prompt = prompt_template.format(context=combined_context, question=query_text)

        used_model = model_name if model_name else CHAT_MODEL
        logging.info(f"Using model for file query: {used_model}")

        model = OllamaLLM(
            base_url=OLLAMA_BASE_URL,
            model=used_model,
            temperature=CHAT_MODEL_TEMPERATURE,
            num_predict=8192,
            num_ctx=10500,
        )

        # Generate response
        response_text = model.invoke(prompt)

        if not response_text:
            return (
                "No response could be generated for this query with the uploaded file."
            )

        # Add source information
        sources_info = f"\n\n**Sources:**\n* **Document téléchargé** ({len(pdf_chunks)} sections analysées)"
        if results and results[0][1] >= RETRIEVING_THRESHOLD:
            sources = [doc.metadata.get("id", None) for doc, _score in results]
            additional_sources = format_sources_as_markdown(sources)
            if additional_sources:
                sources_info += f"\n{additional_sources.replace('**Sources:**', '**Sources supplémentaires:**')}"

        return f"{response_text}{sources_info}"

    except Exception as e:
        logging.error(f"Error processing PDF file: {str(e)}")
        return f"Erreur lors du traitement du fichier PDF: {str(e)}"


_chauvin_patterns = [
    re.compile(r"Customer:", re.IGNORECASE),
    re.compile(r"No\.\s+of\s+User\(s\):\s*\d+", re.IGNORECASE),
    re.compile(r"Company:\s*CHAUVIN\s+ARNOUX", re.IGNORECASE),
    re.compile(r"Order\s+No\.:\s*", re.IGNORECASE),
    re.compile(r"copyright\s+of\s+IEC,\s+Geneva,\s+Switzerland", re.IGNORECASE),
    re.compile(r"All\s+rights\s+reserved", re.IGNORECASE),
    re.compile(r"licence\s+agreement", re.IGNORECASE),
    re.compile(r"custserv@iec\.ch", re.IGNORECASE),
]


def _remove_chauvin_block_programmatically(text_input: str, doc_path_info: str) -> str:
    """
    Programmatically removes the Chauvin Arnoux block from text.
    This is an alternative to the slow regex.
    """
    output_parts = []
    current_search_start_index = 0
    text_len = len(text_input)

    while current_search_start_index < text_len:
        # Find the start of a potential block ("Customer:")
        # We search in the remainder of the text_input
        match_p1 = _chauvin_patterns[0].search(
            text_input, pos=current_search_start_index
        )

        if not match_p1:
            # No more "Customer:" found, append the rest of the text
            output_parts.append(text_input[current_search_start_index:])
            break

        # "Customer:" found.
        block_potential_start_index = match_p1.start()

        # Add text before this potential block start
        output_parts.append(
            text_input[current_search_start_index:block_potential_start_index]
        )

        # Try to match the rest of the sequence from this point
        current_match_end_index = match_p1.end()
        is_a_valid_chauvin_block = True

        for i in range(1, len(_chauvin_patterns)):
            next_pattern = _chauvin_patterns[i]
            # Search for the next pattern starting from the end of the previous match
            match_next_part = next_pattern.search(
                text_input, pos=current_match_end_index
            )

            if not match_next_part:
                is_a_valid_chauvin_block = False
                break

            # Update the end index for the next search
            current_match_end_index = match_next_part.end()

        if is_a_valid_chauvin_block:
            # If it's a valid block, we skip its content by advancing current_search_start_index
            # tqdm.write(f"ℹ️ [{doc_path_info}] Chauvin Arnoux block removed.") # Optional: Log when a block is removed
            current_search_start_index = current_match_end_index
        else:
            # Not a valid block, so we keep the "Customer:" part we found
            # and continue searching after it.
            output_parts.append(
                text_input[block_potential_start_index : match_p1.end()]
            )
            current_search_start_index = match_p1.end()

    return "".join(output_parts)


def clean_text(text, doc_path_info=""):
    cleaned = re.sub(r"<[^>]+>", "", text)  # Remove HTML tags
    cleaned = re.sub(
        r"\.{2,}", " ", cleaned
    )  # Replace multiple dots with a single space
    cleaned = re.sub(
        r"\.\s+\.\s+\.\s+\.+", " ", cleaned
    )  # Replace spaced multiple dots

    # Remove Chauvin Arnoux specific block
    cleaned = _remove_chauvin_block_programmatically(cleaned, doc_path_info)

    # This regex might also be slow if it's similar in structure. Monitor its performance.
    # Remove general IEC copyright block
    cleaned = re.sub(
        r"THIS PUBLICATION IS COPYRIGHT PROTECTED.*?Copyright © .*?IEC, Geneva, Switzerland.*?All rights reserved.*?Droits de reproduction réservés.*?IEC Central Office.*?www\.iec\.ch",
        "",
        cleaned,
        flags=re.DOTALL | re.IGNORECASE,
    )
    cleaned = re.sub(
        r"Tel\.: \+41 22 919 02 11", "", cleaned
    )  # Remove specific phone number
    cleaned = html.unescape(cleaned)  # Unescape HTML entities
    cleaned = re.sub(r"\s+", " ", cleaned)  # Normalize whitespace to single spaces

    cleaned = cleaned.strip()  # Remove leading/trailing whitespace
    return cleaned
