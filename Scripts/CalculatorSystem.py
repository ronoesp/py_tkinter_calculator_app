import math
from decimal import Decimal
from CalculatorParameter import CalculatorParameter as cparam

class CalculatorSystem():
    @staticmethod
    
    def exponential_notation(data : str, limit : int):
        num = Decimal(data)
        
        # num = 0 の時は 0 を返す
        if(num == 0):
            return "0"
        elif(num == -0):
            return "0"
        else:
            return  str(f"{num:.{limit}g}")
    
    # 値が0か確認する
    def is_zero(data : str):
        num = Decimal(data)
        if(num == 0):
            return True
        return False
    
    # 値が負の値か確認する
    def is_minus(data : str):
        num = Decimal(data)
        if (num < 0):
            return True
        return False
    
    def err_msg_div_by_zero() -> str:
        return "0で割ることはできません"
    
    def err_msg_invalid_input() -> str:
        return "無効な入力です"
    
    # x(BackSpace)
    def back_space(data : str) -> str:
        if( len(data) > 0 ):
            result = data[:-1]
            if(result == "-0"):
                return "0"
            elif(result == "-"):
                return "0"
            elif(result == ""):
                return "0"
            else:
                return result
        else:
            return ""
    
    # .(小数点)
    def decimal_point(data : str) -> str:
        if("." in data):
            return  data
        else:
            return data + "."
        
    # 入力可能文字数を超えていないかチェック（整数値が実質0, "." , "-" は入力文字数に含めない）
    def check_num_limit(data : str, limit : int):

        check1 = int(Decimal(data)) == 0
        check2 = "." in data
        check3 = "-" in data
        
        if(check1):
            limit = limit + 1
        if(check2):
                limit = limit + 1
        if(check3):
            limit = limit + 1
        return len(data) < limit
    # def check_num_limit(data : str, limit : int):
    #     check0 = data.startswith("-0.")
    #     check1 = data.startswith("0.")
    #     check2 = "." in data
    #     check3 = "-" in data
        
    #     if(check0):
    #         limit = limit + 3
    #     elif(check1):
    #         limit = limit + 2
    #     else:
    #         if(check2):
    #             limit = limit + 1
    #         if(check3):
    #             limit = limit + 1
        
    #     return len(data) < limit
    
    # 0~9(number)
    def number( data : str, num_str : str, limit : int) -> str:
        if(not CalculatorSystem.check_num_limit(data, limit)):
            return data
        
        if(data == "0"):
            return num_str
        else:
            return data + num_str
    
    # CE
    def clear_enter(data : str):
        return "0"
    
    # ±（コマンド文字）
    def negate_str(data : str) -> str:
        return "negate( " + data + " )"
    
    # ±
    def negate(data : str) -> str:
        # -1をかけてない（0.0が-0.0になるから）
        # 先頭に-があれば消す、なければつける、が正しい処理
        if(data == "0"):
            return data
        else:
            if( data.startswith("-") ):
               return data[1:]
            else:
                return "-" + data
    
    # 1/X（コマンド文字）
    def reciprocal_str(data : str) -> str:
        return "1/( " + str(data) + " )"

    # 1/X
    def reciprocal(data : str) -> str:
        # dataが0ならエラー処理
        if(data == "0"):
            return "err"
        
        # 計算
        num = 1 / Decimal(data)
        return str(num.normalize())
    
    # X2（コマンド文字）
    def squared_str(data : str):
        return "sqr( " + str(data) + " )"
    
    # X2
    def squared(data : str) -> str:
        # 計算
        num = Decimal(data)
        num = num * num
        return str(num.normalize())
    
    # √（コマンド文字）
    def root_str(data : str) -> str:
        return "√( " + str(data) + " )"
    
    # √
    def root(data : str) -> str:
        # 計算
        num = math.sqrt(Decimal(data))
        num = Decimal(num)
        return str(num.normalize())
    
    # % (演算子が*/ならdataAを空欄にして使う)
    def percent(param : cparam) -> str:
        
        # 演算子*/の場合：dataB = dataB / 100
        # 演算子+-の場合：dataB = dataA * (dataB / 100)
        listA = ["*","/"]
        listB = ["+","-"]
        if(param.operator in listA):
            return str( Decimal(param.dataB) / 100 )
        elif(param.operator in listB):
            return str( Decimal(param.dataA) * (Decimal(param.dataB) / 100) )
        else:
            return ""
        
    # 四則演算
    def calculate(param : cparam) -> str:
        numA = Decimal(param.dataA)
        numB = Decimal(param.dataB)
        
        if(param.operator == "+"):
            return str( numA + numB )
        elif(param.operator == "-"):
            return str( numA - numB )
        elif(param.operator == "*"):
            return str( numA * numB )
        elif(param.operator == "/"):
            if(numB == 0):
                return "err"
            return str( numA / numB )
        else:
            return ""
        
    def format_custom(data = str, limit = int):
        # 1. まず小数点以下16桁の固定小数点で文字列にしてみる
        value = Decimal(data)
        s_fixed = f"{value:.{limit}f}"
        
        # 2. float(s_fixed) が元の値と同じなら「16桁以内で収まる（誤差なし）」と判断
        # ※ただし 0 のみ例外処理
        if float(s_fixed) == value or value == 0:
            # 末尾の無駄なゼロを消してきれいに整形
            return s_fixed.rstrip('0').rstrip('.') if '.' in s_fixed else s_fixed
        else:
            # 17桁目以降に値がある場合は、デフォルトの指数表記にする
            return str(value)