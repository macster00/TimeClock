import os
import shutil
class Prog2:
    def func1_test(self):
        print "function 1"
        if not os.path.exists('J:\NewPythonFolder'):
            os.makedirs('J:\NewPythonFolder')
            
    
    
    def func2_test(self):
        print "function 2"
        shutil.copytree("J:\NewPythonFolder", "J:\New")
        
def main():
    p = Prog2()
       
    #p.func1_test()
    p.func2_test()
    
main()