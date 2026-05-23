from ollama import chat
from tools.prompts import explainer_system_prompt

MODEL = "qwen3:8b"


def call_llm(messages, temperature=0.7):
    response = chat(
        model=MODEL,
        messages=messages,
        options={
            "temperature": temperature
        }
    )

    return response["message"]["content"]


def explain_paper(text):
    messages = [
        {
            "role": "system",
            "content": explainer_system_prompt
        },
        {
            "role": "user",
            "content": f"Explain this paper clearly:\n\n{text}"
        }
    ]

    return call_llm(messages, temperature=0.3)


def ChatBot(prompt,system_prompt,conversation_history=None,context=None):
    if conversation_history is None:
        conversation_history = []

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    if context:
        messages.append({
            "role": "system",
            "content": f"Relevant context:\n\n{context}"
        })

    messages.extend(conversation_history)

    messages.append({
        "role": "user",
        "content": prompt
    })

    answer = call_llm(messages)

    conversation_history.append({
        "role": "user",
        "content": prompt
    })

    conversation_history.append({
        "role": "assistant",
        "content": answer
    })

    return {
        "response": answer,
        "history": conversation_history
    }