from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel
from typing import List, Optional
import datetime
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


# Now import from the rag module
from rag.query_data import query_rag_async


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

                    # Output as plain JSON (not SSE format)
                    yield json.dumps(response)

            # Final message with done=true and sources
            final_response = {
                "model": query_request.model or "default_model",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                + "Z",
                "message": {"role": "assistant", "content": ""},
                "sources": sources_data,
                "done": True,
            }
            yield json.dumps(final_response)

        except Exception as e:
            error_response = {
                "model": query_request.model or "default_model",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                + "Z",
                "error": str(e),
                "done": True,
            }
            yield json.dumps(error_response)

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
