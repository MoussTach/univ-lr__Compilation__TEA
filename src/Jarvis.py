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

        if self.infos[Jarvis.CategoryDesc.TRANSITIONS] is not None:
            for trans in self.infos[Jarvis.CategoryDesc.TRANSITIONS]:
                print(trans)

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

            self.infos[Jarvis.CategoryDesc.TRANSITIONS] = [[None] * nbStates] * nbStates
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

        print(self.infos[Jarvis.CategoryDesc.INIT])

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

        print(self.infos[Jarvis.CategoryDesc.FINAL])

    def __parsing_TRANSITIONS(self, splitLine: [str], countLine: int):
        print(splitLine)


jarvis = Jarvis("../dir/S0.descr")
