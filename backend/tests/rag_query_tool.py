import re
import requests
import argparse
import json
from datetime import datetime
from typing import List, Dict, Optional


# Predefined lists of queries and models
DEFAULT_QUERIES = [
    "Tu peux m'expliquer comme fonctionne la 61850 ? fais un maximum de schémas en ascii art",
    "Tu peux détailler les Logical Nodes et leur architecture dans la norme IEC 61850 en t'appuyant sur de l'ascii art pour les schémas?",
    "Tu peux me faire un exemple complet d'une application qui mesure les puissances dans un transformateur haute tension et qui utiliserait le 61850 ? ajoute des schémas en ascii et détaille bien chaque interface",
    "Tu peux me faire un exemple complet d'une application qui mesure les puissances dans un transformateur haute tension et qui utiliserait le 61850 ? ajoute des schémas en ascii et détaille bien chaque interface et utilise les mots clés de l'IEC 61850 pour chaque élément.",
    "Tu peux me faire un exemple complet d'une application qui mesure les puissances dans un transformateur haute tension et qui utiliserait le 61850 ? ajoute des schémas en ascii et détaille bien chaque interface et utilise les mots clés de l'IEC 61850 pour chaque élément. Fais apparaitre la les notions de logical nodes, logical device et IED",
]

DEFAULT_MODELS = [
    "mistral-small:latest",
    "deepseek-r1:32b",
]


def query_rag(
    query: str, model: Optional[str] = None, api_base_url: str = "http://localhost:8000"
) -> Dict:
    """Send a query to the RAG chat endpoint and return the response."""
    url = f"{api_base_url}/rag/chat"

    payload = {"query": query}
    if model:
        payload["model"] = model

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": f"Failed to connect to API at {url}. Is the server running?"}
    except requests.exceptions.Timeout:
        return {"error": f"Request timed out when connecting to {url}"}
    except requests.exceptions.HTTPError as e:
        error_detail = "Unknown error"
        try:
            error_detail = response.json().get("detail", "Unknown server error")
        except:
            pass
        return {"error": f"HTTP error: {error_detail}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def process_queries(
    queries: List[str], models: List[str], api_base_url: str = "http://localhost:8000"
) -> Dict:
    """Process multiple queries with multiple models and return results."""
    results = {}

    for query in queries:
        query_results = {}
        for model in models:
            print(f"Processing query '{query}' with model '{model}'...")
            response = query_rag(query, model, api_base_url)
            query_results[model] = response

        results[query] = query_results

    return results


def save_to_markdown(results: Dict, output_file: str):
    """Save results to a markdown file."""
    with open(output_file, "w") as f:
        f.write(f"# RAG Query Results\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for query, query_results in results.items():
            f.write(f"## Query: {query}\n\n")

            for model, response in query_results.items():
                f.write(f"### Model: {model}\n\n")

                if "error" in response:
                    f.write(f"**Error:** {response['error']}\n\n")
                else:
                    # Remove thinking tokens before saving to markdown
                    cleaned_response = response["response"]
                    if cleaned_response:
                        # Remove content between <think> and </think> tags
                        cleaned_response = re.sub(
                            r"<think>.*?</think>", "", cleaned_response, flags=re.DOTALL
                        )

                    f.write(f"**Response:**\n\n{cleaned_response}\n\n")

                    if response.get("sources") and response["sources"]:
                        f.write("**Sources:**\n\n")
                        for source in response["sources"]:
                            f.write(f"- {source}\n")
                        f.write("\n")

                f.write("---\n\n")


def main():
    parser = argparse.ArgumentParser(
        description="Send queries to RAG API and save results"
    )
    parser.add_argument(
        "--queries",
        nargs="+",
        help="List of queries to process (overrides default queries)",
    )
    parser.add_argument(
        "--models", nargs="+", help="List of models to use (overrides default models)"
    )
    parser.add_argument(
        "--output", default="rag_results.md", help="Output markdown file path"
    )
    parser.add_argument(
        "--api-url", default="http://localhost:8000/api/v1", help="Base URL for the API"
    )
    parser.add_argument(
        "--use-defaults", action="store_true", help="Use default queries and models"
    )

    args = parser.parse_args()

    # Use provided queries/models or defaults
    queries = (
        args.queries if args.queries and not args.use_defaults else DEFAULT_QUERIES
    )
    models = args.models if args.models and not args.use_defaults else DEFAULT_MODELS

    print(f"Processing {len(queries)} queries with {len(models)} models...")
    results = process_queries(queries, models, args.api_url)
    save_to_markdown(results, args.output)
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
