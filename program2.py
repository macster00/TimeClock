import os
import shutil
class Prog2:
    def func1_test(self):
        print "function 1"
        if not os.path.exists('E:\NewPythonFolder'):
            os.makedirs('E:\NewPythonFolder')
            
    
    
    def func2_test(self):
        print "function 2"
        if not os.path.exists('E:\New'):
            os.makedirs('E:\New')
        shutil.move("E:\NewPythonFolder\Aurelio_Mejia 20151230073237.png", "E:\New")
        
def main():
    p = Prog2()
       
    p.func1_test()
    p.func2_test()
    
main()