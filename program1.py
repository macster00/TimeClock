#import program2
#from program2 import Prog2
import cv2



class Prog1:
    
    def funcA(self):
        cv2.namedWindow("window", cv2.WINDOW_NORMAL)
        img = cv2.imread('image.jpg',0)
        cv2.imshow('window',img)
      
        cv2.resizeWindow('window', 1096, 617)
        cv2.moveWindow('window', 412, 232)
        
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
        
    def funcB(self):
        print "funcB"
        program2.main()
        
        
def main():
        one = Prog1()
        #two = Prog2()
        
        one.funcA()
        #two.func1_test()
        
main()