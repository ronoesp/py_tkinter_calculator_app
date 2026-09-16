from decimal import Decimal


class NumFormatter():
    """数値の文字列表現を整える処理をまとめたクラス。

    Pythonで小数を扱うと自動で指数表記に変換されてしまう場合があるため、
    Decimalを使って値の正確さを保ちつつ、任意の桁数で
    「通常表記 ⇔ 指数表記」を相互に変換できるようにしている。
    """

    # ===========================================================
    # 表記の正規化（内部で使う小さな変換処理）
    # ===========================================================
    @staticmethod
    def _normalize_exponent_case(data: str) -> str:
        """指数を表すEが大文字なら小文字に変換する。"""
        return data.replace("E", "e")

    @staticmethod
    def _normalize_zero(data: str) -> str:
        """値が実質0なら"0"を返す。"""
        if Decimal(data) == 0:
            return "0"
        return data

    @staticmethod
    def _normalize_fractional(data: str) -> str:
        """小数の末尾に無駄な0があれば削除する。"""
        if "." in data:
            # 末尾の0を削り、その結果末尾が小数点になったらそれも削る
            return data.rstrip("0").rstrip(".")
        return data

    @staticmethod
    def _exponential_notation_to_num(data: str) -> str:
        """指数表記を通常表記に戻す。

        Decimalは "1.23e-8" のような指数表記の文字列をそのままパースできるため、
        符号(+/-)や指数部分を自前で計算する必要はない。
        """
        if "e" not in data:
            return data

        value = Decimal(data)
        return f"{value:f}"

    @staticmethod
    def _num_to_exponential_notation(data: str, limit: int) -> str:
        """通常表記の数値を、limit桁の有効数字で指数表記に変換する。

        limit桁に収まっているかどうかは「表示上の文字数」で判定する
        （0.0000000123... のような小数は、先頭の0も含めた文字数で判定するため、
        単純な有効数字の桁数とは異なる）。桁数の変換自体は、Decimalの
        'e' フォーマット指定子に任せることで、正しい四捨五入と繰り上がり
        （例: 9.999... → 1.0e+1）を保証している。
        """
        is_negative = data.startswith("-")
        abs_data = data[1:] if is_negative else data
        integer_part, _, fractional_part = abs_data.partition(".")

        # 表示上の文字数をカウントする（整数部が"0"のみの場合は数えない）
        digit_count = len(fractional_part)
        if integer_part != "0":
            digit_count += len(integer_part)

        if digit_count <= limit:
            return data

        # limit桁の有効数字に丸めて指数表記にする
        mantissa, exponent = f"{Decimal(data):.{limit - 1}e}".split("e")
        mantissa = NumFormatter._normalize_fractional(mantissa)
        return f"{mantissa}e{exponent}"

    # ===========================================================
    # 公開インターフェース
    # ===========================================================
    @staticmethod
    def normalize_num(data: str, limit: int) -> str:
        """数値文字列を正規化する。

        1. 指数のEを小文字に統一
        2. 実質0なら"0"にする
        3. 指数表記なら一旦通常表記に戻す
        4. 小数末尾の無駄な0を削る
        5. limit桁を超えていれば指数表記に変換する
        """
        data = NumFormatter._normalize_exponent_case(data)

        data = NumFormatter._normalize_zero(data)
        if data == "0":
            return data

        data = NumFormatter._exponential_notation_to_num(data)
        data = NumFormatter._normalize_fractional(data)
        data = NumFormatter._num_to_exponential_notation(data, limit)

        return data
