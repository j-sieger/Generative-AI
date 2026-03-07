# MLFlow GenAI Tracking

A simple example for tracking LLM experiments with MLFlow and IBM WatsonX.

## Project Structure

```
.
├── 1.MLFlow-basic_example.py    # All-in-one example script
├── .env.example                 # Environment variables template
├── pyproject.toml               # Project dependencies (uv)
└── mlruns/                      # MLFlow tracking data
```

## Setup

### Using uv (Recommended)

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your WatsonX credentials
   ```

4. **Run the application:**
   ```bash
   uv run python 1.MLFlow-basic_example.py
   ```

### Using pip

1. **Install dependencies:**
   ```bash
   pip install langchain-ibm mlflow python-dotenv
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your WatsonX credentials
   ```

3. **Run the application:**
   ```bash
   python 1.MLFlow-basic_example.py
   ```

## Configuration

### config.py
Contains centralized configuration settings:
- **WatsonX API credentials** - API key, project ID, and URL
- **Model parameters** - Temperature (0.5), max_tokens (200), top_p, top_k, stop_sequences
- **MLFlow settings** - Experiment name

### Environment Variables (.env)
Required environment variables:
```
WATSONX_APIKEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

## Features

The example script (`1.MLFlow-basic_example.py`) demonstrates:

### LLM Client Functions
- `create_llm_client()` - Creates and configures the WatsonX LLM client
- `generate_text()` - Generates text from a prompt using the LLM

### MLFlow Tracking Functions
- `setup_mlflow()` - Initializes MLFlow experiment
- `log_parameters()` - Logs model parameters and prompts
- `log_results()` - Logs generated text, metrics, and artifacts

### Tracked Artifacts
- **generated_text.txt** - The generated text output
- **chat_completion.json** - Full response object with metadata
- **Metrics** - Text length and other generation metrics
- **Parameters** - Model name, temperature, max_tokens, and prompt

## Usage Example

The script follows this workflow:

```python
# 1. Setup MLFlow experiment
setup_mlflow()

# 2. Create LLM client
llm = create_llm_client()

# 3. Start MLFlow run and track everything
with mlflow.start_run():
    # Log parameters
    log_parameters(prompt)
    
    # Generate text
    generated_text = generate_text(llm, prompt)
    
    # Log results and artifacts
    log_results(generated_text)
```

## View Results

Start MLFlow UI to view tracked experiments:
```bash
mlflow ui
```

Then open http://localhost:5000 in your browser to explore:
- Experiment runs and comparisons
- Logged parameters and metrics
- Generated artifacts (text files, JSON responses)
- Run metadata and timestamps

## Model Configuration

Current model: **meta-llama/llama-3-3-70b-instruct**

Parameters:
- Temperature: 0.5
- Max tokens: 200
- Top P: 0.9
- Top K: 50
- Stop sequences: ["\n"]

## Dependencies

- **langchain-ibm** (>=1.0.4) - IBM WatsonX integration
- **mlflow** (>=3.10.1) - Experiment tracking
- **python-dotenv** (>=1.2.2) - Environment variable management