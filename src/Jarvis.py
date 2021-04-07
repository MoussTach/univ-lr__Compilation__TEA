import numpy as np
import time

from CategoryDesc import CategoryDesc
from JarvisParser import JarvisParser


class Jarvis:
    def __init__(self, fileName: str):
        self.verbose = False
        self.jarvisParser = JarvisParser()
        self.infos = self.jarvisParser.parseFile(fileName)

    def __lambdafermeture(self, states, list=None):
        if list is None:
            list = []
            for state in states:
                list.append(state)
        for i in range(0,len(states)):
            t = states[i]
            if t > (self.infos[CategoryDesc.NB_STATES]-1): #str(t).isnumeric() ?
                print("{}{}{}".format("\33[91m", "error", "\33[0m"))
            else:
                for transition, value in self.infos[CategoryDesc.TRANSITIONS][int(t)].items():
                    if transition == self.infos[CategoryDesc.META]:
                        for path in value:
                            output_state_lambda = path[0]
                            if output_state_lambda not in list:
                                list.append(output_state_lambda)
                                self.__lambdafermeture([output_state_lambda], list)
        print("{}{}{}".format("\33[32m", list, "\33[0m")) if self.verbose else ""
        return list

    def __transiter(self, states, characterRead, list=None):
        if list is None:
            list = []
        for i in range(0,len(states)):
            t = states[i]
            if t > (self.infos[CategoryDesc.NB_STATES]-1): #str(t).isnumeric() ?
                print("{}{}{}".format("\33[91m", "error", "\33[0m"))
            else:
                for transition, value in self.infos[CategoryDesc.TRANSITIONS][int(t)].items():
                    if transition == str(characterRead):
                        for path in value:
                            output_state_lambda = path[0]
                            if output_state_lambda not in list:
                                list.append(output_state_lambda)
                                self.__transiter([output_state_lambda], characterRead, list)
        print("{}{}{}".format("\33[33m", list, "\33[0m")) if self.verbose else ""
        return list

    def __is_lambda_transition(self):
        lambda_transition = False
        index = 0
        while (not lambda_transition) and (index < self.infos[CategoryDesc.NB_STATES]-1):
            if self.infos[CategoryDesc.TRANSITIONS][index]:
                for transition, value in self.infos[CategoryDesc.TRANSITIONS][index].items():
                    if transition == self.infos[CategoryDesc.META]:
                        lambda_transition = True
                if not lambda_transition:
                    index += 1
            else:
                index += 1
        return lambda_transition

    def __use(self, read: str, determinisation: bool = False) -> str:
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
        if determinisation:
            if self.__is_lambda_transition():
                self.determinisation_lambda()
            else:
                self.determinisation_transition()
            return "determined"

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
            #self.createDot()
            return output
        else:
            return "the last node is not final"


    def setVerbose(self, bool: bool):
        self.verbose = bool

    def useFileDesc(self, fileName: str):
        self.infos = self.jarvisParser.parseFile(fileName)

    def useAutomate(self, chain: str, determinisation: bool = False) -> [str]:
        splitedChain = chain.split()
        resList = []
        for word in splitedChain:
            try:
                resList.append((word, self.__use(word, determinisation)))
            except Exception as err:
                print("{}{}{}".format("\33[31m", err, "\33[0m"))
        return resList

    def createDot(self):
        dot = open("graph.dot", "w")
        dot.write("digraph G {\n")
        num = 0

        for transition in self.infos[CategoryDesc.TRANSITIONS]:

            for (key,value) in transition.items():
                nodeNumber = str(num)
                nodeNeighbor = str(value[0][0])
                inputCharacter = key
                outputCharacter = str(value[0][1])
                string = nodeNumber + "->" + nodeNeighbor + " [label=\"" + inputCharacter
                if outputCharacter:
                    string += "/" + outputCharacter
                string += "\"]\n"

                dot.write(string)
            num += 1

        for final_state in self.infos[CategoryDesc.FINAL]:
            dot.write(str(final_state) + " [peripheries=2]\n")
        dot.write("}\n")

    def createDotDeterminized(self, transitions, states_list):
        dot = open("determinizedGraph.dot", "w")
        dot.write("digraph G {\n")

        for t in transitions:
            if (t[2]):
                nodeNumber = str(t[0])
                nodeNumber = nodeNumber.strip('[]')
                nodeNumber = nodeNumber.replace(", ", "_")

                nodeNeighbor = str(t[2])
                nodeNeighbor = nodeNeighbor.strip('[]')
                nodeNeighbor = nodeNeighbor.replace(", ", "_")

                inputCharacter = t[1]

                string = "_" + nodeNumber + "->" + "_" + nodeNeighbor + " [label=\"" + inputCharacter + "\"]\n"
                dot.write(string)

        for final_state in self.infos[CategoryDesc.FINAL]:  # Pour chaque état final dans le parsing
            for states in states_list:  # Et pour chaque groupe d'états
                if final_state in states:  # Si l'état final fait partie de l'un des groupes d'états
                    string = ""
                    for state in states:  # On affiche le groupe d'états dans le .dot et on le met en nomenclature "etat final"
                        string += "_" + str(state)
                    dot.write(str(string) + " [peripheries=2]\n")

        dot.write("}\n")

    def determinisation_lambda(self):

        transition_table = []  # Récupérer les transitions de table
        states_list = []  # Récupérer les listes d'états

        L = []  # Récupérer les groupes d'états X
        index_L = 1  # Parcourir le groupe d'état
        etats_parcourus = []

        # Dans le cas d'états initiaux multiples, on récupère le premier par défaut.
        if len(self.infos[CategoryDesc.INIT]) > 1:
            P = self.__lambdafermeture([self.infos[CategoryDesc.INIT][0]])
        else:
            P = self.__lambdafermeture(self.infos[CategoryDesc.INIT])

        determinisation_finished = False
        # On récupère les états du 1er groupe d'états X
        for state in P:
            etats_parcourus.append(state)

        L.append(P)

        # Tant que la déterminisation n'est pas finie, c'est à dire qu'on rencontre de nouveaux lambda-fermetures...
        while not determinisation_finished:
            # Afin d'éviter le traitement inutile des lambda-fermetures vides et de refaire un groupe d'états déjà vu.
            if (P not in L[:(index_L - 1)] and P) or len(L) == 1:
                # Toutes les lettres de l'alphabet de sortie pour l'appel de __transiter.
                # (Prendre en compte le cas du lambda dans Output (caractère méta ici))
                for input_character in self.infos[CategoryDesc.INPUT]:
                    if input_character != self.infos[CategoryDesc.META]:  # Ne pas prendre en compte le caractère lambda.
                        # On transite avec le groupe d'états X à l'aide de l'output_character
                        new_lambdas = sorted(self.__lambdafermeture(self.__transiter(P, input_character)))
                        for state in new_lambdas:
                            if state not in etats_parcourus:
                                etats_parcourus.append(state)

                        if P not in states_list:
                            states_list.append(P)

                        L.append(new_lambdas)
                        print("{}{}{}".format("\33[34m", "Exemple {} : {} {}".format(str(index_L-1), str(P), input_character), "\33[0m")) if self.verbose else ""
                        print("{}{}{}".format("\33[34m", new_lambdas, "\33[0m")) if self.verbose else ""
                        transition_table.append((P, input_character, new_lambdas))

                P = L[index_L]
                index_L += 1

            else:
                # Si on a atteint le dernier groupe d'états connus, on vérifie si la déterminisation est finie.
                if index_L == len(L):
                    determinisation_finished = True
                else:
                    # On récupère le résultat du lambda fermeture du prochain groupe d'états
                    P = L[index_L]
                    index_L += 1
        if len(etats_parcourus) < self.infos[CategoryDesc.NB_STATES]:
            raise \
                Exception("Problème, expected {}, got {} : {}"
                          .format(self.infos[CategoryDesc.NB_STATES], len(etats_parcourus), etats_parcourus))
        self.createDotDeterminized(transition_table, states_list)

    def determinisation_transition(self):
        transition_table = []  # Récupérer les transitions de table
        states_list = []  # Récupérer les listes d'états

        L = []  # Récupérer les groupes d'états X
        index_L = 0  # Parcourir le groupe d'état
        etats_parcourus = []

        #Dans le cas d'états initiaux multiples, on récupère le premier par défaut.
        if len(self.infos[CategoryDesc.INIT]) > 1:
            P = [self.infos[CategoryDesc.INIT][0]]
        else:
            P = self.infos[CategoryDesc.INIT]
        # On récupère les états du 1er groupe d'états X
        for state in P:
            etats_parcourus.append(state)

        determinisation_finished = False
        # On récupère les états du 1er groupe d'états X

        # Tant que la déterminisation n'est pas finie, c'est à dire qu'on rencontre de nouveaux lambda-fermetures...
        while not determinisation_finished:
            # Afin d'éviter le traitement inutile des lambda-fermetures vides et de refaire un groupe d'états déjà vu.
            if (P not in L[:(index_L - 1)] and P) or len(L) == 1:
                # Toutes les lettres de l'alphabet de sortie pour l'appel de __transiter.
                # (Prendre en compte le cas du lambda dans Output (caractère méta ici))
                for input_character in self.infos[CategoryDesc.INPUT]:
                    if input_character != self.infos[CategoryDesc.META]:  # Ne pas prendre en compte le caractère lambda.
                        # On transite avec le groupe d'états X à l'aide de l'output_character
                        new_lambdas = sorted(self.__transiter(P, input_character))
                        for state in new_lambdas:
                            if state not in etats_parcourus:
                                etats_parcourus.append(state)

                        if P not in states_list:
                            states_list.append(P)

                        L.append(new_lambdas)

                        print("{}{}{}".format("\33[35m", "Exemple {} : {} {}".format(str(index_L), str(P), input_character), "\33[0m")) if self.verbose else ""
                        print("{}{}{}".format("\33[35m", new_lambdas, "\33[0m")) if self.verbose else ""
                        transition_table.append((P, input_character, new_lambdas))

                P = L[index_L]
                index_L += 1

            else:
                # Si on a atteint le dernier groupe d'états connus, on vérifie si la déterminisation est finie.
                if index_L == len(L):
                    determinisation_finished = True
                else:
                    # On récupère le résultat du lambda fermeture du prochain groupe d'états
                    P = L[index_L]
                    index_L += 1

        print("{}{}{}".format("\33[35m", transition_table, "\33[0m")) if self.verbose else ""
        self.createDotDeterminized(transition_table, states_list)

#C0 : Test de base
#S0 : Lambda transition
#S1 : Déterminisation d'un algo sans lambda-transition 1
#S2 : Déterminisation d'un algo sans lambda-transition 2
#T0 : Lambda transition

print("__________________________________________________")
try:
    jarvis = Jarvis("../dir/NDSL04.descr")
    jarvis.setVerbose(True)
    #jarvis.createDot()
    print(jarvis.useAutomate("b", determinisation=True))
except Exception as err:
    print("{}{}{}".format("\33[31m", err, "\33[0m"))