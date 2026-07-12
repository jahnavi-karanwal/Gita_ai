from app.gemini_client import GeminiClient

llm = GeminiClient()

response = llm.generate("Say hello.")

print(response)