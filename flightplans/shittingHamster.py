import properties
import utils
from random import randint

class drone:
    def __init__(self):
        self.rango_largo = properties.RANGO_LARGO
        self.rango_ancho = properties.RANGO_ANCHO
        self.mapa_largo = properties.MAPA_LARGO/self.rango_largo
        self.mapa_ancho = properties.MAPA_ANCHO/self.rango_ancho
        self.search_map = [[0 for j in range(int(self.mapa_largo))]for i in range(int(self.mapa_ancho))]

    def explorar(self,x,y):

        self.search_map[x][y] += 1
        exitloop = False
        firstTime = True
        #while exitloop == False:
        for y2 in range(-1,2):
            for x2 in range(-1,2):
                x3 = x+x2
                y3 = y+y2
                if x3>=0 and y3>= 0 and x3<self.mapa_ancho and y3<self.mapa_largo:
                    #print("val: "+ str(val))
                    if firstTime:
                        val = self.search_map[x3][y3]
                        x1 = x3
                        y1 = y3
                        firstTime = False
                    print("x3: "+str(x3)+ " y3: "+str(y3)+" self.mapa_ancho: "+str(self.mapa_ancho)+ " self.mapa_largo: "+ str(self.mapa_largo))
                    if self.search_map[x3][y3] < val:
                        #if randint(10)<2:
                            x1, y1 = x3, y3
                            val = self.search_map[x3][y3]
                            #print("encontre")
                            #exitloop = True
                            #break
                #if exitloop:
                    #break
        x=x1
        y=y1
        print("x: "+str(x)+" y: "+str(y))
        utils.printMatrix(self.search_map)
        return (x, y)
