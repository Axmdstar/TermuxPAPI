class SmsAnalysis:
    def __init__(self, messages):
        self.messages = messages

    def Number_Of_Messages(self):
        """Return the total number of messages."""
        return len(self.messages)
