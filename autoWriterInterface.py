from autoWriter import AutoWriter

class AutoWriterInterface:
    def __init__(self):
        self._autoWriter = AutoWriter()
        
    def setConfig(self, *, filePath=None, timeBtChar=None, timeFStart=None):
        if filePath:
            self._autoWriter.setFilePath(filePath)
        if timeBtChar:
            self._autoWriter.setTimeBtChar(float(timeBtChar))
        if timeFStart:
            self._autoWriter.setTimeFStart(int(timeFStart))
    
    def startWriter(self, position=None):
        if position:
            self._autoWriter.setPosition(position)
        self._autoWriter.start()
    
    def stopWriter(self):
        self._autoWriter.stop()
    
    def resetWriter(self):
        self._autoWriter.reset()