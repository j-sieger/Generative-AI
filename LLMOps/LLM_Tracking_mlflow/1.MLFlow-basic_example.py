"""MLFlow GenAI Tracking - All-in-One Script"""
import os
import json
import mlflow
from dotenv import load_dotenv
from langchain_ibm import ChatWatsonx

# Load environment variables
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

# WatsonX Configuration
WATSONX_APIKEY = os.getenv('WATSONX_APIKEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

# Model Configuration
MODEL_ID = "meta-llama/llama-3-3-70b-instruct"
MODEL_PARAMETERS= {
    "temperature": 0.5,
    "max_tokens": 500,
    "top_p": 0.9,
    "top_k": 50,
    "stop_sequences": ["\n"]
}

# MLFlow Configuration
MLFLOW_EXPERIMENT_NAME = "MLFlow_GenAI_Experiment"

# ============================================================================
# LLM CLIENT FUNCTIONS
# ============================================================================

def create_llm_client():
    """Create and return a WatsonX LLM client"""
    llm = ChatWatsonx(
        model_id=MODEL_ID,
        url=WATSONX_URL,
        apikey=WATSONX_APIKEY,
        project_id=WATSONX_PROJECT_ID,
        params=MODEL_PARAMETERS
    )
    return llm


def generate_text(llm, prompt: str):
    """Generate text using the LLM"""
    response = llm.invoke(prompt)
    return response


# ============================================================================
# MLFLOW TRACKING FUNCTIONS
# ============================================================================

def setup_mlflow():
    """Setup MLFlow experiment"""
    if mlflow.active_run():
        mlflow.end_run()
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)


def log_parameters(prompt: str):
    """Log model parameters and prompt to MLFlow"""
    mlflow.log_param("model_name", MODEL_ID)
    mlflow.log_param("temperature", MODEL_PARAMETERS['temperature'])
    mlflow.log_param("max_tokens", MODEL_PARAMETERS['max_tokens'])
    mlflow.log_param("prompt", prompt)


def log_results(generated_text):
    """Log generation results to MLFlow
       These are all different functions for logging metrics, artifcats
    """

    # Save and log text
    with open("generated_text.txt", "w") as f:
        f.write(generated_text.content)
    mlflow.log_artifact("generated_text.txt")
    
    # Log metric
    mlflow.log_metric("generated_text_length", len(generated_text.content))
    
    # Save and log full object
    with open("chat_completion.json", "w") as f:
        json.dump(dict(generated_text), f, indent=4)
    mlflow.log_artifact("chat_completion.json")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    # Define prompt
    prompt = "what is the capital of india"
    
    # Setup MLFlow
    setup_mlflow()
    
    # Create LLM client
    llm = create_llm_client()
    
    # Start MLFlow run
    with mlflow.start_run():
        # Log parameters
        log_parameters(prompt)
        
        try:
            # Generate text
            generated_text = generate_text(llm, prompt)
            print("Generated Text:", generated_text)            

            # Log results
            log_results(generated_text)
            
        except Exception as e:
            print("❌ Error during generation:", e)
    
    print("✅ MLflow run completed.")


if __name__ == "__main__":
    main()
