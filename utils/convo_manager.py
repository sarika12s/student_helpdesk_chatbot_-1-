import time

class ConversationManager:
    def __init__(self):
        # Each session_id stores a message history
        self.sessions = {}  # { session_id: [ {"role":"user/bot", "text": "..."} ] }
        self.max_history = 6  # keep last 6 messages only

    # ---------------- ADD USER MESSAGE ----------------
    def add_user_message(self, session_id, message):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({"role": "user", "text": message})
        self._trim_history(session_id)

    # ---------------- ADD BOT MESSAGE ----------------
    def add_bot_message(self, session_id, message):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({"role": "bot", "text": message})
        self._trim_history(session_id)

    # ---------------- TRIM OLD MESSAGES ----------------
    def _trim_history(self, session_id):
        """Keeps memory short & efficient"""
        if len(self.sessions[session_id]) > self.max_history:
            self.sessions[session_id] = self.sessions[session_id][-self.max_history:]

    # ---------------- GET CONTEXT STRING ----------------
    def get_context(self, session_id):
        """Returns combined last conversation turns for use in answer generation"""
        if session_id not in self.sessions:
            return ""

        history = self.sessions[session_id]

        # Convert into readable text
        context_text = ""
        for msg in history:
            prefix = "User: " if msg["role"] == "user" else "Bot: "
            context_text += prefix + msg["text"] + "\n"

        return context_text.strip()
