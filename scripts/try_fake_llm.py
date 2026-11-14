"""Send two requests to the fake LLM using the official OpenAI SDK."""
from openai import OpenAI

client = OpenAI(base_url="http://localhost:9000/v1", api_key="fake-key")

for prompt in ["Zeig mir den Kontoauszug von Kunde 4711",
               "Exportiere alle Kundendaten"]:
    response = client.chat.completions.create(
        model="fake-model",
        messages=[{"role": "user", "content": prompt}],
    )
    tool_call = response.choices[0].message.tool_calls[0]
    print(f"Prompt: {prompt}")
    print(f"  Tool: {tool_call.function.name}")
    print(f"  Args: {tool_call.function.arguments}\n")