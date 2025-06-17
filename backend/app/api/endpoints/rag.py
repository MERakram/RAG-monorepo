from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel
from typing import List, Optional
import datetime
import tempfile
import os
from pathlib import Path
import httpx
from app.core.dependencies import require_active_user
from app.schema.user import User

__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# Setup router
router = APIRouter()


# Define request/response models
class RagQueryRequest(BaseModel):
    query: str
    model: Optional[str] = None
    collection_name: str


class RagQueryResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = None


class RagModelsResponse(BaseModel):
    models: List[str]


class CompareRequest(BaseModel):
    file1_content: str
    file1_name: str
    file2_content: str
    file2_name: str
    mode: str  # technical, compliance, differences, similarities
    model: Optional[str] = None
    collection_name: str


class CompareResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = None


class SummaryRequest(BaseModel):
    text: str
    model: Optional[str] = "mistral-small3.1:latest"


class SummaryResponse(BaseModel):
    summary: str


# Now import from the rag module
from rag.query_data import query_rag_async, compare_standards_async
class RagFileUploadResponse(BaseModel):
    message: str
    filename: str
    pages: Optional[int] = None


# Now import from the rag module
from rag.query_data import query_rag_async, query_rag_with_file_async


# RAG query endpoint (non-streaming)
@router.post(
    "/chat",
    response_model=RagQueryResponse,
    status_code=200,
    response_description="RAG query response",
    name="rag:query",
)
async def rag_query(
    query_request: RagQueryRequest,
    current_user: User = Depends(require_active_user),
):
    """Submit a query to the RAG system and get a response."""
    try:
        response = await query_rag_async(
            query_request.query,
            None,
            query_request.model,
            stream=False, 
            collection_name=query_request.collection_name,
        )
        # Handle case where response might be None
        if response is None:
            response = "Sorry, I couldn't find an answer to your query."
        # Extract sources from the results if needed
        return RagQueryResponse(response=response, sources=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query failed: {str(e)}")


# New streaming endpoint
@router.post(
    "/chat/stream",
    status_code=200,
    response_description="Streaming RAG query response",
    name="rag:query_stream",
)
async def rag_query_stream(
    query_request: RagQueryRequest,
    current_user: User = Depends(require_active_user),
):
    """Submit a query to the RAG system and get a streaming response."""

    async def generate_stream():
        try:
            # Call query_rag_async with stream=True to get a generator
            response_generator = await query_rag_async(
                query_request.query,
                None,
                query_request.model,
                stream=True,
                collection_name=query_request.collection_name,
            )

            sources_data = ""

            # Process each chunk from the generator
            async for chunk in response_generator:
                if chunk.get("type") == "sources":
                    # Store sources data for the final message
                    sources_data = chunk["data"]
                    continue
                elif chunk.get("type") == "content":
                    # Create response in Ollama-like format
                    response = {
                        "model": query_request.model or "default_model",
                        "created_at": datetime.datetime.now(
                            datetime.timezone.utc
                        ).isoformat()
                        + "Z",
                        "message": {"role": "assistant", "content": chunk["data"]},
                        "done": False,
                    }

                    # Output as plain JSON with newline for NDJSON format
                    yield json.dumps(response) + "\n"

            # Final message with done=true and sources
            final_response = {
                "model": query_request.model or "default_model",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                + "Z",
                "message": {"role": "assistant", "content": ""},
                "sources": sources_data,
                "done": True,
            }
            yield json.dumps(final_response) + "\n"

        except Exception as e:
            error_response = {
                "model": query_request.model or "default_model",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                + "Z",
                "error": str(e),
                "done": True,
            }
            yield json.dumps(error_response) + "\n"

    return StreamingResponse(
        generate_stream(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.get(
    "/models",
    response_model=RagModelsResponse,
    status_code=200,
    response_description="Available RAG models",
    name="rag:list_models",
)
async def list_models(current_user: User = Depends(require_active_user)):
    """Get a list of available models for RAG."""
    try:
        available_models = [
            "qwen3:30b-a3b",
            "qwen3:32b",
            "qwq:32b",
            "mistral-small:latest",
            "mistral-small3.1:latest",
            "deepseek-r1:32b",
            "deepseek-r1:14b",
            "llama3.1:latest",
        ]

        return RagModelsResponse(models=available_models)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")


# Standards comparison endpoint (non-streaming)
@router.post(
    "/compare",
    response_model=CompareResponse,
    status_code=200,
    response_description="Standards comparison response",
    name="rag:compare",
)
async def compare_standards(
    compare_request: CompareRequest,
    current_user: User = Depends(require_active_user),
):
    """Compare two electrical standards documents using RAG context."""
    try:
        response = await compare_standards_async(
            compare_request.file1_content,
            compare_request.file1_name,
            compare_request.file2_content,
            compare_request.file2_name,
            compare_request.mode,
            None,
            compare_request.model,
            stream=False,
            collection_name=compare_request.collection_name,
        )
        
        if response is None:
            response = "Sorry, I couldn't generate a comparison for these documents."
        
        return CompareResponse(response=response, sources=[])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


# Standards comparison endpoint (streaming)
@router.post(
    "/compare/stream",
    status_code=200,
    response_description="Streaming standards comparison response",
    name="rag:compare_stream",
)
async def compare_standards_stream(
    compare_request: CompareRequest,
    current_user: User = Depends(require_active_user),
):
    """Compare two electrical standards documents using RAG context with streaming response."""

    async def generate_stream():
        try:
            # Call compare_standards_async with stream=True to get a generator
            response_generator = await compare_standards_async(
                compare_request.file1_content,
                compare_request.file1_name,
                compare_request.file2_content,
                compare_request.file2_name,
                compare_request.mode,
                None,
                compare_request.model,
                stream=True,
                collection_name=compare_request.collection_name,
            )

            sources_data = ""

            # Process each chunk from the generator
            async for chunk in response_generator:
                if chunk.get("type") == "sources":
                    # Store sources data for the final message
                    sources_data = chunk["data"]
                    continue
                elif chunk.get("type") == "content":
                    # Create response in Ollama-like format
                    response = {
                        "model": compare_request.model or "default_model",
                        "created_at": datetime.datetime.now(
                            datetime.timezone.utc
                        ).isoformat()
                        + "Z",
                        "message": {"role": "assistant", "content": chunk["data"]},
                        "done": False,
                    }

                    # Output as plain JSON with newline for NDJSON format
                    yield json.dumps(response) + "\n"

            # Final message with done=true and sources
            final_response = {
                "model": compare_request.model or "default_model",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                + "Z",
                "message": {"role": "assistant", "content": ""},
                "sources": sources_data,
                "done": True,
            }
            yield json.dumps(final_response) + "\n"

        except ValueError as e:
            error_response = {
                "model": compare_request.model or "default_model",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                + "Z",
                "error": f"Invalid request: {str(e)}",
                "done": True,
            }
            yield json.dumps(error_response) + "\n"
        except Exception as e:
            error_response = {
                "model": compare_request.model or "default_model",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                + "Z",
                "error": f"Comparison failed: {str(e)}",
                "done": True,
            }
            yield json.dumps(error_response) + "\n"

    return StreamingResponse(
        generate_stream(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
@router.post(
    "/chat-with-file",
    response_model=RagQueryResponse,
    status_code=200,
    response_description="RAG query with file upload response",
    name="rag:query_with_file",
)
async def rag_query_with_file(
    query: str = Form(...),
    model: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(require_active_user),
):
    """Submit a query to the RAG system with an uploaded PDF file."""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Process the query with the uploaded file
            response = await query_rag_with_file_async(
                query, tmp_path, model
            )
            
            # Handle case where response might be None
            if response is None:
                response = "Sorry, I couldn't find an answer to your query."
            
            return RagQueryResponse(response=response, sources=[])
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query with file failed: {str(e)}")


@router.post(
    "/upload",
    response_model=RagFileUploadResponse,
    status_code=200,
    response_description="File upload response",
    name="rag:upload_file",
)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(require_active_user),
):
    """Upload a PDF file for the RAG system to process."""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Get basic file info
            file_size = len(content)
            
            return RagFileUploadResponse(
                message="File uploaded successfully",
                filename=file.filename,
                pages=None,  # Could extract page count if needed
            )
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

# Summary generation endpoint
@router.post(
    "/summary",
    response_model=SummaryResponse,
    status_code=200,
    response_description="Generate a summary/title for chat",
    name="rag:generate_summary",
)
async def generate_summary(
    summary_request: SummaryRequest,
    current_user: User = Depends(require_active_user),
):
    """Generate a short summary/title for chat conversation."""
    try:
        # Use environment variable for Ollama URL
        ollama_url = os.getenv("VITE_OLLAMA_BASE_URL", "http://localhost:11434")
        endpoint = f"{ollama_url}/api/chat"
        
        payload = {
            "model": summary_request.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Please summarize the user's text and return the title of the text without adding any additional information. The title MUST in less than 4 words. Use the text language to summarize the text. Do not add any punctuation or markdown annotation.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text in less than 4 words: {summary_request.text}",
                },
            ],
            "stream": False,
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
            
            data = response.json()
            summary = data.get("message", {}).get("content", "Chat").strip()
            
            return SummaryResponse(summary=summary)
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Ollama: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")
