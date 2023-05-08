class BannedWords:
    def __init__(self):
        self._bannedWords = [
            "frocio","stronzo"
        ]

    def isBanned(self,m : str):
        if m in self._bannedWords:
            return True
        else:
            return False