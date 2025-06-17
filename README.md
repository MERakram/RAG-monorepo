# RAG Monorepo Template

## Overview
This is a comprehensive RAG (Retrieval-Augmented Generation) monorepo template that allows users to query information from their document collections. This tool provides AI-powered knowledge extraction and question-answering capabilities for various document types and domains.

## Supported Document Types
The assistant can work with various document formats including:

- **PDF Documents**: Technical specifications, manuals, research papers
- **Text Files**: Documentation, articles, reports  
- **Word Documents**: Policies, procedures, guides
- **Markdown Files**: Technical documentation, wikis

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your system

### Running with Docker Compose

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd RAG-monorepo
   ```

2. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the application through your web browser at:
   ```
   http://localhost:3002
   ```

## Features

- **Document Upload**: Support for PDF, TXT, DOC, DOCX, and MD files
- **Intelligent Querying**: AI-powered question answering based on document content
- **Document Comparison**: Compare two documents and analyze differences/similarities
- **Multi-language Support**: Interface available in multiple languages
- **Real-time Streaming**: Live response streaming for better user experience
- **Collection Management**: Organize documents into collections for better organization

## Configuration
### Setting the Model

Choose the appropriate language model for your use case:

Recommended models include:
- `mistral`
- `llama`
- `deepseek`

### Environment Configuration

Before running the application, you need to set up your environment variables:

1. Create your environment files from the templates:
   ```bash
   cp .env.sample .env
   cp backend/rag/.env.sample backend/rag/.env
   ```

2. Edit both files according to your environment:
   - **Main `.env` file**: Configure security settings, database connections, and server ports.
   - **RAG `.env` file**: Set embedding providers, models, retrieval parameters, and the ChromaDB collection name.

3. Place your ChromaDB data folder into the `backend/rag/` directory. The path to this folder should also be configured in the `backend/rag/.env` file if it's not the default.

These configurations are essential for proper functioning of the application and must be adjusted to match your infrastructure and requirements.

## Usage

To interact with the RAG system:

1. Type your question in the chat interface
2. Upload documents to build your knowledge base
3. Format questions clearly, for example:
   - "What are the key points in this document?"
   - "Compare the requirements between these two documents"
   - "Explain the process described in the manual"

The system will retrieve relevant information from your document collection and provide accurate responses based on the content you've uploaded.
