import argparse

class PredicateLogicConvert:

    def __init__(self):

        self.conf = 'Def_group'
        self.readSymbol()

    def readSymbol(self):

        self.symbols = list()
        with open(self.conf, 'rt') as f:

            for line in f:

                x = line.split()
                if not x or line[0] in ['#', '-']:
                    continue
                self.symbols.append((x[0], x[1]))



    def convert(self, inputFile, withEOQ):

        
        self.inputFile = inputFile
        if withEOQ == True:
            # Generating polish with EOQ first.
            self.polishOut = inputFile + "_EOQ"
            self.polishConvert(withEOQ=True)

        self.polishOut = inputFile + "_polish"
        self.infixOut  = inputFile + "_infix"
        self.polishConvert()
        self.infixConvert()




    def polishConvert(self, withEOQ=False):
        
        out = open(self.polishOut, 'wt')
        with open(self.inputFile, 'rt') as f:
            for line in f:
                
                if line.startswith('#'):
                    out.write(line)
                    continue

                for symbol, string in self.symbols: 
                    line = line.replace(string, symbol)
              
                # This should be put at last
                if not withEOQ:
                    line = line.replace(",EOQ", "")

                line = line.replace(",", " ") #This will also remove , in f(x,y)
                
                line = line.replace("{x x}", "{x,x}")
                line = line.replace("<x y>", "<x,y>")
                line = line.replace("restrict(xr x y)", "restrict(xr,x,y)")
                line = line.replace("dom(z x y)", "dom(z,x,y)")
                line = line.replace("ran(z x y)", "ran(z,x,y)")
                line = line.replace("nothom1(xh xf xg)", "nothom1(xh,xf,xg)")
                line = line.replace("nothom2(xh xf xg)", "nothom2(xh,xf,xg)")
                line = line.replace("COMPATIBLE(x y z)", "COMPATIBLE(x,y,z)")
                line = line.replace("HOM(x y z)", "HOM(x,y,z)")
                



                out.write(line) 
        out.close()

    def infixConvert(self):

        diction = ['#', 'InferenceRule', 'LogicalPremise', 'Degree', 'EliminationRule', 'EmpiricalPremise']
        nochange = False
        out = open(self.infixOut, 'wt')
        with open(self.polishOut, 'rt') as f:
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

                        cur = symbols[-1]
                        # Connectors
                        if cur in ["⇒", "∧"]:
                            stack.append("(" + stack.pop() + symbols.pop() + stack.pop() + ")")

                        elif cur == "￢":
                            stack.append("(" + symbols.pop() + stack.pop() + ")") 
                        
                        # Functions
                        elif cur in ['×', '∩', '∪', '+', 'notsub', '"', '◦', "'", '•']:
                            stack.append("(" + stack.pop() + symbols.pop() + stack.pop() + ")")

                        elif cur in ['{x}', 'rotate(x)', 'flip(x)', 'D(x)', 'inverse(x)', 'succ(x)', 'diag(x)', 'U(x)', 'P(x)', 
                                     'cantor(x)', 'regular(x)', 'memb(x)', 'sv1(x)', 'sv2(x)', 'sv3(x)', 'G(x)']:
                            stack.append(symbols.pop().replace('x', stack.pop()))
                        
                        elif cur == 'R(z)':
                            stack.append(symbols.pop().replace('z', stack.pop()))
                        
                        elif cur in ['~', '1st', '2nd']:
                            stack.append("(" + symbols.pop() + stack.pop() + ")") 
                        
                        elif cur == '{x,x}':
                            symbols.pop()
                            stack.append('{' + stack.pop() + ',' + stack.pop() + '}')

                        elif cur == '<x,y>':
                            stack.append(symbols.pop().replace('x', stack.pop()).replace('y', stack.pop()))

                        elif cur == 'restrict(xr,x,y)':
                            stack.append(symbols.pop().replace('xr', stack.pop()).replace('x', stack.pop()).replace('y', stack.pop()))

                        elif cur == 'nothom1(xh,xf,xg)':
                            stack.append(symbols.pop().replace('xh', stack.pop()).replace('xf', stack.pop()).replace('xg', stack.pop()))
                            
                        elif cur == 'nothom2(xh,xf,sxg)':
                            stack.append(symbols.pop().replace('xh', stack.pop()).replace('xf', stack.pop()).replace('xg', stack.pop()))
                            
                        elif cur in ['dom(z,x,y)', 'ran(z,x,y)']:
                            stack.append(symbols.pop().replace('z', stack.pop()).replace('x', stack.pop()).replace('y', stack.pop()))
                            
                             
                        # Predicate
                        elif cur in ['∈', '⊆', '=']:
                            try:
                                stack.append("(" + stack.pop() + symbols.pop() + stack.pop() + ")")
                            except Exception as e:
                                print(e)

                        elif cur in ['INDUCTIVE(x)', 'SINGVAL(x)', 'FUNCTION(x)', 'ONEONE(x)', 'OPERATION']:
                            stack.append(symbols.pop().replace('x', stack.pop()))

                        elif cur in ['COMPATIBLE(x,y,z)', 'HOM(x,y,z)']:
                            stack.append(symbols.pop().replace('x', stack.pop()).replace('y', stack.pop()).replace('z', stack.pop()))
        
                        # Variables
                        # Leave out brackets for ∀
                        elif cur in ['∀x' , '∀y', '∀u', '∀z', '∃x', '∃y', '∃u', '∃z']:
                            try:
                                stack.append(symbols.pop() + stack.pop())
                            except Exception:
                                print(line)

                        else:
                            stack.append(symbols.pop())

                    out.write(" ".join(stack)+'\n')
        out.close()        

            
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='FreeEnCal Logic Fragments Convert')

    parser.add_argument(dest='file', metavar='file', nargs=1, help='Input the name of file you want to format')
    args = parser.parse_args()
    filename = args.file[0]

    PLC = PredicateLogicConvert()
    PLC.convert(inputFile=filename, withEOQ=True)