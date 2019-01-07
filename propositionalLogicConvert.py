# -*- coding: utf-8 -*-

class PropositionalLogicConvert:

    def __init__(self, inputFile="./input"):

        self.inputFile = inputFile
        self.nameOut   = self.inputFile + "_nameConv"
        self.polishOut = self.inputFile + "_polishConv"

    def nameConvert(self):

        out = open(self.nameOut, 'wt')
        with open(self.inputFile, 'rt') as f:
            for line in f:

                line = line.replace("F_2_2,C_2_0", "⇒")
                line = line.replace("F_2_2,C_2_1", "∧")
                line = line.replace("F_2_1,C_2_3", "￢")

                line = line.replace("V_2_0", "A")
                line = line.replace("V_2_1", "B")
                line = line.replace("V_2_2", "C")
                line = line.replace("V_2_3", "D")
                line = line.replace("V_2_4", "E")
                line = line.replace("V_2_5", "F")
                line = line.replace("V_2_6", "G")
                line = line.replace("V_2_7", "H")
                line = line.replace(",", " ")

                out.write(line)
                print(line)
        out.close()

    def polishConvert(self):

        out = open(self.polishOut, 'wt')
        with open(self.nameOut, 'rt') as f:
            for line in f:

                symbols = [e for e in line.split()]
                stack = []

                while symbols:
                    if symbols[-1] == "⇒":
                        stack.append("(" + stack.pop() + symbols.pop() + stack.pop() + ")")
                    
                    elif symbols[-1] == "∧":
                        stack.append("(" + stack.pop() + symbols.pop() + stack.pop() + ")")

                    elif symbols[-1] == "￢":
                        stack.append("(" + symbols.pop() + stack.pop() + ")")
                    
                    else:
                        stack.append(symbols.pop())

                out.write(" ".join(stack))
                out.write('\n')
        out.close()        
        
if __name__ == "__main__":
    PLC = PropositionalLogicConvert()
    PLC.nameConvert()
    PLC.polishConvert()