class CalculatorParameter:
    """計算のためのデータを一時保存するクラス。

    dataA / dataB      : 計算に使う実際の値（文字列として保持）
    dataA_str/dataB_str: ディスプレイ表示用の文字列
                         （"sqr( 5 )" のように命令の履歴が入ることがある）
    operator           : 演算子（+ - * /）
    result             : 計算結果
    """

    # formula() が返す状態パターン。
    # 分岐側で文字列リテラルを直接書くとタイプミスに気付けないため定数化する。
    FORMULA_A = "A"          # 左辺のみ
    FORMULA_A_EQ = "A="      # 左辺＋結果あり（＝を連続で押した状態）
    FORMULA_A_OP = "A:"      # 左辺＋演算子
    FORMULA_A_OP_B = "A:B"   # 左辺＋演算子＋右辺
    FORMULA_A_OP_B_EQ = "A:B="  # 上記＋結果あり

    def __init__(self):
        self.init_param()

    def init_param(self):
        self.dataA: str = "0"
        self.dataB: str = ""
        self.operator: str = ""
        self.result: str = ""
        self.dataA_str: str = ""
        self.dataB_str: str = ""

    def formula(self) -> str:
        """現在保持しているデータの組み合わせを文字列パターンで返す。

        どの値が埋まっているかによって、＝を押した時の計算方法が変わるため、
        その判定用に状態を文字列で表現している。
        """
        parts = []
        if self.dataA != "":
            parts.append("A")
        if self.operator != "":
            parts.append(":")
        if self.dataB != "":
            parts.append("B")
        if self.result != "":
            parts.append("=")

        return "".join(parts)

    def __repr__(self) -> str:
        """デバッグ用。print(param) で中身を一覧できるようにする。"""
        return (
            f"CalculatorParameter("
            f"dataA={self.dataA!r}, operator={self.operator!r}, dataB={self.dataB!r}, "
            f"result={self.result!r}, dataA_str={self.dataA_str!r}, dataB_str={self.dataB_str!r}, "
            f"formula={self.formula()!r})"
        )
