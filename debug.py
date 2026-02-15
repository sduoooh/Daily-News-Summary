class RuntimeValue:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __str__(self):
        return f"{self.name}: \n{self.value}"

class DebugInfo:
    def __init__(self, filename, funcname, msg, objs = []):
        self.filename = filename
        self.funcname = funcname
        self.message = msg
        self.objs = objs
    
    def __str__(self):
        base = f"""
Debug Info in {self.filename} - {self.funcname}:
    {self.message}
"""
        if len(self.objs) > 0:
            base += "With some runtime values:\n"
            for obj in self.objs:
                base += f"  {obj}\n"

        return base
    
class Debug:
    debug_info: list[DebugInfo] = []
    debug_mode = False
    debug_runallowlist: list[str] = []

    def __init__(self, mode=False, runallowlist=[]):
        self.debug_mode = mode
        self.debug_runallowlist = runallowlist

    def check_func_status(self, funcname):
        if self.debug_mode and funcname not in self.debug_runallowlist:
            return False
        return True
    
    def add_debug_info(self, filename, funcname, msg, objs = []):
        self.debug_info.append(DebugInfo(filename, funcname, msg, objs))

    def print_debug_info(self):
        if self.debug_mode:
            print("============ Debug Information ============\n")
            for info in self.debug_info:
                print(info, "\n")

debugger = Debug()