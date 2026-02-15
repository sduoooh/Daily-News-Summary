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
    
debug_info: list[DebugInfo] = []
debug_mode = False