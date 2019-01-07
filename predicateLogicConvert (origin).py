    import argparse

class PredicateLogicConvert:

    def __init__(self, inputFile):

        self.inputFile = inputFile
        self.nameOut   = self.inputFile + "_polish"
        self.polishOut = self.inputFile + "_infix"

    def readSymbol(self):

        self.symbols = dict()

    def nameConvert(self):

        out = open(self.nameOut, 'wt')
        with open(self.inputFile, 'rt') as f:
            for line in f:
                if line.startswith('#'):
                    out.write(line)
                    continue

                line = line.replace("F_2_2,C_2_0", "⇒")
                line = line.replace("F_2_2,C_2_1", "∧") 
                line = line.replace("F_2_1,C_2_3", "￢")

                line = line.replace("C_2_0", "⇒")
                line = line.replace("C_2_1", "∧")
                line = line.replace("C_2_3", "￢")

                line = line.replace("V_2_0", "A")
                line = line.replace("V_2_1", "B")
                line = line.replace("V_2_2", "C")
                line = line.replace("V_2_3", "D")
                line = line.replace("V_2_4", "E")
                line = line.replace("V_2_5", "F")
                line = line.replace("V_2_6", "G")
                line = line.replace("V_2_7", "H")
                
                line = line.replace("Q_0,V_0_0", "∀x")
                line = line.replace("Q_0,V_0_1", "∀y")
                line = line.replace("Q_0,V_0_2", "∀z")
                line = line.replace("Q_0,V_0_3", "∀u")
                line = line.replace(",EOQ", "")

                # For those in NBG
                line = line.replace("C_0_9", "V")
                line = line.replace("V_0_0", "x")
                line = line.replace("V_0_1", "y")
                line = line.replace("V_0_2", "z")
                line = line.replace("V_0_3", "u")

                line = line.replace("F_1_2,C_1_0", "∈")
                line = line.replace("F_1_2,C_1_1", "⊆")
                line = line.replace("F_1_2,C_1_2", "=")

                # This should be put at last
                line = line.replace(",", " ")

                out.write(line)
        out.close()

    def polishConvertIntex(self):

        diction = ['#', 'InferenceRule', 'LogicalPremise', 'Degree', 'EliminationRule', 'EmpiricalPremise']
        nochange = False
        out = open(self.polishOut, 'wt')
        with open(self.nameOut, 'rt') as f:
            for line in f:

                symbols = [e for e in line.split()]
                if nochange == True or symbols[0] in diction:                
                    if symbols[0] == 'Degree':
                        nochange = True
                    if symbols[0] == 'EliminationRule':
                        nochange = False
                    out.write(line)

                else:
                    stack   = []
                    while symbols:

                        sym = symbols[-1]
                        # Need brackets
                        if sym == "⇒":
                            stack.append("(" + stack.pop() + symbols.pop() + stack.pop() + ")")
                        
                        elif sym == "∧":
                            stack.append("(" + stack.pop() + symbols.pop() + stack.pop() + ")")
                        
                        elif sym == "⊆":
                            stack.append("(" + stack.pop() + symbols.pop() + stack.pop() + ")")
                            
                        elif sym == "∈":
                            stack.append("(" + stack.pop() + symbols.pop() + stack.pop() + ")")

                        elif sym == "=":
                            stack.append("(" + stack.pop() + symbols.pop() + stack.pop() + ")")

                        elif sym == "￢":
                            stack.append("(" + symbols.pop() + stack.pop() + ")")


                        # Leave out brackets
                        elif sym == "∀x":
                            # stack.append("(" + symbols.pop() + stack.pop() + ")")
                            stack.append(symbols.pop() + stack.pop())

                        elif sym == "∀y":
                            # stack.append("(" + symbols.pop() + stack.pop() + ")")
                            stack.append(symbols.pop() + stack.pop())

                        elif sym == "∀u":
                            # stack.append("(" + symbols.pop() + stack.pop() + ")")
                            stack.append(symbols.pop() + stack.pop())

                        elif sym == "∀z":
                            # stack.append("(" + symbols.pop() + stack.pop() + ")")
                            stack.append(symbols.pop() + stack.pop())
                            
                        else:
                            stack.append(symbols.pop())

                    out.write(" ".join(stack)+'\n')
        out.close()        

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FreeEnCal Logic Fragments Convert')

    parser.add_argument(dest='file', metavar='file', nargs=1, help='Input the name of file you want to format')
    args = parser.parse_args()
    filename = args.file[0]

    PLC = PredicateLogicConvert(filename)
    PLC.nameConvert()
    PLC.polishConvertIntex()