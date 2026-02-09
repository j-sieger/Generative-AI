# LangGraph Use Cases

This repository serves as a practical guide and collection of examples for building stateful, multi-actor applications with LLMs using [LangGraph](https://langchain-ai.github.io/langgraph/). It covers various patterns from simple graph structures to complex agentic workflows like RAG (Retrieval-Augmented Generation) and ReAct.

## Key Examples

The repository is structured as a series of tutorials and examples:

*   **Fundamentals**:
    *   `1.SimpleGraphs.ipynb`: Introduction to basic graph components and structure.
    *   `4.ToolCall.ipynb`: Demonstrating how agents can invoke and use external tools.
    *   `5.MemoryTOagent.ipynb`: Managing state and memory within agent workflows.

*   **Chatbots**:
    *   `2.Chatbot-sequence.py`: A simple linear chatbot implementation.
    *   `3.Chatbot-conditional.py`: Chatbot with conditional logic and branching.

*   **Agent Architectures**:
    *   `8.React-agent.py`: Implementation of a ReAct (Reasoning and Acting) agent.
    *   `9.RAG-agent.py`: A complete RAG agent that answers questions based on a PDF document (e.g., *Stock Market Performance 2024*).

*   **Human-in-the-Loop**:
    *   `7.HumaninLoop.py`: implementing workflows that require human approval or input.

## Features

- **LangChain Integration**: Leverages LangGraph for orchestration and LangChain for components.
- **IBM Watsonx**: Uses IBM Watsonx as the LLM provider for the examples.
- **Vector Search**: Demonstrates vector store integration (ChromaDB) for RAG applications.

## Prerequisites

- Python 3.11+
- IBM Watsonx API credentials

## Getting Started

1.  **Clone the repository**.

2.  **Install Dependencies**:
    This project uses [uv](https://github.com/astral-sh/uv) for dependency management.
    ```bash
    uv sync
    ```
    Alternatively, you can install the dependencies listed in `pyproject.toml`.

3.  **Environment Setup**:
    Create a `.env` file in the root directory with your IBM Watsonx credentials:
    ```env
    WATSONX_APIKEY=your_api_key
    WATSONX_PROJECT_ID=your_project_id
    WATSONX_URL=https://us-south.ml.cloud.ibm.com
    ```

4.  **Run an Example**:
    ```bash
    python 9.RAG-agent.py
    ```
