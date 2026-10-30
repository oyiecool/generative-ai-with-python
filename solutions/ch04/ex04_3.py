class SummarisingHistory:
    def __init__(self, fast: LLM, keep_turns: int = 6):
        self.fast, self.keep = fast, keep_turns
        self.summary, self.turns = "", []

    def add(self, role: str, content: str) -> None:
        self.turns.append(Message(role, content))
        if len(self.turns) > self.keep * 2:
            old, self.turns = self.turns[:2], self.turns[2:]       # fold the oldest exchange
            transcript = "\n".join(f"{m.role}: {m.content}" for m in old)
            self.summary = self.fast.chat(
                f"Current summary:\n{self.summary or '(none)'}\n\nNew exchange:\n{transcript}\n\n"
                "Update the summary in at most 120 words. Keep names, numbers and decisions.",
                temperature=0).text

    def messages(self) -> list[Message]:
        head = [Message("user", f"Summary of earlier conversation: {self.summary}"),
                Message("assistant", "Understood.")] if self.summary else []
        return head + self.turns
