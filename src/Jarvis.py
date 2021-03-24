import numpy as np

from CategoryDesc import CategoryDesc
from JarvisParser import JarvisParser


class Jarvis:
    def __init__(self, fileName: str):
        self.jarvisParser = JarvisParser()
        self.infos = self.jarvisParser.parseFile(fileName)

    def useFileDesc(self, fileName: str):
        self.infos = self.jarvisParser.parseFile(fileName)

    def use(self, read: str) -> str:
        for i in read:
            if not (i in (self.infos[CategoryDesc.INPUT])):
                raise Exception(
                    "Use | The argument didn't correspond to the input of Jarvis [expected '{}*' got '{}']".format(
                        self.infos[CategoryDesc.INPUT], read))

        output = ""
        curNode = self.infos[CategoryDesc.INIT][0]
        for node in self.infos[CategoryDesc.INIT]:
            if str(read[:1]) in (self.infos[CategoryDesc.TRANSITIONS][int(node)]):
                curNode = node
                break

        print("input = {}".format(read))
        for letter in read:
            print("{} | '{}'".format(curNode, letter))
            if letter in self.infos[CategoryDesc.TRANSITIONS][curNode]:
                path = self.infos[CategoryDesc.TRANSITIONS][curNode][letter]
                for availablePath in path:
                    curNode = availablePath[0]
                    if not availablePath[1] in self.infos[CategoryDesc.META]:
                        output += availablePath[1]
                    print("\t->{}".format(availablePath[1]))
            else:
                return "can't find a occurrence"

        if curNode in self.infos[CategoryDesc.FINAL]:
            return output
        else:
            return "the last node is not final"

print("__________________________________________________")
jarvis = Jarvis("../dir/S0.descr")
print(jarvis.use("010110111"))

print("__________________________________________________")
jarvis.useFileDesc("../dir/S1.descr")
print(jarvis.use("010110111"))

print("__________________________________________________")
jarvis.useFileDesc("../dir/S0.descr")
print(jarvis.use("010110111"))