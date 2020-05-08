from time import sleep
from pynput.keyboard import Key, Controller
from threading import Thread
from re import match
class AutoWriter:
    def __init__(self):
        self._thread = None
        self._filePath = None
        self._fileHandler = None
        self._charPosition = 0
        self._timeBtChar = 0.02
        self._timeFStart = 3
        self._flagStop = False
        self._keywordHandler = Controller()
    
    def setFilePath(self, path):
        self._filePath = path
    
    def setTimeBtChar(self, time):
        self._timeBtChar = time
    
    def setTimeFStart(self, time):
        self._timeFStart = time
    
    def setPosition(self, position):
        self._charPosition = position
    
    def getPosition(self):
        return self._charPosition
    
    def checkSpecialFunction(self, string):
        r = match("\[(\w+)=(.{1,3})]", string)
        if r:
            captureFuncion = r.group(0)
            offset = len(captureFuncion)
            nameFunction = r.group(1)                     
            value = float(r.group(2))
            #print("Excetion especial function {} with value {}".format(nameFunction, value))  
            if nameFunction == "endslow":
                return ('end-slow', value, offset)
            elif nameFunction == "slow":
                return ('slow', value, offset)            
            elif nameFunction == "sleep":
                return ('sleep', value, offset)
            elif nameFunction == "stop":
                return ('stop', value, offset)
        return False
    
    def _writer(self):
        with open(self._filePath, 'r') as self._fileHandler:
            position = self.getPosition()
            self._fileHandler.seek(position)
            timeBtChar = self._timeBtChar
            while(not self._flagStop):
                char = self._fileHandler.read(1)
                if char == "[":
                    #print("Function detection")
                    self._fileHandler.seek(position)
                    line = self._fileHandler.readline()
                    r = self.checkSpecialFunction(line)                        
                    if(r):                        
                        if(r[0] == 'slow'):
                            timeBtChar = r[1]                            
                        elif(r[0] == "end-slow"):
                            timeBtChar = self._timeBtChar
                        elif(r[0] == "sleep"):
                            sleep(r[1])
                        elif(r[0] == "stop"):
                            position += r[2]
                            print("Break function")
                            self.setPosition(position)
                            break
                        #offset
                        position += r[2]
                        self._fileHandler.seek(position)
                        continue
                    else:
                        pass
                        #print("No function")
                if not char:
                    print("End file")
                    break
                self._keywordHandler.press(char)
                self._keywordHandler.release(char)
                position = self._fileHandler.tell()
                self.setPosition(position)
                sleep(timeBtChar)
                
    def start(self):
        if self._filePath == None:
            raise
        
        for x in reversed(range(self._timeFStart+1)):            
            if not x == 0:
                print(x)
                sleep(1)
                continue
            print("Start writing")
        Thread(target=self._writer).start()      
    
    def stop(self):
        self._flagStop = True
    
    def reset(self):
        self.setPosition(0)

if(__name__ == "__main__"):
    autoWriter = AutoWriter()
    autoWriter.setFilePath("test/index.html.txt")
    autoWriter.start()