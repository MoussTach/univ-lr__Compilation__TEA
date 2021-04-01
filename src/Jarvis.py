import numpy as np
import time

from CategoryDesc import CategoryDesc
from JarvisParser import JarvisParser


class Jarvis:
    def __init__(self, fileName: str):
        self.verbose = False
        self.jarvisParser = JarvisParser()
        self.infos = self.jarvisParser.parseFile(fileName)

    def setVerbose(self, bool: bool):
        self.verbose = bool

    def useFileDesc(self, fileName: str):
        self.infos = self.jarvisParser.parseFile(fileName)

    def createDot(self):
        dot = open("graph.dot", "w")
        dot.write("digraph G {\n")
        num = 0
        print(self.infos[CategoryDesc.TRANSITIONS])
        for transition in self.infos[CategoryDesc.TRANSITIONS]:
            print(transition)

            for (key, value) in transition.items():
                nodeNumber = str(num)
                nodeNeighbor = str(value[0][0])
                inputCharacter = key
                outputCharacter = str(value[0][1])
                string = nodeNumber + "->" + nodeNeighbor + " [label=\"" + inputCharacter + "/" + outputCharacter + "\"]\n"
                dot.write(string)
            num += 1
        dot.write("}\n")

    def _lambdafermeture(self, states, list=None):
        if list is None:
            list = []
            for state in states:
                list.append(state)
        for i in range(0,len(states)):
            t = states[i]
            if t > (self.infos[CategoryDesc.NB_STATES]-1): #str(t).isnumeric() ?
                print("error")
            else:
                for transition in self.infos[CategoryDesc.TRANSITIONS][int(t)]:
                    if transition == 'l': #l pour lambda
                        output_state_lambda = self.infos[CategoryDesc.TRANSITIONS][int(t)]['l'][0][0]
                        if output_state_lambda not in list:
                            list.append(output_state_lambda)
                            self._lambdafermeture([output_state_lambda], list)

        print(list)
        return list

    def transiter(self, states, characterRead, list=None):
        if list is None:
            list = []
        for i in range(0,len(states)):
            t = states[i]
            if t > (self.infos[CategoryDesc.NB_STATES]-1): #str(t).isnumeric() ?
                print("error")
            else:
                for transition in self.infos[CategoryDesc.TRANSITIONS][int(t)]:
                    if transition == str(characterRead):
                        output_state_lambda = self.infos[CategoryDesc.TRANSITIONS][int(t)][str(characterRead)][0][0]
                        if output_state_lambda not in list:
                            list.append(output_state_lambda)
                            self.transiter([output_state_lambda], characterRead, list)
        #print(list)
        return list

    def determinisation(self):

        L = []  # Récupérer les groupes d'états X
        index_L = 1 #Parcourir le groupe d'état
        etats_parcourus = []
        P = self._lambdafermeture(self.infos[CategoryDesc.INIT])
        determinisation_finished = False

        #On récupère les états du 1er groupe d'états X
        for state in P:
            etats_parcourus.append(state)

        L.append(P)

        #Tant que la déterminisation n'est pas finie, c'est à dire qu'on rencontre de nouveaux lambda-fermetures...
        while not determinisation_finished:
            #cpt_determinisation = 0
            #Afin d'éviter le traitement inutile des lambda-fermetures vides et de refaire un groupe d'états déjà vu.
            if P and P not in L[:index_L]:
                # Toutes les lettres de l'alphabet de sortie pour l'appel de transiter.
                # (Prendre en compte le cas du lambda dans Output ('l'))
                for output_character in self.infos[CategoryDesc.OUTPUT]:
                    if output_character != 'l': #Ne pas prendre en compte le caractère lambda.
                        # On transite avec le groupe d'états X à l'aide de l'output_character
                        new_lambdas = self._lambdafermeture(self.transiter(P, output_character))
                        for state in new_lambdas:
                            if state not in L:
                                etats_parcourus.append(state)

                        L.append(new_lambdas)

                        #Création des transitions ici.

                P = L[index_L]
                index_L += 1
            else:

                # Transition vide.

                # Si on a atteint le dernier groupe d'états connus, on vérifie si la déterminisation est finie.
                if index_L == len(L):
                    determinisation_finished = True
                else:
                    # On récupère le résultat du lambda fermeture du prochain groupe d'états
                    P = L[index_L]
                    index_L += 1
        if len(etats_parcourus) < self.infos[CategoryDesc.NB_STATES]:
            raise Exception("Problème")

    def __use(self, read: str) -> str:
        for i in read:
            if not (i in (self.infos[CategoryDesc.INPUT])):
                raise \
                    Exception("Use | The argument didn't correspond to the input of Jarvis [expected '{}*' got '{}']"
                              .format(self.infos[CategoryDesc.INPUT], read))

        output = ""
        curNode = self.infos[CategoryDesc.INIT][0]
        for node in self.infos[CategoryDesc.INIT]:
            if str(read[:1]) in (self.infos[CategoryDesc.TRANSITIONS][int(node)]):
                curNode = node
                break

        print("input = {}".format(read)) if self.verbose else ""
        for letter in read:
            print("{} | '{}'".format(curNode, letter)) if self.verbose else ""
            if letter in self.infos[CategoryDesc.TRANSITIONS][curNode]:
                path = self.infos[CategoryDesc.TRANSITIONS][curNode][letter]
                for availablePath in path:
                    curNode = availablePath[0]
                    if not availablePath[1] in self.infos[CategoryDesc.META]:
                        output += availablePath[1]
                    print("\t->{}".format(availablePath[1])) if self.verbose else ""
            else:
                return "can't find a occurrence"

        if curNode in self.infos[CategoryDesc.FINAL]:
            return output
        else:
            return "the last node is not final"

    def useAutomate(self, chain: str) -> [str]:
        splitedChain = chain.split()
        resList = []
        for word in splitedChain:
            try:
                print("input = {}".format(word))
                resList.append((word, self.__use(word)))
            except Exception as err:
                print("{}{}{}".format("\33[31m", err, "\33[0m"))
        return resList


print("__________________________________________________")
try:
    jarvis = Jarvis("../dir/S0.descr")
    print(jarvis.useAutomate("010110111 1100"))
except Exception as err:
    print("{}{}{}".format("\33[31m", err, "\33[0m"))

print("__________________________________________________")
try:
    jarvis.useFileDesc("../dir/S1.descr")
    print(jarvis.useAutomate("010110111 10 1011100 10"))
except Exception as err:
    print("{}{}{}".format("\33[31m", err, "\33[0m"))

print("__________________________________________________")
try:
    jarvis.useFileDesc("../dir/S0.descr")
    print(jarvis.useAutomate("010110111 1100  11100 1101 0 1 1 100"))
except Exception as err:
    print("{}{}{}".format("\33[31m", err, "\33[0m"))
