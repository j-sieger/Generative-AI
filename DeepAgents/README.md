# Deep Agents

A powerful framework for building intelligent AI agents with advanced capabilities for task planning, context management, and complex problem-solving.

## Table of Contents

- [What are Agents?](#what-are-agents)
- [What are Deep Agents?](#what-are-deep-agents)
- [Key Differences](#key-differences)
- [Core Capabilities](#core-capabilities)
- [When to Use Deep Agents](#when-to-use-deep-agents)
- [Example Agents](#example-agents)
- [Getting Started](#getting-started)
- [Architecture](#architecture)

## What are Agents?

**Agents** are AI systems that include LLM calls and basic tool usage capabilities. They can execute simple tasks and respond to queries but lack sophisticated planning mechanisms. Traditional agents struggle with complex, multi-step workflows that require decomposition and strategic thinking.

## What are Deep Agents?

**Deep Agents** are advanced AI agents powered by Large Language Models (LLMs) with built-in capabilities for:
- **Task Planning**: Intelligent decomposition of complex tasks into manageable steps
- **Filesystem Management**: Context management through file system operations
- **Subagent Spawning**: Dynamic creation of specialized agents for specific subtasks
- **Long-term Memory**: Persistent memory across threads using LangGraph's memory store

Deep Agents represent a significant evolution in agentic AI, enabling systems to handle sophisticated workflows that would be impossible for traditional agents.

## Key Differences

| Feature | Traditional Agents | Deep Agents |
|---------|-------------------|-------------|
| **Planning** | ❌ No built-in planning | ✅ Advanced task decomposition |
| **Complexity Handling** | ❌ Struggles with complex queries | ✅ Handles multi-step workflows |
| **Context Management** | ⚠️ Limited context handling | ✅ Filesystem tools + auto-summarization |
| **Subagent Support** | ❌ No subagent spawning | ✅ Dynamic subagent creation |
| **Memory** | ⚠️ Session-based only | ✅ Long-term persistent memory |
| **Tool Usage** | ✅ Basic tool calling | ✅ Advanced tool orchestration |

## 🎯 Core Capabilities

### 1. Planning and Task Decomposition
Deep Agents automatically break down complex tasks into logical steps, creating execution plans that ensure systematic problem-solving.

### 2. Subagent Spawning
When faced with specialized subtasks, Deep Agents can spawn dedicated subagents with specific expertise, enabling parallel processing and specialized handling.

### 3. Context Management
- **File System Tools**: Agents can offload large context to in-memory or file system storage
- **Auto-Summarization**: Automatic context summarization prevents token limit issues
- **Efficient Retrieval**: Smart context retrieval ensures relevant information is always available

### 4. Long-term Memory
Extend agents with persistent memory across threads using LangGraph's memory store, enabling continuity and learning from past interactions.

## When to Use Deep Agents

Deep Agents are ideal for scenarios requiring:

✅ **Complex, Multi-Step Tasks**
- Research projects requiring information gathering, analysis, and report generation
- Software development workflows with planning, coding, testing, and documentation
- Data analysis pipelines with collection, processing, and visualization

✅ **Large Context Management**
- Processing extensive documentation or codebases
- Analyzing multiple data sources simultaneously
- Maintaining context across long conversations

✅ **Task Planning and Decomposition**
- Breaking down ambiguous requirements into actionable steps
- Creating project roadmaps and execution plans
- Coordinating multiple interdependent tasks

✅ **Persistent Memory Requirements**
- Learning from past interactions
- Maintaining user preferences across sessions
- Building knowledge bases over time

## Example Agents

This repository contains several example implementations:

### 1. **Basic Deep Agent**
A simple Deep Agent with default configuration, demonstrating core functionality.
```python
from deepagents import create_deep_agent

agent = create_deep_agent(model=model)
```

### 2. **Research Agent**
An expert researcher agent with custom system prompt for conducting thorough research and writing polished reports.
```python
research_instructions = """
You are an expert researcher. Your job is to conduct 
thorough research, and then write a polished report.
"""

agent = create_deep_agent(
    model=model,
    system_prompt=research_instructions,
)
```

### 3. **Deep Agent with Internet Search**
An agent equipped with web search capabilities using Tavily API for real-time information retrieval.
```python
agent = create_deep_agent(
    model=model,
    tools=[internet_search]
)
```

### 4. **Simple Agent (Comparison)**
A traditional LangChain agent for comparison, showing the baseline functionality.
```python
from langchain.agents import create_agent

simple_agent = create_agent(
    model=model,
    tools=[web_search]
)
```

## 🛠️ Getting Started

### Prerequisites

- Python >= 3.11
- API keys for your chosen LLM provider (WatsonX, Groq, etc.)
- Tavily API key (for web search functionality)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DeepAgents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using uv:
```bash
uv pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your API keys:
```env
WATSONX_API_KEY=your_watsonx_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Quick Start

```python
import os
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_ibm import ChatWatsonx

# Load environment variables
load_dotenv()

# Initialize model
model = ChatWatsonx(
    model_id="meta-llama/llama-3-3-70b-instruct",
    url=os.getenv("WATSONX_URL"),
    apikey=os.getenv("WATSONX_API_KEY"),
    project_id=os.getenv("WATSONX_PROJECT_ID"),
)

# Create Deep Agent
agent = create_deep_agent(
    model=model,
    system_prompt="You are a helpful AI assistant."
)

# Invoke the agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "What is deepagent?"}]
})

print(result["messages"][-1].content)
```

