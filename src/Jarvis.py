from enum import Enum
import numpy as np


class Jarvis:
    class CategoryDesc(Enum):
        META = "M"
        INPUT = "V"
        OUTPUT = "O"
        NB_STATES = "E"
        INIT = "I"
        FINAL = "F"
        TRANSITIONS = "T"

        @classmethod
        def has_value(cls, value):
            return value in cls._value2member_map_

    def __init__(self, fileName):
        parsing = {
            Jarvis.CategoryDesc.META.value: self.__parsing_META,
            Jarvis.CategoryDesc.INPUT.value: self.__parsing_INPUT,
            Jarvis.CategoryDesc.OUTPUT.value: self.__parsing_OUTPUT,
            Jarvis.CategoryDesc.NB_STATES.value: self.__parsing_NB_STATES,
            Jarvis.CategoryDesc.INIT.value: self.__parsing_INIT,
            Jarvis.CategoryDesc.FINAL.value: self.__parsing_FINAL,
            Jarvis.CategoryDesc.TRANSITIONS.value: self.__parsing_TRANSITIONS
        }

        self.infos = {
            Jarvis.CategoryDesc.META: "#",
            Jarvis.CategoryDesc.INPUT: [],
            Jarvis.CategoryDesc.OUTPUT: [],
            Jarvis.CategoryDesc.NB_STATES: -1,
            Jarvis.CategoryDesc.INIT: [0],
            Jarvis.CategoryDesc.FINAL: [],
            Jarvis.CategoryDesc.TRANSITIONS: None
        }

        self.is_meta_defined = None
        self.is_input_alphabet_set = False
        self.is_output_alphabet_set = False

        with open(fileName) as file:
            countLine = 1
            for line in file:
                splitLine = line.split()

                if len(splitLine) > 0:
                    if Jarvis.CategoryDesc.has_value(splitLine[0]):
                        parsing[splitLine[0]](splitLine, countLine)
                    else:
                        raise Exception(
                            "Parsing [L:{}] | The argument isn't valid [got '{}']".format(countLine, splitLine[0]))

                countLine += 1

    '''
    Parsing Partie META

        - Regarde si un seul argument est donné (le mot-vide), en plus de la lettre. 
        - Regarde si l'information caractérisant le META a déjà été donnée.
        - Regarde si l'élément META n'est pas écrit dans le langage INPUT et OUTPUT dans l'alphabet.

    '''

    def __parsing_META(self, splitLine: [str], countLine: int):
        if not self.is_meta_defined:
            if self.infos[Jarvis.CategoryDesc.META] == self.infos[Jarvis.CategoryDesc.INPUT] \
                    or self.infos[Jarvis.CategoryDesc.META] == self.infos[Jarvis.CategoryDesc.OUTPUT]:
                raise Exception("Parsing ['{}'|L:{}] | The meta character is already used in input alphabet or in the "
                                "output alphabet".format(Jarvis.CategoryDesc.NB_STATES, countLine))
            elif len(splitLine) != 2:
                raise Exception("Parsing ['{}'|L:{}] | The argument size of the line didn't correspond "
                                "[expected {} - got {}]".format(Jarvis.CategoryDesc.NB_STATES, countLine, 2,
                                                                len(splitLine)))
            else:
                self.infos[Jarvis.CategoryDesc.META] = splitLine[1]
                self.is_meta_defined = True

        else:
            raise Exception(
                "Parsing ['{}'|L:{}] | This type of information has already been given.".format(
                    Jarvis.CategoryDesc.NB_STATES, countLine))

    '''
        Parsing Partie INPUT

        - Regarde si un seul argument est donné, en plus de la lettre.
        - Le méta caractère du mot vide ne doit pas être dans la ligne.
        - Regarde si l'information caractérisant le INPUT a déjà été donnée.
    '''

    def __parsing_INPUT(self, splitLine: [str], countLine: int):
        if not self.is_input_alphabet_set:
            if len(splitLine) != 2:
                raise Exception("Parsing ['{}'|L:{}] | The argument size of the line didn't correspond "
                                "[expected {} - got {}]".format(Jarvis.CategoryDesc.NB_STATES, countLine, 2,
                                                                len(splitLine)))

            elif splitLine[1].strip("\"").find(self.infos[Jarvis.CategoryDesc.META]) != -1:
                raise Exception("Parsing ['{}'|L:{}] | The meta character doesn't have to be in the input alphabet."
                                .format(Jarvis.CategoryDesc.NB_STATES, countLine, 2, len(splitLine)))
            else:
                self.infos[Jarvis.CategoryDesc.INPUT] = splitLine[1]
                self.is_input_alphabet_set = True
        else:
            raise Exception(
                "Parsing ['{}'|L:{}] | This type of information has already been given.".format(
                    Jarvis.CategoryDesc.NB_STATES, countLine))

    '''
        Parsing Partie OUTPUT

        - Regarde si un seul argument est donné, en plus de la lettre.
        - Le méta caractère du mot vide ne doit pas être dans la ligne.
        - Regarde si l'information caractérisant le OUTPUT a déjà été donnée.
    '''

    def __parsing_OUTPUT(self, splitLine: [str], countLine: int):
        if not self.is_output_alphabet_set:
            if len(splitLine) != 2:
                raise Exception("Parsing ['{}'|L:{}] | The argument size of the line didn't correspond "
                                "[expected {} - got {}]".format(Jarvis.CategoryDesc.NB_STATES, countLine, 2,
                                                                len(splitLine)))

            elif splitLine[1].strip("\"").find(self.infos[Jarvis.CategoryDesc.META]) != -1:
                raise Exception("Parsing ['{}'|L:{}] | The meta character doesn't have to be in the output alphabet."
                                .format(Jarvis.CategoryDesc.NB_STATES, countLine, 2, len(splitLine)))
            else:
                self.infos[Jarvis.CategoryDesc.OUTPUT] = splitLine[1]
                self.is_output_alphabet_set = True
        else:
            raise Exception(
                "Parsing ['{}'|L:{}] | This type of information has already been given.".format(
                    Jarvis.CategoryDesc.NB_STATES, countLine))

    '''
        Parsing Partie STATES

        - Cherche directement si il y a 2 arguments.
        - Regarde si l'argument donné est numérique.
        - Regarde si l'argument donné n'est pas 0 -> invalide, cela signifie qu'il n'y a pas d'état.
        - Regarde si l'argument donné est bien supérieur aux nombres dans les listes INIT et FINAL.
    '''

    def __parsing_NB_STATES(self, splitLine: [str], countLine: int):
        if len(splitLine) == 2:
            nbStates = splitLine[1]
            if not str(nbStates).isnumeric():
                raise Exception("Parsing ['{}'|L:{}] | The given value isn't numeric [expected '{}' - got '{}']".format(
                    Jarvis.CategoryDesc.NB_STATES.value, countLine, "0|[0-9][0-9]*", nbStates))

            nbStates = int(splitLine[1])
            if nbStates <= 0:
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given value cannot be used as a valid argument [expected '{}' - got '{}']".format(
                        Jarvis.CategoryDesc.NB_STATES.value, countLine, "> 0", nbStates))

            maxValue = max(max(self.infos[Jarvis.CategoryDesc.INIT]), max(self.infos[Jarvis.CategoryDesc.FINAL] or [0]))
            if maxValue >= int(nbStates):
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given argument surpass the number of state already know by the program [expected '< {}' - got '{}']".format(
                        Jarvis.CategoryDesc.NB_STATES.value, countLine, maxValue, nbStates))

            self.infos[Jarvis.CategoryDesc.TRANSITIONS] = []
            for count in range(nbStates):
                self.infos[Jarvis.CategoryDesc.TRANSITIONS].append({})

            self.infos[Jarvis.CategoryDesc.TRANSITIONS][0]['s'] = "test"
            self.infos[Jarvis.CategoryDesc.NB_STATES] = nbStates
        else:
            raise Exception(
                "Parsing ['{}'|L:{}] | The argument size of the line didn't correspond [expected '{}' - got '{}']".format(
                    Jarvis.CategoryDesc.NB_STATES.value, countLine, 2, len(splitLine)))

    '''
        Parsing Partie INIT

        - Cherche si il y a plus de 2 arguments.
        boucle sur les arguments:
            - Regarde si l'argument donné est numérique.
            - Regarde si l'argument donné existe déjà dans la liste d'initialisation.
            - Regarde, si le nombre d'état est déjà spécifié, si l'argument est bien supérieur ou égal au nombre d'état.
    '''

    def __parsing_INIT(self, splitLine: [str], countLine: int):
        if not len(splitLine) >= 2:
            raise Exception(
                "Parsing ['{}'|L:{}] | The argument size of the line didn't correspond [expected '{}' - got '{}']".format(
                    Jarvis.CategoryDesc.INIT.value, countLine, "> 2", len(splitLine)))

        self.infos[Jarvis.CategoryDesc.INIT] = []
        for arg in splitLine[1:]:
            if not str(arg).isnumeric():
                raise Exception("Parsing ['{}'|L:{}] | The given value isn't numeric [expected '{}' - got '{}']".format(
                    Jarvis.CategoryDesc.INIT.value, countLine, "0|[0-9][0-9]*", arg))

            if int(arg) in self.infos[Jarvis.CategoryDesc.INIT]:
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given argument already exists on the variable [got '{}']".format(
                        Jarvis.CategoryDesc.NB_STATES.value, countLine, arg))

            if 0 <= self.infos[Jarvis.CategoryDesc.NB_STATES] <= int(arg):
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given argument surpass the number of state already know by the program [expected '< {}' - got '{}']".format(
                        Jarvis.CategoryDesc.NB_STATES.value, countLine, self.infos[Jarvis.CategoryDesc.NB_STATES], arg))
            self.infos[Jarvis.CategoryDesc.INIT].append(int(arg))

    '''
        Parsing Partie FINAL

        - Cherche si il y a plus de 2 arguments.
        boucle sur les arguments:
            - Regarde si l'argument donné est numérique.
            - Regarde si l'argument donné existe déjà dans la liste finale.
            - Regarde, si le nombre d'état est déjà spécifié, si l'argument est bien supérieur ou égal au nombre d'état.
    '''

    def __parsing_FINAL(self, splitLine: [str], countLine: int):
        if not len(splitLine) >= 2:
            raise Exception(
                "Parsing ['{}'|L:{}] | The argument size of the line didn't correspond [expected '{}' - got '{}']".format(
                    Jarvis.CategoryDesc.FINAL.value, countLine, "> 2", len(splitLine)))

        for arg in splitLine[1:]:
            if not str(arg).isnumeric():
                raise Exception("Parsing ['{}'|L:{}] | The given value isn't numeric [expected '{}' - got '{}']".format(
                    Jarvis.CategoryDesc.FINAL.value, countLine, "0|[0-9][0-9]*", arg))

            if int(arg) in self.infos[Jarvis.CategoryDesc.FINAL]:
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given argument already exists on the variable [got '{}']".format(
                        Jarvis.CategoryDesc.FINAL.value, countLine, arg))

            if 0 <= self.infos[Jarvis.CategoryDesc.NB_STATES] <= int(arg):
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given argument surpass the number of state already know by the program [expected '< {}' - got '{}']".format(
                        Jarvis.CategoryDesc.FINAL.value, countLine, self.infos[Jarvis.CategoryDesc.NB_STATES], arg))
            self.infos[Jarvis.CategoryDesc.FINAL].append(int(arg))

    '''
        - Regarde si les deux états font partis des états disponibles
        - Regarde si les deux transitions font partis de l'alphabet de sortie
        - Regarde si un élément n'a jamais eu de transitions
    '''

    def __parsing_TRANSITIONS(self, splitLine: [str], countLine: int):
        if 4 < len(splitLine) > 5:
            raise Exception(
                "Parsing ['{}'|L:{}] | The argument size of the line didn't correspond [expected '{}' - got '{}']".format(
                    Jarvis.CategoryDesc.TRANSITIONS.value, countLine, "4 <-> 5", len(splitLine)))

        if len(splitLine) == 4:
            splitLine.insert(4, self.infos[Jarvis.CategoryDesc.META])

        if self.infos[Jarvis.CategoryDesc.NB_STATES] <= 0:
            raise Exception(
                "Parsing ['{}'|L:{}] | The number of state isn't correct or inexistant [expected '{}' - got '{}']".format(
                    Jarvis.CategoryDesc.TRANSITIONS.value, countLine,
                    "{} > 0".format(Jarvis.CategoryDesc.NB_STATES.value), self.infos[Jarvis.CategoryDesc.NB_STATES]))

        if splitLine[1].isnumeric() and splitLine[3].isnumeric():
            if int(splitLine[1]) > (self.infos[Jarvis.CategoryDesc.NB_STATES]):
                raise Exception(
                    "Parsing ['{}'|L:{}] | State numbers are not supposed to be equal or more than the number of states : expected less than {}, got {}"
                        .format(Jarvis.CategoryDesc.TRANSITIONS.value, countLine,
                                self.infos[Jarvis.CategoryDesc.NB_STATES],
                                splitLine[1]))
            if int(splitLine[3]) > (self.infos[Jarvis.CategoryDesc.NB_STATES]):
                raise Exception(
                    "Parsing ['{}'|L:{}] | State numbers are not supposed to be equal or more than the number of states : expected less than {}, got {}"
                        .format(Jarvis.CategoryDesc.TRANSITIONS.value, countLine,
                                self.infos[Jarvis.CategoryDesc.NB_STATES], splitLine[3]))
        else:
            raise Exception("Parsing ['{}'|L:{}] | Argument type is not of the expected type (int)".format(
                Jarvis.CategoryDesc.TRANSITIONS.value, countLine))

        if (splitLine[2].strip("'") not in self.infos[Jarvis.CategoryDesc.INPUT]
                and splitLine[2].strip("'") != self.infos[Jarvis.CategoryDesc.META]):
            raise Exception(
                "Parsing ['{}'|L:{}] | Transition has a character unexpected, it needs to be an input alphabet character or the meta character".format(
                    Jarvis.CategoryDesc.TRANSITIONS.value, countLine))

        if self.infos[Jarvis.CategoryDesc.OUTPUT]:
            if (splitLine[4].strip("'") not in self.infos[Jarvis.CategoryDesc.OUTPUT]
                    and splitLine[4].strip("'") != self.infos[Jarvis.CategoryDesc.META]):
                raise Exception(
                    "Parsing ['{}'|L:{}] | Transition has a character unexpected, it needs to be an output alphabet character or the meta character".format(
                        Jarvis.CategoryDesc.TRANSITIONS.value, countLine))

        node1 = splitLine[1]
        carac1 = splitLine[2].strip("\'")
        node2 = splitLine[3]
        carac2 = splitLine[4].strip("\'")

        if str(carac1) in self.infos[Jarvis.CategoryDesc.TRANSITIONS][int(node1)]:
            self.infos[Jarvis.CategoryDesc.TRANSITIONS][int(node1)][str(carac1)].append((int(node2), str(carac2)))

        else:
            self.infos[Jarvis.CategoryDesc.TRANSITIONS][int(node1)][str(carac1)] = [(int(node2), str(carac2))]


    def use(self, read: str) -> str:
        # if not (read in (self.infos[Jarvis.CategoryDesc.INPUT])):
        #    raise Exception(
        #        "Use | The argument didn't correspond to the input of Jarvis [expected '{}*' got '{}']".format(
        #            self.infos[Jarvis.CategoryDesc.INPUT], read))

        output = ""
        curNode = self.infos[Jarvis.CategoryDesc.INIT][0]
        for node in self.infos[Jarvis.CategoryDesc.INIT]:
            if str(read[:1]) in (self.infos[Jarvis.CategoryDesc.TRANSITIONS][int(node)]):
                curNode = node
                break

        print("input = {}".format(read))
        for letter in read:
            print("{} | '{}'".format(curNode, letter))
            if letter in self.infos[Jarvis.CategoryDesc.TRANSITIONS][curNode]:
                path = self.infos[Jarvis.CategoryDesc.TRANSITIONS][curNode][letter]
                for availablePath in path:
                    curNode = availablePath[0]
                    if not availablePath[1] in self.infos[Jarvis.CategoryDesc.META]:
                        output += availablePath[1]
                    print("\t->{}".format(availablePath[1]))
            else:
                return "can't find a occurrence"

        if curNode in self.infos[Jarvis.CategoryDesc.FINAL]:
            return output
        else:
            return "the last node is not final"


jarvis = Jarvis("../dir/S0.descr")
print(jarvis.use("010110111"))
