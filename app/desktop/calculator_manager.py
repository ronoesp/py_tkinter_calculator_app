import logging

from calculator_parameter import CalculatorParameter as cparam
from calculator_system import CalculatorSystem as csystem
from commons.num_formatter import NumFormatter as nf

from calculator_phase import Phase
from phase_handlers import (
    InitPhaseHandler,
    InputAPhaseHandler,
    ExCalcAPhaseHandler,
    OperatorPhaseHandler,
    InputBPhaseHandler,
    ExCalcBPhaseHandler,
    ChainCalcPhaseHandler,
    ResultPhaseHandler,
    ErrorPhaseHandler,
)

# ※時間があれば修正必須：dataA,dataBの値が実質0の場合、値を0にする処理を追加（変更箇所多そう…）


class CalculatorManager:
    """電卓の状態遷移を管理するクラス。

    各フェーズの実処理は phase_handlers.py 側の各ハンドラクラスに委譲し、
    ここでは「現在のフェーズに対応するハンドラを呼び出す」ことに専念する。
    """

    # 1回のexecution()呼び出しで発生しうるフェーズ遷移数の上限（無限ループ検知用）
    _MAX_TRANSITIONS = 4

    def __init__(self):
        self.num_length_limit = 16
        self.param = cparam()
        self.init_status()

        self._handlers = {
            Phase.INIT: InitPhaseHandler(self),
            Phase.INPUT_A: InputAPhaseHandler(self),
            Phase.EX_CALC_A: ExCalcAPhaseHandler(self),
            Phase.OPERATOR: OperatorPhaseHandler(self),
            Phase.INPUT_B: InputBPhaseHandler(self),
            Phase.EX_CALC_B: ExCalcBPhaseHandler(self),
            Phase.CHAIN_CALC: ChainCalcPhaseHandler(self),
            Phase.RESULT: ResultPhaseHandler(self),
            Phase.ERROR: ErrorPhaseHandler(self),
        }

    def init_status(self):
        self.phase = Phase.INIT
        self.main_str = "0"
        self.sub_str = ""
        self.order = ""
        self.err_msg = ""

    # 表示用の文字が桁数を超えたら指数表記にする
    def e_n_str(self):
        # 左辺文字列の指数化チェック
        if self.param.dataA_str == "":
            pass
        elif "(" in self.param.dataA_str:
            pass
        elif csystem.is_zero(self.param.dataA_str):
            self.param.dataA_str = "0"
        elif not csystem.check_num_limit(self.param.dataA_str, self.num_length_limit + 1):
            self.param.dataA_str = csystem.exponential_notation(self.param.dataA_str, self.num_length_limit)

        # 右辺文字列の指数化チェック
        if self.param.dataB_str == "":
            pass
        elif "(" in self.param.dataB_str:
            pass
        elif csystem.is_zero(self.param.dataB_str):
            self.param.dataB_str = "0"
        elif not csystem.check_num_limit(self.param.dataB_str, self.num_length_limit + 1):
            self.param.dataB_str = csystem.exponential_notation(self.param.dataB_str, self.num_length_limit)

    def create_message_main(self) -> str:
        # エラー状態ではmain_strに数値ではなくメッセージ文字列が入っているため、
        # 桁数チェック（Decimal変換）を行わずそのまま返す。
        # （ここをスキップしないと Decimal("無効な入力です") 等でエラーになる）
        if self.phase == Phase.ERROR:
            return self.main_str

        if self.main_str == "":
            pass
        elif not csystem.check_num_limit(self.main_str, self.num_length_limit + 1):
            self.main_str = csystem.exponential_notation(self.main_str, self.num_length_limit)
        return self.main_str

    def create_message_sub(self) -> str:
        return self.sub_str

    def execution(self):
        # C（クリア）が実施されたら初期化して終了
        if self.order == "C":
            self.param.init_param()
            self.init_status()
            return

        is_execute = True
        remaining = self._MAX_TRANSITIONS

        while is_execute:
            handler = self._handlers.get(self.phase)
            if handler is None:
                break
            is_execute = handler.execute()

            remaining -= 1
            if remaining <= 0:
                logging.warning(
                    "フェーズ %s でフラグ変化による処理が実行されず無限ループしています",
                    self.phase,
                )
                is_execute = False

    def normalize_str(self):
        # 空欄や"err"（エラーを表す内部値）をnormalize_num関数に渡さないようにする
        # （Decimal関数にこれらを渡すとエラーになるため）
        if self.param.result not in ("", "err"):
            self.param.result = nf.normalize_num(self.param.result, self.num_length_limit)
        if self.param.dataA_str != "":
            self.param.dataA_str = nf.normalize_num(self.param.dataA_str, self.num_length_limit)
        if self.param.dataB_str != "":
            self.param.dataB_str = nf.normalize_num(self.param.dataB_str, self.num_length_limit)
