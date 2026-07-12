from app.retriever import GitaRetriever
from app.gemini_client import GeminiClient
from app.memory import ConversationMemory
from app.prompt import prompt
from app.intent import IntentDetector
from app.state import ConversationState
from app.utils import format_context
from app.verse_lookup import VerseLookup
from app.chapter_lookup import ChapterLookup
class GitaChatbot:

    def __init__(self):

        self.retriever = GitaRetriever()
        self.llm = GeminiClient()
        self.memory = ConversationMemory()
        self.intent = IntentDetector()
        self.state = ConversationState()
        self.lookup = VerseLookup()
        self.chapter_lookup = ChapterLookup()

    def chat(self, user_query):

        # -----------------------------
        # Detect Intent
        # -----------------------------

        mode = self.intent.detect(user_query)
        self.state.update(mode)

        # -----------------------------
        # Conversation History
        # -----------------------------

        history = ""

        for msg in self.memory.get_history():
            history += f"{msg['role'].capitalize()}: {msg['content']}\n"

        # ==========================================================
        # DIRECT VERSE LOOKUP (Before FAISS)
        # ==========================================================
        
        verse = self.lookup.find(user_query)
        print("=" * 50)
        print("VERSE LOOKUP")
        print(verse)
        print("=" * 50)
        
        if verse:

            context = (
                f"[Verse]\n"
                f"Chapter {verse['chapter']} Verse {verse['verse']}\n\n"
                f"{verse['content']}"
            )
            print("=" * 50)
            print("CONTEXT")
            print(context)
            print("=" * 50)

            final_prompt = prompt.format_messages(
                mode="teacher",
                context=context,
                history=history,
                question=user_query
            )

            answer = self.llm.generate(final_prompt)
            
            print("=" * 50)
            print("ANSWER")
            print(answer)
            print("=" * 50)
            self.memory.add_user_message(user_query)
            self.memory.add_assistant_message(answer)

            return {
            "answer": answer,
            "sources": [
            {
            "type": "verse",
            "chapter": verse["chapter"],
            "verse": verse["verse"],
            }
        ],
    }
        chapter = self.chapter_lookup.find(user_query)

        if chapter:

            context = "[Chapter]\n\n"

            for item in chapter:

                context += (
                    f"Verse {item['verse']}\n"
                    f"{item['content']}\n\n"
                )

            final_prompt = prompt.format_messages(
                mode="teacher",
                context=context,
                history=history,
                question=user_query,
            )

            answer = self.llm.generate(final_prompt)

            self.memory.add_user_message(user_query)
            self.memory.add_assistant_message(answer)

            return {
                "answer": answer,
                "sources": [
                    {
                        "type": "chapter",
                        "chapter": chapter[0]["chapter"],
                    }
                ],
            }

        # ==========================================================
        # VECTOR RETRIEVAL (FAISS)
        # ==========================================================

        recent_history = ""

        for msg in self.memory.get_history()[-2:]:

            if msg["role"] == "user":
                recent_history += msg["content"] + "\n"

        retrieval_query = recent_history + user_query

        results = self.retriever.search(retrieval_query, k=5)

        context = ""

        for item in results:

            if item["type"] == "verse":

                context += (
                    f"\n[Verse]\n"
                    f"Chapter {item['chapter']} Verse {item['verse']}\n"
                    f"{item['text']}\n"
                )

            elif item["type"] == "explanation":

                context += (
                    f"\n[Explanation]\n"
                    f"Chapter {item['chapter']}\n"
                    f"Topic: {item['topic']}\n"
                    f"{item['text']}\n"
                )

        # ==========================================================
        # BUILD PROMPT
        # ==========================================================

        final_prompt = prompt.format_messages(
            mode=mode,
            context=context,
            history=history,
            question=user_query
        )

        # ==========================================================
        # GENERATE RESPONSE
        # ==========================================================

        answer = self.llm.generate(final_prompt)

        # ==========================================================
        # UPDATE MEMORY
        # ==========================================================

        self.memory.add_user_message(user_query)
        self.memory.add_assistant_message(answer)

        sources = []

        for item in results:

            source = {
                "type": item["type"],
                "chapter": item["chapter"],
            }

            if item["type"] == "verse":
                source["verse"] = item["verse"]

            else:
                source["topic"] = item["topic"]

            sources.append(source)

        return {
            "answer": answer,
            "sources": sources,
        }