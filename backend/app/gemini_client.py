import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class GeminiClient:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.4,
        )
    def generate(self, prompt):

        response = self.llm.invoke(prompt)

        if isinstance(response.content, str):
            return response.content

        if isinstance(response.content, list):
            return "".join(
                block.get("text", "")
                for block in response.content
                if isinstance(block, dict)
            )

        return str(response.content)
    