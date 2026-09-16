from decimal import Decimal
from CalculatorParameter import CalculatorParameter as cparam
from CalculatorSystem import CalculatorSystem as csystem
from commons.num_formatter import NumFormatter as nf

# ※時間があれば修正必須：dataA,dataBの値が実質0の場合、値を0にする処理を追加（変更箇所多そう…）
class CalculatorManager():
    def __init__(self):
        self.num_length_limit = 16
        self.param = cparam()
        self.init_status()
        self.init_order_lists()
    
    def init_status(self):
        self.phase = 0
        self.main_str = "0"
        self.sub_str = ""
        self.order = ""
        self.err_msg = ""
        
    def init_order_lists(self):
        self.orders_number = ["0","1","2","3","4","5","6","7","8","9"]
        self.orders_return_input_phase = ["0","1","2","3","4","5","6","7","8","9",".","CE"]
        self.orders_operator = ["+","-","/","*"]
        self.orders_ex_calc = ["1/X","X2","√","±","%"]
        
        # 分岐用に最適化していきたい（名称、要素など）
        self.create_num_orders = ["0","1","2","3","4","5","6","7","8","9",".","±","x"]
        self.result_order = ["="]
        self.clear_orders = ["C","CE"]
    
    # 表示用の文字が桁数を超えたら指数表記にする
    def e_n_str(self):
        # 左辺文字列の指数化チェック
        if(self.param.dataA_str == ""):
            pass
        elif("(" in self.param.dataA_str):
            pass
        elif(csystem.is_zero(self.param.dataA_str)):
            self.param.dataA_str = "0"
        elif(not csystem.check_num_limit(self.param.dataA_str, self.num_length_limit + 1)):
            self.param.dataA_str = csystem.exponential_notation(self.param.dataA_str, self.num_length_limit)
            
        # 右辺文字列の指数化チェック
        if(self.param.dataB_str == ""):
            pass
        elif("(" in self.param.dataB_str):
            pass
        elif(csystem.is_zero(self.param.dataB_str)):
            self.param.dataB_str = "0"
        elif(not csystem.check_num_limit(self.param.dataB_str, self.num_length_limit + 1)):
            self.param.dataB_str = csystem.exponential_notation(self.param.dataB_str, self.num_length_limit)
        # else:
        #     self.param.dataB_str = csystem.exponential_notation(self.param.dataB_str, self.num_length_limit)
        
    def create_message_main(self) -> str:
        if(self.main_str == ""):
            pass
        elif(not csystem.check_num_limit(self.main_str, self.num_length_limit + 1)):
            self.main_str = csystem.exponential_notation(self.main_str, self.num_length_limit)
        
        return self.main_str

    def create_message_sub(self) -> str:
        return self.sub_str
        
    def execution(self):
        # C（クリア）が実施されたら初期化して終了
        if(self.order == "C"):
            self.param.init_param()
            self.init_status()
            return
            
        is_execute = True   # 処理の分岐管理：フェーズ変更があったらもう一度実行させる
        safety_count = 4    #無限ループ防止用（起きたらバグなので修正しろ）
        
        
        # 分岐処理
        while is_execute:
            if(self.phase == 0):
                is_execute = self.phase0()
            elif(self.phase == 1):
                is_execute = self.phase1()
            elif(self.phase == 2):
                is_execute = self.phase2()
            elif(self.phase == 3):
                is_execute = self.phase3()
            elif(self.phase == 4):
                is_execute = self.phase4()
            elif(self.phase == 5):
                is_execute = self.phase5()
            elif(self.phase == 6):
                is_execute = self.phase6()
            elif(self.phase == 7):
                is_execute = self.phase7()
            elif(self.phase == -1):
                is_execute = self.phaseErr()
            
            # エラー発見用処理===============================
            safety_count = safety_count - 1
            if(safety_count <= 0):
                print(self.phase)
                print("フラグ変化による処理が実行されず無限ループしています")
                is_execute = False
            # エラー発見用処理===============================
            
# phase0===========================================================
    def phase0(self) -> bool:
        return self.phase0_change()
            
    # phase0から別のphaseに移動したらTrueを返す
    def phase0_change(self) -> bool:
        if(self.order in self.create_num_orders):
            self.phase = 1
            self.param.dataA = "0"
            self.param.dataA_str = ""
        elif(self.order in self.orders_ex_calc):
            self.phase = 2
            self.param.dataA = "0"
            self.param.dataA_str = "0"
        elif(self.order in self.orders_operator):
            self.phase = 3
            self.param.dataA = "0"
            self.param.dataA_str = "0"
            self.param.dataB = ""
        elif(self.order in self.result_order):
            self.phase = 7
            self.param.dataA = "0"
            self.param.dataA_str = "0"
        else:
            return False
        return True

# phase1===========================================================
    def phase1(self) -> bool:
        if(self.phase1_update()):
            return False
        elif(self.phase1_change()):
            return True
        else:
            return False
            
    # phase1の処理を実行
    def phase1_update(self) -> bool:
        if(self.order == "CE"):
            self.param.dataA = csystem.clear_enter(self.param.dataA)
        elif(self.order == "±"):
            self.param.dataA = csystem.negate(self.param.dataA)
        elif(self.order == "x"):
            self.param.dataA = csystem.back_space(self.param.dataA)
        elif(self.order == "."):
            self.param.dataA = csystem.decimal_point(self.param.dataA)
        elif(self.order in self.orders_number):
            self.param.dataA = csystem.number(self.param.dataA, self.order, self.num_length_limit)
        else:
            return False
        
        # ディスプレイ用の文字を更新
        self.phase1_display_str_update()
        return True
        
    def phase1_change(self) -> bool:
        if(self.order in self.orders_ex_calc):
            self.phase = 2
            self.param.dataA_str = self.param.dataA
        elif(self.order in self.orders_operator):
            self.phase = 3
            self.param.dataA_str = self.param.dataA
        elif(self.order in self.result_order):
            self.phase = 7
            self.param.dataA_str = self.param.dataA
        else:
            return False
        return True

    def phase1_display_str_update(self):
        self.e_n_str()
        self.sub_str = ""
        self.main_str = self.param.dataA
# ===========================================================


# phase2=====================================================
    def phase2(self) -> bool:
        if(self.phase2_update()):
            return False
        elif(self.phase2_change()):
            return True
        else:
            return False
        
    def phase2_update(self) -> bool:
        # 各ボタンの処理
        if(self.order == "1/X"):
            
            # サブディスプレイ用のコマンドには、1/xが実行されたことがわかるようにするため、必ず実行する
            self.param.dataA_str = csystem.reciprocal_str(self.param.dataA_str)
            
            if(csystem.is_zero(self.param.dataA)):
                self.order = "err"
                self.err_msg = csystem.err_msg_div_by_zero()
                return False    #Phase-1に変更するためFalseでPhaseChange関数を実行させる
            else:
                self.param.dataA = csystem.reciprocal(self.param.dataA)
                
        elif(self.order == "X2"):
            
            self.param.dataA = csystem.squared(self.param.dataA)
            self.param.dataA_str = csystem.squared_str(self.param.dataA_str)
            
        elif(self.order == "√"):
            
            if(csystem.is_minus(self.param.dataA)):
                self.order = "err"
                self.err_msg = csystem.err_msg_invalid_input()
                return False    #Phase-1に変更するためFalseでPhaseChange関数を実行させる
            else:
                self.param.dataA = csystem.root(self.param.dataA)
                self.param.dataA_str = csystem.root_str(self.param.dataA_str)

        elif(self.order == "±"):
            
            self.param.dataA = csystem.negate(self.param.dataA)
            self.param.dataA_str = csystem.negate_str(self.param.dataA_str)
            
        elif(self.order == "%"):
            
            # 左辺値に対して％を使用すると、値が0、サブ文字も0で上書きされる
            self.param.dataA = "0"
            self.param.dataA_str = "0"
            
        else:
            return False
        
        # ディスプレイ用の文字を更新
        self.phase2_display_str_update()
        return True
    
    def phase2_change(self) -> bool:
        if(self.order == "err"):
            self.phase2_display_str_update(self.err_msg)    #Phase-1でできそうならそっちでやらせる（ここのは消す）
            self.phase = -1
        elif(self.order in self.orders_return_input_phase):
            self.phase = 1
            self.param.dataA = "0"
        elif(self.order in self.orders_operator):
            self.phase = 3
            self.param.operator = ""
            self.param.dataB = "0"
            if(self.param.result != ""):
                self.param.dataA = self.param.result
                self.param.dataA_str = self.param.result
            
        elif(self.order == "="):
            self.phase = 7
        else:
            return False
        return True

    def phase2_display_str_update(self, err_message : str = ""):
        self.e_n_str()
        if(err_message != ""):
            self.main_str = err_message
        else:
            self.main_str = self.param.dataA
            
        self.sub_str = self.param.dataA_str
# ===========================================================
        
        
# phase3=====================================================
    def phase3(self) -> bool:
            if(self.phase3_update()):
                return False
            elif(self.phase3_change()):
                return True
            else:
                return False

    def phase3_update(self) -> bool:
        if(self.order == "+"):
            self.param.operator = "+"
        elif(self.order == "-"):
            self.param.operator = "-"
        elif(self.order == "*"):
            self.param.operator = "*"
        elif(self.order == "/"):
            self.param.operator = "/"
        else:
            return False
        
        # dataAの値が実質0なら0にする
        if(csystem.is_zero(self.param.dataA)):
            self.param.dataA = "0"
        
        # ディスプレイ用の文字を更新
        self.phase3_display_str_update()
        return True
    
    def phase3_change(self) -> bool:
        if(self.order in self.orders_return_input_phase):
            self.phase = 4
            self.param.dataB = "0"
            self.param.dataB_str = ""
        elif(self.order in self.orders_ex_calc):
            self.phase = 5
            self.param.dataB = self.param.dataA
            self.param.dataB_str = self.param.dataA
        elif(self.order == "="):
            self.phase = 7
            self.param.dataB = self.param.dataA
            self.param.dataB_str = self.param.dataA
        else:
            return False
        return True
    
    def phase3_display_str_update(self):
        self.e_n_str()
        
        self.main_str = self.param.dataA_str
        self.sub_str = self.param.dataA_str + " " + self.param.operator
# ===========================================================
        

# phase4===========================================================
    def phase4(self) -> bool:
        if(self.phase4_update()):
            return False
        elif(self.phase4_change()):
            return True
        else:
            return False
            
    def phase4_update(self) -> bool:
        if(self.order == "CE"):
            self.param.dataB = csystem.clear_enter(self.param.dataB)
        elif(self.order == "±"):
            self.param.dataB = csystem.negate(self.param.dataB)
        elif(self.order == "x"):
            self.param.dataB = csystem.back_space(self.param.dataB)
        elif(self.order == "."):
            self.param.dataB = csystem.decimal_point(self.param.dataB)
        elif(self.order in self.orders_number):
            self.param.dataB = csystem.number(self.param.dataB, self.order, self.num_length_limit)
        else:
            return False
        
        # ディスプレイ用の文字を更新
        self.phase4_display_str_update()
        return True
        
    def phase4_change(self) -> bool:
        if(self.order in self.orders_ex_calc):
            self.phase = 5
            self.param.dataB_str = self.param.dataB
        elif(self.order in self.orders_operator):
            self.phase = 6
        elif(self.order in self.result_order):
            self.phase = 7
            self.param.dataB_str = self.param.dataB
        else:
            return False
        return True

    def phase4_display_str_update(self):
        self.e_n_str()
        self.main_str = self.param.dataB
        self.sub_str = self.param.dataA_str + " " + self.param.operator
# ===========================================================


# phase5=====================================================
    def phase5(self) -> bool:
        if(self.phase5_update()):
            return False
        elif(self.phase5_change()):
            return True
        else:
            return False

    def phase5_update(self) -> bool:
        if(self.order == "1/X"):
            
            # サブディスプレイ用のコマンドには、1/xが実行されたことがわかるようにするため、必ず実行する
            self.param.dataB_str = csystem.reciprocal_str(self.param.dataB_str)
            
            if(csystem.is_zero(self.param.dataB)):
                self.order = "err"
                self.err_msg = csystem.err_msg_div_by_zero()
                return False    #Phase-1に変更するためFalseでPhaseChange関数を実行させる
            else:
                self.param.dataB = csystem.reciprocal(self.param.dataB)
                
        elif(self.order == "X2"):
            
            self.param.dataB = csystem.squared(self.param.dataB)
            self.param.dataB_str = csystem.squared_str(self.param.dataB_str)
            
        elif(self.order == "√"):
            
            if(csystem.is_minus(self.param.dataB)):
                self.order = "err"
                self.err_msg = csystem.err_msg_invalid_input()
                return False    #Phase-1に変更するためFalseでPhaseChange関数を実行させる
            else:
                self.param.dataB = csystem.root(self.param.dataB)
                self.param.dataB_str = csystem.root_str(self.param.dataB_str)

        elif(self.order == "±"):
            
            self.param.dataB = csystem.negate(self.param.dataB)
            self.param.dataB_str = csystem.negate_str(self.param.dataB_str)
            
        elif(self.order == "%"):
            
            self.param.dataB = csystem.percent(self.param)
            self.param.dataB_str = self.param.dataB
            
        else:
            return False
        
        # ディスプレイ用の文字を更新
        self.phase5_display_str_update()
        return True

    def phase5_change(self) -> bool:
        if(self.order == "err"):
            self.phase5_display_str_update(self.err_msg)    #Phase-1でできそうならそっちでやらせる（ここのは消す）
            self.phase = -1
        elif(self.order in self.orders_return_input_phase):
            self.phase = 4
            self.param.dataB = "0"
        elif(self.order in self.orders_operator):
            self.phase = 6
        elif(self.order == "="):
            self.phase = 7
        else:
            return False
        return True

    def phase5_display_str_update(self, err_message : str = ""):
        self.e_n_str()
        if(err_message != ""):
            self.main_str = err_message
        else:
            self.main_str = self.param.dataB
            
        self.sub_str = self.param.dataA_str + self.param.operator + self.param.dataB_str
# ===========================================================


# Phase6の処理完了後、Phase3に移行する
# phase6=====================================================
    def phase6(self) -> bool:
        self.phase6_update()
        self.phase6_change()
        return False
        
    def phase6_update(self):
        self.param.dataA = csystem.calculate(self.param)
        self.param.dataA_str = self.param.dataA
        
        # ↓（B処理）は不要かも？（確認できたら消す）
        self.param.dataB = ""
        self.param.dataB_str = self.param.dataB
        
        # ここで演算子を変更し、Whileは終了させる？
        self.param.operator = self.order
        
        # ディスプレイ用の文字を更新
        self.phase6_display_str_update()
        
    def phase6_change(self):
        self.phase = 3
        
    def phase6_display_str_update(self):
        self.e_n_str()
        self.normalize_str()
        
        self.main_str = self.param.dataA_str
        self.sub_str = self.param.dataA_str + " " + self.param.operator
# ===========================================================
        
        
# Phase7の処理完了後、Phase2に移行する（±を押した時の処理から、Phase1ではなくPhase2へ移行している）
# phase7=====================================================
    def phase7(self) -> bool:
        if(self.phase7_update()):
            return False
        elif(self.phase7_change()):
            return True
        else:
            return False

    def phase7_update(self) -> bool:
            
        fo_str = self.param.formula()
        
        if(self.order == "="):
            # =を押されたタイミングによる分岐処理
            if(fo_str == "A"):
                self.param.result = self.param.dataA
            elif(fo_str == "A="):
                self.param.dataA_str = self.param.result
            elif(fo_str == "A:"):
                self.param.dataB = self.param.dataA
                self.param.dataB_str = self.param.dataB
                self.param.result = csystem.calculate(self.param)
            elif(fo_str == "A:B"):
                self.param.result = csystem.calculate(self.param)
            elif(fo_str == "A:B="):
                self.param.dataA = self.param.result
                self.param.dataA_str = self.param.dataA
                self.param.dataB_str = self.param.dataB
                self.param.result = csystem.calculate(self.param)
            
            # 0除算が行われた場合、result = "err" となるので、エラー処理に移行させる
            if(self.param.result == "err"):
                self.order = "err"
                self.err_msg = csystem.err_msg_div_by_zero()
                return False
            
            # resultの値が実質0の時は常に0にする（指数表記を入れない）
            if(csystem.is_zero(self.param.result)):
                self.param.result = "0"
                
            # 16桁以内ならば指数表記から通常表記に戻す
            self.param.result = csystem.format_custom(self.param.result, self.num_length_limit + 1)
                        
            # ディスプレイ用の文字を更新
            self.phase7_display_str_update()
            return True
            
        elif(self.order == "x"):
            if(fo_str == "A:B="):
                self.main_str = self.param.result
                self.sub_str = ""
                return True
        else:
            return False
        
        
    def phase7_change(self) -> bool:
        if(self.order == "err"):
            self.phase7_display_str_update(self.err_msg)    #Phase-1でできそうならそっちでやらせる（ここのは消す）
            self.phase = -1
        else:
            self.phase = 2
            self.param.dataA = self.param.result
            self.param.dataA_str = self.param.result
            self.param.result = ""
        return True
        
    def phase7_display_str_update(self, err_message : str = ""):
        self.e_n_str()
        self.normalize_str()
        
        if(err_message != ""):
            self.main_str = err_message
        else:
            self.main_str = self.param.result
        
        if(self.param.dataB != ""):
            self.sub_str = self.param.dataA_str +" "+ self.param.operator +" "+ self.param.dataB_str +" "+ "="
        else:
            self.sub_str = self.param.dataA_str +" "+ "="
# ===========================================================


# phase-1====================================================
    def phaseErr(self) -> bool:
        if(self.order == "err"):
            return False
        
        # orderだけは初期化させないようにする
        order = self.order
        self.param.init_param()
        self.init_status()
        self.order = order
        
        if(self.order in self.orders_number):
            self.phase = 1
            return True
        else:
            # self.init_status() で self.phase = 0 となっている
            return False
# ===========================================================

    def normalize_str(self):
        # 空欄をnormalize_num関数に渡さないようにする（Decimal関数に空欄が渡されてエラーとなるため）
        if self.param.result != "":
            self.param.result = nf.normalize_num(self.param.result, self.num_length_limit)
        if self.param.dataA_str != "":
            self.param.dataA_str = nf.normalize_num(self.param.dataA_str, self.num_length_limit)
        if self.param.dataB_str != "":
            self.param.dataB_str = nf.normalize_num(self.param.dataB_str, self.num_length_limit)
        