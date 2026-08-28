from decimal import Decimal

class NumFormatter():
    
    # 指数を表すeが大文字なら小文字に変換する
    def convert_e(data : str) -> str:
        if("E" in data):
            return data.replace("E", "e")
        else:
            return data
    
    # dataが実質0なら"0"が返る：normalize_numとかにする？(なら、少数以下の0も削る処理を加える？)
    def _normalize_zero(data : str) -> str:
        num = Decimal(data)
        if(num == 0):
            return "0"
        return data

    # 小数の末尾に無駄な0があれば削除する
    def _normalize_fractional(data :str) -> str:
        if '.' in data:
            return data.rstrip('0').rstrip('.') # 末尾の0を削り、その結果末尾が小数点になったらそれも削る
        else:
            return data

    # 指数表記を通常表記に戻す
    def _exponential_notation_to_num(data : str):
        
        if("e" in data):
            result = data.split("e")
            dataA = result[0]
            dataB = result[1][0]
            dataC = result[1][1:]
            ten_power = Decimal('10') ** Decimal(dataC)
            
            if(dataB == "+"):
                result = f"{Decimal(dataA) * ten_power:f}"
            elif(dataB == "-"):
                result = f"{Decimal(dataA) / ten_power:f}"
            else:
                return data
        else:
            return data
        return result

    @classmethod
    # 通常数値を指数表記に変換する
    def _num_to_exponential_notation(cls, data : str, limit : int):
        
        # 符号を記憶、数値から符号を外す
        is_negative = data.startswith("-")
        prefix = "-" if is_negative else ""
        abs_data = data[1:] if is_negative else data
        
        # 整数部と小数部に分ける（かつ小数点を消す）
        if "." in abs_data:
            integer_part, fractional_part = abs_data.split(".")
        else:
            integer_part, fractional_part = abs_data, ""
        
        # 1. 純粋な「数値の桁数」を正しくカウントする
        digit_count = 0
        if(integer_part != "0"):
            digit_count = digit_count + len(integer_part)
        digit_count = digit_count + len(fractional_part)

        # 桁数が limit 以下なら、そのまま返す
        if digit_count <= limit:
            return data
        
        # --- ここから制限を超えた場合の指数表記化プロセス ---
        # 2. 小数（1未満）の処理
        if integer_part == "0":

            # 最初の「0以外の数字」の位置を探す
            first_non_zero_index = -1
            for i, char in enumerate(fractional_part):
                if char != "0":
                    first_non_zero_index = i
                    break

            # 最期まで0ならそのままdataを返す
            if first_non_zero_index == -1:
                return data

            first_digit = fractional_part[first_non_zero_index]
            remaining_digits = fractional_part[first_non_zero_index + 1 :].rstrip("0")
            exponent = (first_non_zero_index + 1)
            sign = "-"

        # 3. 整数・1以上の数の処理
        else:
            first_digit = integer_part[0]
            remaining_digits = (integer_part[1:] + fractional_part).rstrip("0")
            exponent = len(integer_part) - 1
            sign = "+"
            
        # 4. 指数表記化して返す
        if remaining_digits:
            num_str = first_digit + "." + remaining_digits
            num_str = num_str[:limit + 1]
            num_str = cls._normalize_fractional(num_str)
            return f"{prefix}{num_str}e{sign}{exponent}"
        else:
            first_digit = first_digit[:limit]
            return f"{prefix}{first_digit}e{sign}{exponent}"
        
    @classmethod
    def normalize_num(cls, data : str, limit : int) -> str:
        # 指数を表すeが大文字なら小文字に変換する
        data = cls.convert_e(data)
        
        # 値が実質0であれば0に補正する
        data = cls._normalize_zero(data)
        if(data == "0"):
            return data
        
        # 指数表記なら、通常表記に戻す
        data = cls._exponential_notation_to_num(data)
        
        # 少数の末尾に無駄な0があれば削除する
        data = cls._normalize_fractional(data)
        
        # 指定桁数を超えていた場合、通常表記から指数表記に変換する
        data = cls._num_to_exponential_notation(data, limit)
        
        return data