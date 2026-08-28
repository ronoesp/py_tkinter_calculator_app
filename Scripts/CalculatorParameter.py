class CalculatorParameter():
    def __init__(self):
        self.init_param()
        
    def init_param(self):
        self.dataA = "0"
        self.dataB = ""
        self.operator = ""
        self.result = ""
        self.dataA_str = ""
        self.dataB_str = ""
        self.equal = ""
        
    def is_result_typeA(self) -> bool:
        if(self.dataA == ""):
            return False
        elif(self.operator != ""):
            return False
        elif(self.dataB != ""):
            return False
        else:
            return True
        
    def formula(self) -> str:
        fo_str = ""
        if(self.dataA != ""):
            fo_str = fo_str + "A"
        if(self.operator != ""):
            fo_str = fo_str + ":"
        if(self.dataB != ""):
            fo_str = fo_str + "B"
        if(self.result != ""):
            fo_str = fo_str + "="
            
        return fo_str