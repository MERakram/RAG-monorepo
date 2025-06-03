# CA-NormExpert

## Overview
CA-NormExpert is an AI assistant developed for Chauvin Arnoux Energy that allows users to query information about specific electrical norms and standards. This tool provides expert knowledge and guidance related to various international electrical standards.

## Supported Norms
The assistant can answer questions about the following norms:

- **IEC 61557-12**: Norme de mesure électrique (ENERIUM, TRIAD 3, MEMO P200)
- **IEC 60688**: Norme convertisseur de mesure (TRIAD 2, TRIAD 3, T82N)
- **IEC 61850**: Norme protocole de communication poste numérique (ELINK, TRIAD 3)
- **IEC 60051-X**: Norme indicateur analogique (CLASSIC, NORMEUROPE, PN)
- **IEC 61869-X**: Norme transformateur de courant (TRI500-600-700, JVS/JVP)
- **IEC 62053-X**: Norme compteur électrique (ALTYS, Compteurs d'achat revente)
- **EN50470-X**: Norme compteur électrique MID (ALTYS, Compteurs d'achat revente)
- **IEC 61810-X**: Norme Relais (RELAIS AMRA ET REUX)

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your system

### Running with Docker Compose

1. Clone the repository:
   ```bash
   git clone https://git.chauvin-arnoux.com/elwaak00/CA-NormExpert
   cd CA-NormExpert
   ```

2. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the application through your web browser at:
   ```
   http://localhost:3002
   ```

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

To interact with CA-NormExpert:

1. Type your question in the chat interface
2. Format questions clearly, for example:
   - "What are the key requirements in IEC 61557-12?"
   - "Explain the differences between EN50470-X and IEC 62053-X"
   - "How does IEC 61850 apply to TRIAD 3?"

The system will retrieve relevant information from the norms database and provide accurate responses.
