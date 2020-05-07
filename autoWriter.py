from time import sleep
from pynput.keyboard import Key, Controller
from re import match
class AutoWriter:
    def __init__(self):
        self._thread = None
        self._filePath = None
        self._fileHandler = None
        self._charPosition = 0
        self._timeBtChar = 0.01
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
        print(string)
        r = match("\[(\w+)=(.{1,3})]", string)
        if r:
            captureFucntion = r.group(0)
            lenString = len(captureFucntion)
            nameFunction = r.group(1)            
            value = float(r.group(2))
            print(captureFucntion)
            print(nameFunction, value)            
            if 'slow=' in string:
                return ('slow', value, lenString)
            elif 'endslow=' in string:
                return ('end-slow', value, lenString)
            elif 'sleep=' in string:
                return ('sleep', value, lenString)
        return False
    
    def start(self):
        for x in reversed(range(self._timeFStart+1)):            
            if not x == 0:
                print(x)
                sleep(1)
                continue
            print("Start writing")
            
        with open(self._filePath, 'r') as self._fileHandler:
            position = self.getPosition()
            self._fileHandler.seek(position)
            timeBtChar = self._timeBtChar
            while(not self._flagStop):
                char = self._fileHandler.read(1)
                if char == "[":
                    print("Function detecttion")
                    print(position)
                    self._fileHandler.seek(position-1)
                    line = self._fileHandler.readline()
                    r = self.checkSpecialFunction(line)                        
                    if(r):
                        if(r[0] == 'slow'):
                            timeBtChar = r[1]
                            
                        elif(r[0] == "end-slow"):
                            timeBtChar = self._timeBtChar
                        elif(r[0] == "sleep"):
                            sleep(r[1])
                        position += r[2]
                        self._fileHandler.seek(position)
                        continue
                if not char:
                    print("End file")
                    break
                #print(char)
                self._keywordHandler.press(char)
                self._keywordHandler.release(char)
                position += 1
                self.setPosition(position)
                sleep(timeBtChar)
                
            
    
    def stop(self):
        self._flagStop = True
    
    def reset(self):
        self.setPosition(0)

if(__name__ == "__main__"):
    autoWriter = AutoWriter()
    autoWriter.setFilePath("test/index.html.txt")
    autoWriter.start()