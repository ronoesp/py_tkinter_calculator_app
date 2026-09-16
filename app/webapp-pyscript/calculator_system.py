from decimal import Decimal

from calculator_parameter import CalculatorParameter as cparam


class CalculatorSystem:
    """電卓の数値演算・整形処理をまとめたステートレスなユーティリティクラス。

    インスタンス化はせず、CalculatorSystem.xxx() の形でクラス経由で呼び出す
    前提のため、全メソッドに @staticmethod を付与している。
    """

    # percent() で使う演算子分類（毎回リストを作らずクラス定数として保持）
    _MULTIPLICATIVE_OPERATORS = ("*", "/")
    _ADDITIVE_OPERATORS = ("+", "-")

    # ===========================================================
    # 値の判定
    # ===========================================================
    @staticmethod
    def is_zero(data: str) -> bool:
        """値が0か確認する。"""
        return Decimal(data) == 0

    @staticmethod
    def is_minus(data: str) -> bool:
        """値が負の値か確認する。"""
        return Decimal(data) < 0

    # ===========================================================
    # エラーメッセージ
    # ===========================================================
    @staticmethod
    def err_msg_div_by_zero() -> str:
        return "0で割ることはできません"

    @staticmethod
    def err_msg_invalid_input() -> str:
        return "無効な入力です"

    # ===========================================================
    # 入力チェック・整形
    # ===========================================================
    @staticmethod
    def check_num_limit(data: str, limit: int) -> bool:
        """入力可能文字数を超えていないかチェック
        （整数値が実質0, "." , "-" は入力文字数に含めない）。
        """
        check1 = int(Decimal(data)) == 0
        check2 = "." in data
        check3 = "-" in data

        if check1:
            limit = limit + 1
        if check2:
            limit = limit + 1
        if check3:
            limit = limit + 1
        return len(data) < limit

    @staticmethod
    def number(data: str, num_str: str, limit: int) -> str:
        """0〜9(number)"""
        if not CalculatorSystem.check_num_limit(data, limit):
            return data

        if data == "0":
            return num_str
        else:
            return data + num_str

    @staticmethod
    def decimal_point(data: str) -> str:
        """.(小数点)"""
        if "." in data:
            return data
        else:
            return data + "."

    @staticmethod
    def back_space(data: str) -> str:
        """x(BackSpace)"""
        if len(data) > 0:
            result = data[:-1]
            if result == "-0":
                return "0"
            elif result == "-":
                return "0"
            elif result == "":
                return "0"
            else:
                return result
        else:
            return ""

    @staticmethod
    def clear_enter(data: str) -> str:
        """CE"""
        return "0"

    # ===========================================================
    # 単項演算
    # ===========================================================
    @staticmethod
    def negate_str(data: str) -> str:
        """±（コマンド文字）"""
        return "negate( " + data + " )"

    @staticmethod
    def negate(data: str) -> str:
        """±
        -1をかけてない（0.0が-0.0になるから）。
        先頭に-があれば消す、なければつける、が正しい処理。
        """
        if data == "0":
            return data
        else:
            if data.startswith("-"):
                return data[1:]
            else:
                return "-" + data

    @staticmethod
    def reciprocal_str(data: str) -> str:
        """1/X（コマンド文字）"""
        return "1/( " + str(data) + " )"

    @staticmethod
    def reciprocal(data: str) -> str:
        """1/X"""
        # dataが0ならエラー処理
        if data == "0":
            return "err"

        num = 1 / Decimal(data)
        return str(num.normalize())

    @staticmethod
    def squared_str(data: str) -> str:
        """X2（コマンド文字）"""
        return "sqr( " + str(data) + " )"

    @staticmethod
    def squared(data: str) -> str:
        """X2"""
        num = Decimal(data)
        num = num * num
        return str(num.normalize())

    @staticmethod
    def root_str(data: str) -> str:
        """√（コマンド文字）"""
        return "√( " + str(data) + " )"

    @staticmethod
    def root(data: str) -> str:
        """√
        math.sqrt()はfloat経由になり精度が落ちるため、
        Decimal.sqrt()を使い誤差の混入を避ける。
        （呼び出し側で負の値は事前にチェックされている前提）
        """
        num = Decimal(data).sqrt()
        return str(num.normalize())

    # ===========================================================
    # 二項演算・結果表示の整形
    # ===========================================================
    @staticmethod
    def percent(param: cparam) -> str:
        """% (演算子が*/ならdataAを空欄にして使う)
        演算子*/の場合：dataB = dataB / 100
        演算子+-の場合：dataB = dataA * (dataB / 100)
        """
        if param.operator in CalculatorSystem._MULTIPLICATIVE_OPERATORS:
            return str(Decimal(param.dataB) / 100)
        elif param.operator in CalculatorSystem._ADDITIVE_OPERATORS:
            return str(Decimal(param.dataA) * (Decimal(param.dataB) / 100))
        else:
            return ""

    @staticmethod
    def calculate(param: cparam) -> str:
        """四則演算"""
        numA = Decimal(param.dataA)
        numB = Decimal(param.dataB)

        if param.operator == "+":
            return str(numA + numB)
        elif param.operator == "-":
            return str(numA - numB)
        elif param.operator == "*":
            return str(numA * numB)
        elif param.operator == "/":
            if numB == 0:
                return "err"
            return str(numA / numB)
        else:
            return ""

    @staticmethod
    def exponential_notation(data: str, limit: int) -> str:
        num = Decimal(data)

        # num = 0 の時は 0 を返す
        if num == 0:
            return "0"
        elif num == -0:
            return "0"
        else:
            return str(f"{num:.{limit}g}")

    @staticmethod
    def format_custom(data: str, limit: int) -> str:
        # 1. まず小数点以下 limit 桁の固定小数点表記にしてみる
        value = Decimal(data)
        s_fixed = f"{value:.{limit}f}"

        # 2. 固定小数点表記が元の値と一致するなら「limit桁以内で収まる（誤差なし）」と判断
        #    float()ではなくDecimal()同士で比較し、浮動小数点特有の誤差混入を避ける
        if Decimal(s_fixed) == value or value == 0:
            # 末尾の無駄なゼロを消してきれいに整形
            return s_fixed.rstrip('0').rstrip('.') if '.' in s_fixed else s_fixed
        else:
            # limit桁を超える場合は、デフォルトの指数表記にする
            return str(value)
