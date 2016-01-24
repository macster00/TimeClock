import program2
from program2 import Prog2


class Prog1:
    
    def funcA(self):
        print "funcA"
        
    def funcB(self):
        print "funcB"
        program2.main()
        
        
def main():
        one = Prog1()
        two = Prog2()
        
        one.funcB()
        two.func1_test()
        
main()