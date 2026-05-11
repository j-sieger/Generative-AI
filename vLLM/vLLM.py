import time
from vllm import LLM, SamplingParams
# Sample prompts.
prompts = ["The capital of India is"]
# Create a sampling params object.
sampling_params = SamplingParams(temperature=0.7) #, top_p=0.95

llm = LLM(model="facebook/opt-125m")
start_time = time.perf_counter()
outputs = llm.generate(prompts, sampling_params)
end_time = time.perf_counter()

print("\nGenerated Outputs:\n" + "-" * 60)
print(outputs[0].outputs[0].text)

execution_time = (end_time - start_time) * 1000
print(f"Execution time of Huggingface model: {execution_time:.3f} ms")