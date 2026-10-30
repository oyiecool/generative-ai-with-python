from openai import OpenAI

client = OpenAI(base_url="http://gpu-01.internal:8000/v1", api_key=os.environ["VLLM_KEY"])
