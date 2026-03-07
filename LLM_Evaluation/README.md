# LLM Evaluation with LangSmith

This repository demonstrates LLM evaluation techniques using **LangSmith** for tracking and assessing AI applications.

## Overview

LLM evaluation is critical for measuring model performance, ensuring quality, and comparing different models or configurations. This repo showcases evaluation using **LLM-as-a-Judge** methodology where one LLM evaluates another's outputs.

## Projects

### 1. Simple LLM Application Evaluation
- **File**: `1.LLM_Evaluation_Langsmith.ipynb`
- Evaluates basic chatbot responses using **correctness** and **concision** metrics
- Compares two models: Llama 3.3 70B and Granite 8B
- Uses LangSmith for experiment tracking and visualization

### 2. RAG Application Evaluation
- **File**: `2.RAG_Evaluation.ipynb`
- Comprehensive RAG pipeline evaluation using four key metrics:
  - **Retrieval Relevance**: Measures if retrieved documents are relevant to the question
  - **Groundedness (Faithfulness)**: Checks if answers are grounded in retrieved documents without hallucinations
  - **Correctness**: Validates factual accuracy against ground truth answers
  - **Answer Relevance**: Ensures answers directly address the question
- Built with LangChain, HuggingFace embeddings, and IBM WatsonX LLM
- All evaluations tracked in LangSmith dashboard

## Key Features

- **LLM-as-a-Judge**: Uses Llama 3.3 70B as the evaluator model
- **Structured Outputs**: Leverages typed schemas for consistent evaluation results
- **LangSmith Integration**: Complete experiment tracking and comparison
- **Multiple Metrics**: Comprehensive evaluation across different quality dimensions

## Technologies

- LangChain & LangSmith
- IBM WatsonX (Llama 3.3 70B, Granite 8B)
- HuggingFace Embeddings
- Python

## Results

View experiment results and comparisons in the LangSmith dashboard (screenshots in `/images` folder).