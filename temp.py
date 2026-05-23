from config import GEMINI_API_KEY,GEMINI_MODEL
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="Explain how AI works in a few words",
)

print(response.text)