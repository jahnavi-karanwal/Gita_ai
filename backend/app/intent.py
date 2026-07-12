class IntentDetector:

    def detect(self, query: str):

        q = query.lower()

        teacher = [
            "what is", "explain", "meaning", "verse",
            "chapter", "karma yoga", "bhakti",
            "jnana", "summarize"
        ]

        guide = [
            "should i", "how do i", "how can i",
            "help me", "advice", "career",
            "relationship", "what should i do"
        ]

        listener = [
            "i feel", "i am", "i'm", "sad",
            "anxious", "depressed", "lonely",
            "angry", "afraid", "failure",
            "worthless", "stressed", "lost",
            "confused", "tired"
        ]

        if any(x in q for x in teacher):
            return "teacher"

        if any(x in q for x in guide):
            return "guide"

        if any(x in q for x in listener):
            return "listener"

        return "guide"