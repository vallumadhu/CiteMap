from openai import OpenAI
from config import OPEN_ROUTER_KEY
from tools.prompts import explainer_system_prompt

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPEN_ROUTER_KEY
)

MODEL = "google/gemma-4-31b-it:free"


def call_llm(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return response.choices[0].message.content


def explain_paper(text):
    messages = [
        {"role": "system", "content": explainer_system_prompt},
        {"role": "user", "content": f"Explain this paper clearly:\n\n{text}"}
    ]
    return call_llm(messages)


def ChatBot(prompt, system_prompt, conversation_history=[], context=None):
    messages = [{"role": "system", "content": system_prompt}]

    if context:
        messages.append({
            "role": "system",
            "content": f"Use this context to answer:\n\n{context}"
        })

    messages.extend(conversation_history)
    messages.append({"role": "user", "content": prompt})

    answer = call_llm(messages)

    conversation_history.append({"role": "user", "content": prompt})
    conversation_history.append({"role": "assistant", "content": answer})

    return {
        "response": answer,
        "history": conversation_history
    }