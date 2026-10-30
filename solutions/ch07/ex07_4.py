from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
OA_TOOLS = [{"type": "function", "function": {"name": n, "description": d,
             "parameters": a.model_json_schema()}} for n, (a, _, d) in TOOLS.items()]


def run_oa(question: str, model: str = "qwen2.5:7b", max_steps: int = 6) -> str:
    messages = [{"role": "system", "content": "You are a read-only diagnostics assistant."},
                {"role": "user", "content": question}]
    for _ in range(max_steps):
        r = client.chat.completions.create(model=model, messages=messages, tools=OA_TOOLS)
        msg = r.choices[0].message
        messages.append(msg.model_dump(exclude_none=True))
        if not msg.tool_calls:
            return msg.content
        for call in msg.tool_calls:
            args_model, fn, _ = TOOLS[call.function.name]
            try:
                output = fn(args_model.model_validate_json(call.function.arguments))
            except Exception as e:
                output = {"error": str(e)}
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(output)})
    return "Stopped: step limit reached."
