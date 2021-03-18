class Transition:

    def __init__(self):
        self.transition = {}

    def getTransition(self) -> dict:
        return self.transition

    def addTransition(self, id, value:str):
        self.transition[id] = value
