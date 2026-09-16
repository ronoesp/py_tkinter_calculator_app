"""
電卓の各フェーズ(状態)の処理を担当するハンドラ群。

CalculatorManager が持っていた phase0〜phase7 / phaseErr の各メソッドを、
フェーズごとのクラスに分離したもの（Stateパターン）。

【共通の実行規約】
    execute() が True を返す = このフェーズ内で次のフェーズへ遷移した
                                （CalculatorManager側のwhileループが続行する）
    execute() が False を返す = このフェーズ内で入力を処理して留まった
                                 （whileループはここで終了する）

【A/B重複の解消】
    元のコードでは「左辺(A)の数値入力」(phase1)と「右辺(B)の数値入力」(phase4)、
    「左辺(A)への単項演算」(phase2)と「右辺(B)への単項演算」(phase5)が
    ほぼ同一のロジックを dataA/dataB それぞれに対して書いていたため、
    DataEntryHandler / ExCalcHandler という共通基底クラスを作り、
    getattr/setattr で対象フィールド名 (field_name) を切り替えることで
    重複を排除している。
"""

from abc import ABC, abstractmethod

from calculator_phase import Phase, Orders
from calculator_parameter import CalculatorParameter as cparam
from calculator_system import CalculatorSystem as csystem


class PhaseHandler(ABC):
    """各フェーズハンドラの基底クラス。"""

    def __init__(self, manager):
        self.manager = manager

    @property
    def param(self):
        return self.manager.param

    @property
    def order(self):
        return self.manager.order

    def execute(self) -> bool:
        if self._update():
            self._after_update()
            return False
        if self._change():
            return True
        return False

    def _after_update(self):
        """update後、共通で行いたい後処理があれば override する。"""
        pass

    @abstractmethod
    def _update(self) -> bool:
        """現在のフェーズ内での値更新。処理できたら True。"""
        raise NotImplementedError

    @abstractmethod
    def _change(self) -> bool:
        """次フェーズへの遷移判定。遷移したら True。"""
        raise NotImplementedError


# ===========================================================
# フェーズ0：初期状態
# ===========================================================
class InitPhaseHandler(PhaseHandler):
    """最初のボタン入力によってどのフェーズへ進むかを分岐する。"""

    def execute(self) -> bool:
        return self._change()

    def _update(self) -> bool:
        return False

    def _change(self) -> bool:
        param = self.param
        if self.order in Orders.CREATE_NUM:
            self.manager.phase = Phase.INPUT_A
            param.dataA = "0"
            param.dataA_str = ""
        elif self.order in Orders.EX_CALC:
            self.manager.phase = Phase.EX_CALC_A
            param.dataA = "0"
            param.dataA_str = "0"
        elif self.order in Orders.OPERATOR:
            self.manager.phase = Phase.OPERATOR
            param.dataA = "0"
            param.dataA_str = "0"
            param.dataB = ""
        elif self.order in Orders.RESULT:
            self.manager.phase = Phase.RESULT
            param.dataA = "0"
            param.dataA_str = "0"
        else:
            return False
        return True


# ===========================================================
# フェーズ1 / 4：数値入力中（A/Bで共通処理を持つ）
# ===========================================================
class DataEntryHandler(PhaseHandler):
    """数値入力中の共通処理。field_name をサブクラスで指定する。"""

    field_name: str = ""  # "dataA" または "dataB"

    def _value(self):
        return getattr(self.param, self.field_name)

    def _set_value(self, value):
        setattr(self.param, self.field_name, value)

    def _update(self) -> bool:
        order = self.order
        if order == "CE":
            self._set_value(csystem.clear_enter(self._value()))
        elif order == "±":
            self._set_value(csystem.negate(self._value()))
        elif order == "x":
            self._set_value(csystem.back_space(self._value()))
        elif order == ".":
            self._set_value(csystem.decimal_point(self._value()))
        elif order in Orders.NUMBER:
            self._set_value(csystem.number(self._value(), order, self.manager.num_length_limit))
        else:
            return False

        self._display_update()
        return True

    def _display_update(self):
        raise NotImplementedError


class InputAPhaseHandler(DataEntryHandler):
    """フェーズ1：左辺(A)の数値入力中。"""

    field_name = "dataA"

    def _change(self) -> bool:
        param = self.param
        if self.order in Orders.EX_CALC:
            self.manager.phase = Phase.EX_CALC_A
            param.dataA_str = param.dataA
        elif self.order in Orders.OPERATOR:
            self.manager.phase = Phase.OPERATOR
            param.dataA_str = param.dataA
        elif self.order in Orders.RESULT:
            self.manager.phase = Phase.RESULT
            param.dataA_str = param.dataA
        else:
            return False
        return True

    def _display_update(self):
        self.manager.e_n_str()
        self.manager.sub_str = ""
        self.manager.main_str = self.param.dataA


class InputBPhaseHandler(DataEntryHandler):
    """フェーズ4：右辺(B)の数値入力中。"""

    field_name = "dataB"

    def _change(self) -> bool:
        param = self.param
        if self.order in Orders.EX_CALC:
            self.manager.phase = Phase.EX_CALC_B
            param.dataB_str = param.dataB
        elif self.order in Orders.OPERATOR:
            self.manager.phase = Phase.CHAIN_CALC
        elif self.order in Orders.RESULT:
            self.manager.phase = Phase.RESULT
            param.dataB_str = param.dataB
        else:
            return False
        return True

    def _display_update(self):
        self.manager.e_n_str()
        self.manager.main_str = self.param.dataB
        self.manager.sub_str = f"{self.param.dataA_str} {self.param.operator}"


# ===========================================================
# フェーズ2 / 5：単項演算実行後（A/Bで共通処理を持つ）
# ===========================================================
class ExCalcHandler(PhaseHandler):
    """単項演算（1/X, X2, √, ±, %）の共通処理。"""

    field_name: str = ""      # "dataA" または "dataB"
    str_field_name: str = ""  # "dataA_str" または "dataB_str"

    def _value(self):
        return getattr(self.param, self.field_name)

    def _set_value(self, value):
        setattr(self.param, self.field_name, value)

    def _str_value(self):
        return getattr(self.param, self.str_field_name)

    def _set_str_value(self, value):
        setattr(self.param, self.str_field_name, value)

    def _update(self) -> bool:
        order = self.order

        if order == "1/X":
            # サブディスプレイ用に、1/xが実行されたことがわかる文字列は必ず更新する
            self._set_str_value(csystem.reciprocal_str(self._str_value()))
            if csystem.is_zero(self._value()):
                self.manager.order = "err"
                self.manager.err_msg = csystem.err_msg_div_by_zero()
                return False
            self._set_value(csystem.reciprocal(self._value()))

        elif order == "X2":
            self._set_value(csystem.squared(self._value()))
            self._set_str_value(csystem.squared_str(self._str_value()))

        elif order == "√":
            if csystem.is_minus(self._value()):
                self.manager.order = "err"
                self.manager.err_msg = csystem.err_msg_invalid_input()
                return False
            self._set_value(csystem.root(self._value()))
            self._set_str_value(csystem.root_str(self._str_value()))

        elif order == "±":
            self._set_value(csystem.negate(self._value()))
            self._set_str_value(csystem.negate_str(self._str_value()))

        elif order == "%":
            self._on_percent()

        else:
            return False

        self._display_update()
        return True

    def _on_percent(self):
        """%押下時の処理。A/Bで挙動が異なるためサブクラスで実装する。"""
        raise NotImplementedError

    def _display_update(self, err_message: str = ""):
        raise NotImplementedError


class ExCalcAPhaseHandler(ExCalcHandler):
    """フェーズ2：左辺(A)への単項演算実行後。"""

    field_name = "dataA"
    str_field_name = "dataA_str"

    def _on_percent(self):
        # 左辺値に対して％を使用すると、値が0、サブ文字も0で上書きされる
        self.param.dataA = "0"
        self.param.dataA_str = "0"

    def _change(self) -> bool:
        param = self.param
        if self.order == "err":
            self._display_update(self.manager.err_msg)
            self.manager.phase = Phase.ERROR
        elif self.order in Orders.RETURN_TO_INPUT:
            self.manager.phase = Phase.INPUT_A
            param.dataA = "0"
        elif self.order in Orders.OPERATOR:
            self.manager.phase = Phase.OPERATOR
            param.operator = ""
            param.dataB = "0"
            if param.result != "":
                param.dataA = param.result
                param.dataA_str = param.result
        elif self.order == "=":
            self.manager.phase = Phase.RESULT
        else:
            return False
        return True

    def _display_update(self, err_message: str = ""):
        self.manager.e_n_str()
        self.manager.main_str = err_message if err_message else self.param.dataA
        self.manager.sub_str = self.param.dataA_str


class ExCalcBPhaseHandler(ExCalcHandler):
    """フェーズ5：右辺(B)への単項演算実行後。"""

    field_name = "dataB"
    str_field_name = "dataB_str"

    def _on_percent(self):
        self.param.dataB = csystem.percent(self.param)
        self.param.dataB_str = self.param.dataB

    def _change(self) -> bool:
        if self.order == "err":
            self._display_update(self.manager.err_msg)
            self.manager.phase = Phase.ERROR
        elif self.order in Orders.RETURN_TO_INPUT:
            self.manager.phase = Phase.INPUT_B
            self.param.dataB = "0"
        elif self.order in Orders.OPERATOR:
            self.manager.phase = Phase.CHAIN_CALC
        elif self.order == "=":
            self.manager.phase = Phase.RESULT
        else:
            return False
        return True

    def _display_update(self, err_message: str = ""):
        self.manager.e_n_str()
        self.manager.main_str = err_message if err_message else self.param.dataB
        self.manager.sub_str = self.param.dataA_str + self.param.operator + self.param.dataB_str


# ===========================================================
# フェーズ3：演算子（+ - * /）選択後
# ===========================================================
class OperatorPhaseHandler(PhaseHandler):
    """フェーズ3：演算子選択後。"""

    def _update(self) -> bool:
        if self.order not in Orders.OPERATOR:
            return False

        self.param.operator = self.order

        # dataAの値が実質0なら0にする
        if csystem.is_zero(self.param.dataA):
            self.param.dataA = "0"

        self._display_update()
        return True

    def _change(self) -> bool:
        param = self.param
        if self.order in Orders.RETURN_TO_INPUT:
            self.manager.phase = Phase.INPUT_B
            param.dataB = "0"
            param.dataB_str = ""
        elif self.order in Orders.EX_CALC:
            self.manager.phase = Phase.EX_CALC_B
            param.dataB = param.dataA
            param.dataB_str = param.dataA
        elif self.order == "=":
            self.manager.phase = Phase.RESULT
            param.dataB = param.dataA
            param.dataB_str = param.dataA
        else:
            return False
        return True

    def _display_update(self):
        self.manager.e_n_str()
        self.manager.main_str = self.param.dataA_str
        self.manager.sub_str = f"{self.param.dataA_str} {self.param.operator}"


# ===========================================================
# フェーズ6：連続演算（演算子を続けて押した場合の中間計算）
# 処理完了後は必ずフェーズ3へ遷移する
# ===========================================================
class ChainCalcPhaseHandler(PhaseHandler):
    """フェーズ6：連続演算。

    元の実装同様、このフェーズは1回のexecution()呼び出し内で
    計算とフェーズ3への遷移を完了させるが、あえて execute() は False を返し、
    フェーズ3の処理は次回のボタン入力（次のexecution()呼び出し）に委ねる。
    """

    def execute(self) -> bool:
        self._update()
        self._change()
        return False

    def _update(self) -> bool:
        param = self.param
        param.dataA = csystem.calculate(param)
        param.dataA_str = param.dataA

        # ↓（B処理）は不要かも？（確認できたら消す）
        param.dataB = ""
        param.dataB_str = param.dataB

        param.operator = self.order

        self._display_update()
        return True

    def _change(self) -> bool:
        self.manager.phase = Phase.OPERATOR
        return True

    def _display_update(self):
        self.manager.e_n_str()
        self.manager.normalize_str()
        self.manager.main_str = self.param.dataA_str
        self.manager.sub_str = f"{self.param.dataA_str} {self.param.operator}"


# ===========================================================
# フェーズ7：＝（結果表示）
# 処理完了後はフェーズ2へ遷移する
# （±を押した時の処理から、フェーズ1ではなくフェーズ2へ移行している点に注意）
# ===========================================================
class ResultPhaseHandler(PhaseHandler):
    """フェーズ7：結果表示。"""

    def _update(self) -> bool:
        formula = self.param.formula()

        if self.order == "=":
            return self._on_equal(formula)
        elif self.order == "x":
            if formula == cparam.FORMULA_A_OP_B_EQ:
                self.manager.main_str = self.param.result
                self.manager.sub_str = ""
                return True
            return False
        else:
            return False

    def _on_equal(self, formula: str) -> bool:
        param = self.param

        # =を押されたタイミングによる分岐処理
        if formula == cparam.FORMULA_A:
            param.result = param.dataA
        elif formula == cparam.FORMULA_A_EQ:
            param.dataA_str = param.result
        elif formula == cparam.FORMULA_A_OP:
            param.dataB = param.dataA
            param.dataB_str = param.dataB
            param.result = csystem.calculate(param)
        elif formula == cparam.FORMULA_A_OP_B:
            param.result = csystem.calculate(param)
        elif formula == cparam.FORMULA_A_OP_B_EQ:
            param.dataA = param.result
            param.dataA_str = param.dataA
            param.dataB_str = param.dataB
            param.result = csystem.calculate(param)

        # 0除算が行われた場合、result = "err" となるので、エラー処理に移行させる
        if param.result == "err":
            self.manager.order = "err"
            self.manager.err_msg = csystem.err_msg_div_by_zero()
            return False

        # resultの値が実質0の時は常に0にする（指数表記を入れない）
        if csystem.is_zero(param.result):
            param.result = "0"

        # 桁数以内ならば指数表記から通常表記に戻す
        param.result = csystem.format_custom(param.result, self.manager.num_length_limit + 1)

        self._display_update()
        return True

    def _change(self) -> bool:
        param = self.param
        if self.order == "err":
            self._display_update(self.manager.err_msg)
            self.manager.phase = Phase.ERROR
        else:
            self.manager.phase = Phase.EX_CALC_A
            param.dataA = param.result
            param.dataA_str = param.result
            param.result = ""
        return True

    def _display_update(self, err_message: str = ""):
        self.manager.e_n_str()
        self.manager.normalize_str()
        param = self.param

        self.manager.main_str = err_message if err_message else param.result

        if param.dataB != "":
            self.manager.sub_str = f"{param.dataA_str} {param.operator} {param.dataB_str} ="
        else:
            self.manager.sub_str = f"{param.dataA_str} ="


# ===========================================================
# フェーズ-1：エラー状態
# ===========================================================
class ErrorPhaseHandler(PhaseHandler):
    """次の入力でエラー表示をクリアする。"""

    def execute(self) -> bool:
        return self._change()

    def _update(self) -> bool:
        return False

    def _change(self) -> bool:
        if self.order == "err":
            return False

        # orderだけは初期化させないようにする
        order = self.order
        self.param.init_param()
        self.manager.init_status()
        self.manager.order = order

        if self.order in Orders.NUMBER:
            self.manager.phase = Phase.INPUT_A
            return True
        # init_status() で phase = INIT となっている
        return False
