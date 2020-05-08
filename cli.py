from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.completion import PathCompleter
from autoWriterInterface import AutoWriterInterface

if __name__ == "__main__":    
    interface = AutoWriterInterface()
    completer = NestedCompleter.from_nested_dict({
        "set":{
            "config":{
                "file": PathCompleter(),
                "timeBtChar": None,
                "timeFStart": None
                }
            },
        "start": None,
        "stop": None,
        "reset": None,
        "exit": None,
        "help": None
        })
    session = PromptSession()
    while True:
        cmd = session.prompt('AutoWriter #>', completer=completer)
        if cmd == "":
            continue
        elif cmd == "start":
            interface.startWriter()
        elif cmd == "stop":
            interface.stopWriter()
        elif cmd == "reset":
            interface.resetWriter()
        elif "set config" in cmd:
            try:
                value = cmd.split()[3]                
            except:
                print("ERROR: you must enter an argument")
                continue
            if "file" in cmd:
                interface.setConfig(filePath=value)
            elif "timeBtChar" in cmd:
                interface.setConfig(timeBtChar=value)
            elif "timeFStart" in cmd:
                interface.setConfig(timeBtChar=value)
            else:
                print("Command unknown, use help")            
        elif cmd == "help":
            print("AutoWriter Help")
            print("Config Commands")
            print("\tset config file [pathOfFile]")
            print("\tset config timeBtChar [time between chars write]")
            print("\tset config timeFStart [time downcount start]")
            print("--")
            print("Control Commands")
            print("\tstart #Start writer")
            print("\tstop #Stop writer")
            print("\treset #Restart to head of file")
        elif cmd == "exit":
            break
        else:
            print("Command unknown, use help")