from random import randint

class CFG:
    def __init__(self, term, rules):
        self.term = term  # set of terminal symbols 
        # self.aux = aux # set of non terminal symbls
        self.rules = rules # dictionary of the form: non-terminal:str or int-> List(rule: List[str], probability in the range of 1-100)
                            # two options for the key:
                            # it's either a string that represents a terminal
                            # or an int (for the number of beats you want to generate)
        # mapping probablity to a set of integers
        for key, value in self.rules.items():
            lastNum = 1
            for production in value:
                prob = production[1]
                production[1] = set()
                for i in range(lastNum, lastNum+prob):
                    production[1].add(i)
                lastNum = lastNum+prob                 

    
    # recursive function to generate a string of terminals 
    # where rule is the RHS of the production rule
    def generate(self, rule):
        if len(rule) == 1 and rule[0] in self.term:
            return rule

        # iterate through each symbol
        returnList = []
        for sym in rule:
            if not sym in self.term:
                # pick a random rule that has the given non terminal
                listOfRules = self.rules[sym]
                random = randint(1,100)
                rulePicked = None
                for rule in listOfRules:
                    if random in rule[1]:
                        rulePicked = rule[0]
                        break

                returnList.extend(self.generate(rulePicked))
            else:
                returnList.append(sym)

        return returnList

    # recursive function that generates a string of terminals
    # this is used for generating the skeleton
    def generateSkeleton(self, n):
        if n == 0:
            return []
        if n == 1:
            return ["Q1"]
        if n == 2:
            return ["Q2"]
        if n == 3:
            return ["Q3"]

        returnList = []
        random = randint(1,100)
        if random >=1 and random <= 25:
            returnList.append("Q2")
            returnList.extend(self.generateSkeleton(n-2))
        else:
            returnList.append("Q4")
            returnList.extend(self.generateSkeleton(n-4))

        return returnList
