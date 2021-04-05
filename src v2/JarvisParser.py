from CategoryDesc import CategoryDesc


class JarvisParser:

    def __init__(self):
        self.infos = {}

        self.is_meta_defined = None
        self.is_input_alphabet_set = False
        self.is_output_alphabet_set = False

    def parseFile(self, fileName: str) -> {}:
        self.infos = {
            CategoryDesc.META: "#",
            CategoryDesc.INPUT: [],
            CategoryDesc.OUTPUT: [],
            CategoryDesc.NB_STATES: -1,
            CategoryDesc.INIT: [0],
            CategoryDesc.FINAL: [],
            CategoryDesc.TRANSITIONS: None
        }

        parsing = {
            CategoryDesc.COMMENTARY.value: self.__parsing_COMMENTARY,
            CategoryDesc.META.value: self.__parsing_META,
            CategoryDesc.INPUT.value: self.__parsing_INPUT,
            CategoryDesc.OUTPUT.value: self.__parsing_OUTPUT,
            CategoryDesc.NB_STATES.value: self.__parsing_NB_STATES,
            CategoryDesc.INIT.value: self.__parsing_INIT,
            CategoryDesc.FINAL.value: self.__parsing_FINAL,
            CategoryDesc.TRANSITIONS.value: self.__parsing_TRANSITIONS
        }

        self.is_meta_defined = None
        self.is_input_alphabet_set = False
        self.is_output_alphabet_set = False

        with open(fileName) as file:
            countLine = 1
            for line in file:
                splitLine = line.split()

                if len(splitLine) > 0:
                    if CategoryDesc.has_value(splitLine[0]):
                        parsing[splitLine[0]](splitLine, countLine)
                    else:
                        raise Exception(
                            "Parsing [L:{}] | The argument isn't valid [got '{}']".format(countLine, splitLine[0]))

                countLine += 1
        return self.infos

    def __parsing_COMMENTARY(self, splitLine: [str], countLine: int):
        pass

    '''
        Parsing Partie META

            - Regarde si un seul argument est donné (le mot-vide), en plus de la lettre. 
            - Regarde si l'information caractérisant le META a déjà été donnée.
            - Regarde si l'élément META n'est pas écrit dans le langage INPUT et OUTPUT dans l'alphabet.

        '''

    def __parsing_META(self, splitLine: [str], countLine: int):
        if not self.is_meta_defined:
            if self.infos[CategoryDesc.META] == self.infos[CategoryDesc.INPUT] \
                    or self.infos[CategoryDesc.META] == self.infos[CategoryDesc.OUTPUT]:
                raise Exception("Parsing ['{}'|L:{}] | The meta character is already used in input alphabet or in the "
                                "output alphabet".format(CategoryDesc.NB_STATES, countLine))
            elif len(splitLine) != 2:
                raise Exception("Parsing ['{}'|L:{}] | The argument size of the line didn't correspond "
                                "[expected {} - got {}]".format(CategoryDesc.NB_STATES, countLine, 2,
                                                                len(splitLine)))
            else:
                self.infos[CategoryDesc.META] = splitLine[1]
                self.is_meta_defined = True

        else:
            raise Exception(
                "Parsing ['{}'|L:{}] | This type of information has already been given.".format(
                    CategoryDesc.NB_STATES, countLine))

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
                                "[expected {} - got {}]".format(CategoryDesc.NB_STATES, countLine, 2,
                                                                len(splitLine)))

            #elif splitLine[1].strip("\"").find(self.infos[CategoryDesc.META]) != -1:
            #    raise Exception("Parsing ['{}'|L:{}] | The meta character doesn't have to be in the input alphabet."
            #                   .format(CategoryDesc.NB_STATES, countLine, 2, len(splitLine)))
            else:
                self.infos[CategoryDesc.INPUT] = splitLine[1].strip("\"")
                self.is_input_alphabet_set = True

                self.infos[CategoryDesc.INPUT] += self.infos[CategoryDesc.META] #Gérer le lambda
        else:
            raise Exception(
                "Parsing ['{}'|L:{}] | This type of information has already been given.".format(
                    CategoryDesc.NB_STATES, countLine))

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
                                "[expected {} - got {}]".format(CategoryDesc.NB_STATES, countLine, 2,
                                                                len(splitLine)))

            elif splitLine[1].strip("\"").find(self.infos[CategoryDesc.META]) != -1:
                raise Exception("Parsing ['{}'|L:{}] | The meta character doesn't have to be in the output alphabet."
                                .format(CategoryDesc.NB_STATES, countLine, 2, len(splitLine)))
            else:
                self.infos[CategoryDesc.OUTPUT] = splitLine[1].strip("\"")
                self.is_output_alphabet_set = True
        else:
            raise Exception(
                "Parsing ['{}'|L:{}] | This type of information has already been given.".format(
                    CategoryDesc.NB_STATES, countLine))

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
                    CategoryDesc.NB_STATES.value, countLine, "0|[0-9][0-9]*", nbStates))

            nbStates = int(splitLine[1])
            if nbStates <= 0:
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given value cannot be used as a valid argument [expected '{}' - got '{}']".format(
                        CategoryDesc.NB_STATES.value, countLine, "> 0", nbStates))

            maxValue = max(max(self.infos[CategoryDesc.INIT]), max(self.infos[CategoryDesc.FINAL] or [0]))
            if maxValue >= int(nbStates):
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given argument surpass the number of state already know by the program [expected '< {}' - got '{}']".format(
                        CategoryDesc.NB_STATES.value, countLine, maxValue, nbStates))

            self.infos[CategoryDesc.TRANSITIONS] = []
            for count in range(nbStates):
                self.infos[CategoryDesc.TRANSITIONS].append({})

            self.infos[CategoryDesc.NB_STATES] = nbStates
        else:
            raise Exception(
                "Parsing ['{}'|L:{}] | The argument size of the line didn't correspond [expected '{}' - got '{}']".format(
                    CategoryDesc.NB_STATES.value, countLine, 2, len(splitLine)))

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
                    CategoryDesc.INIT.value, countLine, "> 2", len(splitLine)))

        self.infos[CategoryDesc.INIT] = []
        for arg in splitLine[1:]:
            if not str(arg).isnumeric():
                raise Exception("Parsing ['{}'|L:{}] | The given value isn't numeric [expected '{}' - got '{}']".format(
                    CategoryDesc.INIT.value, countLine, "0|[0-9][0-9]*", arg))

            if int(arg) in self.infos[CategoryDesc.INIT]:
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given argument already exists on the variable [got '{}']".format(
                        CategoryDesc.NB_STATES.value, countLine, arg))

            if 0 <= self.infos[CategoryDesc.NB_STATES] <= int(arg):
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given argument surpass the number of state already know by the program [expected '< {}' - got '{}']".format(
                        CategoryDesc.NB_STATES.value, countLine, self.infos[CategoryDesc.NB_STATES], arg))
            self.infos[CategoryDesc.INIT].append(int(arg))

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
                    CategoryDesc.FINAL.value, countLine, "> 2", len(splitLine)))

        for arg in splitLine[1:]:
            if not str(arg).isnumeric():
                raise Exception("Parsing ['{}'|L:{}] | The given value isn't numeric [expected '{}' - got '{}']".format(
                    CategoryDesc.FINAL.value, countLine, "0|[0-9][0-9]*", arg))

            if int(arg) in self.infos[CategoryDesc.FINAL]:
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given argument already exists on the variable [got '{}']".format(
                        CategoryDesc.FINAL.value, countLine, arg))

            if 0 <= self.infos[CategoryDesc.NB_STATES] <= int(arg):
                raise Exception(
                    "Parsing ['{}'|L:{}] | The given argument surpass the number of state already know by the program [expected '< {}' - got '{}']".format(
                        CategoryDesc.FINAL.value, countLine, self.infos[CategoryDesc.NB_STATES], arg))
            self.infos[CategoryDesc.FINAL].append(int(arg))

    '''
        - Regarde si les deux états font partis des états disponibles
        - Regarde si les deux transitions font partis de l'alphabet de sortie
        - Regarde si un élément n'a jamais eu de transitions
    '''

    def __parsing_TRANSITIONS(self, splitLine: [str], countLine: int):
        if 4 < len(splitLine) > 5:
            raise Exception(
                "Parsing ['{}'|L:{}] | The argument size of the line didn't correspond [expected '{}' - got '{}']".format(
                    CategoryDesc.TRANSITIONS.value, countLine, "4 <-> 5", len(splitLine)))

        if len(splitLine) == 4:
            splitLine.insert(4, self.infos[CategoryDesc.META])

        if self.infos[CategoryDesc.NB_STATES] <= 0:
            raise Exception(
                "Parsing ['{}'|L:{}] | The number of state isn't correct or inexistant [expected '{}' - got '{}']".format(
                    CategoryDesc.TRANSITIONS.value, countLine,
                    "{} > 0".format(CategoryDesc.NB_STATES.value), self.infos[CategoryDesc.NB_STATES]))

        if splitLine[1].isnumeric() and splitLine[3].isnumeric():
            if int(splitLine[1]) > (self.infos[CategoryDesc.NB_STATES]):
                raise Exception(
                    "Parsing ['{}'|L:{}] | State numbers are not supposed to be equal or more than the number of states : expected less than {}, got {}"
                        .format(CategoryDesc.TRANSITIONS.value, countLine,
                                self.infos[CategoryDesc.NB_STATES],
                                splitLine[1]))
            if int(splitLine[3]) > (self.infos[CategoryDesc.NB_STATES]):
                raise Exception(
                    "Parsing ['{}'|L:{}] | State numbers are not supposed to be equal or more than the number of states : expected less than {}, got {}"
                        .format(CategoryDesc.TRANSITIONS.value, countLine,
                                self.infos[CategoryDesc.NB_STATES], splitLine[3]))
        else:
            raise Exception("Parsing ['{}'|L:{}] | Argument type is not of the expected type (int)".format(
                CategoryDesc.TRANSITIONS.value, countLine))

        if (splitLine[2].strip("'") not in self.infos[CategoryDesc.INPUT]
                and splitLine[2].strip("'") != self.infos[CategoryDesc.META]):
            raise Exception(
                "Parsing ['{}'|L:{}] | Transition has a character unexpected, it needs to be an input alphabet character or the meta character".format(
                    CategoryDesc.TRANSITIONS.value, countLine))

        if self.infos[CategoryDesc.OUTPUT]:
            if (splitLine[4].strip("'") not in self.infos[CategoryDesc.OUTPUT]
                    and splitLine[4].strip("'") != self.infos[CategoryDesc.META]):
                raise Exception(
                    "Parsing ['{}'|L:{}] | Transition has a character unexpected, it needs to be an output alphabet character or the meta character".format(
                        CategoryDesc.TRANSITIONS.value, countLine))

        node1 = splitLine[1]
        carac1 = splitLine[2].strip("\'")
        node2 = splitLine[3]
        carac2 = splitLine[4].strip("\'")

        if str(carac1) in self.infos[CategoryDesc.TRANSITIONS][int(node1)]:
            self.infos[CategoryDesc.TRANSITIONS][int(node1)][str(carac1)].append((int(node2), str(carac2)))

        else:
            self.infos[CategoryDesc.TRANSITIONS][int(node1)][str(carac1)] = [(int(node2), str(carac2))]
