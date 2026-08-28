# inport===========================================================
import tkinter as tk
from functools import partial
from CalculatorManager import CalculatorManager as cmanager
from commons import Vector2
from commons import si2d_array
# =================================================================

class CalculatorGUI():
    def __init__(self):

        # 電卓関連情報
        self.err_lock_flg = False
        self.buttons = {}    #[]=配列、{}=辞書型
        self.names = [
                        ["%","CE","C","x"],
                        ["1/X","X2","√","/"],
                        ["7","8","9","*"],
                        ["4","5","6","-"],
                        ["1","2","3","+"],
                        ["±","0",".","="],
                     ]
        
        # 処理用クラスのインスタンス
        self.manager = cmanager()
        self.names_sercher = si2d_array()
        self.names_sercher.set_list(self.names)
        
    # ウィンドウの設定
    def __set_root(self):
        # ウィンドウ関連のインスタンス、基本設定値
        self.root = tk.Tk()
        self.root.title("電卓")
        self.root.geometry("500x500")
        self.root.maxsize(500,500)
        self.root.minsize(300,300)
        
# ディスプレイ===============================================================

    def __create_display_frame(self):
        # --- frame1（ディスプレイ全体の親枠） ---
        # ここで背景色(bg)を「白」にし、枠線(relief)を設定します。
        self.frame1 = tk.Frame(
            self.root, 
            bg="white",         # 背景を白に
            bd=2,               # 枠線の太さ
            relief=tk.SOLID     # 外枠を実線に
        )
        # 画面上部に少し余白（pady=10）を持って配置
        self.frame1.pack(fill=tk.X, padx=10, pady=10)
        
    def __create_display_label_top(self):
        
        # --- 状態管理用の変数（インスタンス変数にする） ---
        self.sub_str = tk.StringVar(value="123 + 456")  # 上段
        
        # --- 1. 上段ラベル（計算式など） ---
        self.label_top = tk.Label(
            self.frame1, 
            textvariable=self.sub_str,
            font=("Helvetica", 10),   # 少し小さめの文字
            bg="white",                # 背景を白に
            fg="gray",                 # 文字色をグレーにして控えめに
            anchor="e",                # 右寄せ
            padx=10,
            pady=5                     # 上下の隙間を少し狭く
        )
        # packのオプションで隙間(padx, pady)を「0」にして密着させる
        self.label_top.pack(fill=tk.X, padx=0, pady=0)
        
    def __create_display_label_bot(self):
        
        # --- 状態管理用の変数（インスタンス変数にする） ---
        self.main_str = tk.StringVar(value="579")        # 下段：結果用

        # --- 2. 下段ラベル（現在の入力値や結果） ---
        self.label_bottom = tk.Label(
            self.frame1, 
            textvariable=self.main_str,
            font=("Helvetica", 20, "bold"), # 大きく太い文字
            bg="white",                     # 背景を白に
            fg="black",                     # 文字色を黒に
            anchor="e",                     # 右寄せ
            padx=10,
            pady=5
        )
        # こちらも隙間「0」で密着させる
        self.label_bottom.pack(fill=tk.X, padx=0, pady=0)
        
    # ディスプレイ更新
    def __update_display(self):
        self.main_str.set(self.manager.create_message_main())
        self.sub_str.set(self.manager.create_message_sub())
        
    def __create_display(self):
        self.__create_display_frame()
        self.__create_display_label_top()
        self.__create_display_label_bot()
        self.__update_display()

# ==========================================================================

# ボタン=====================================================================

    def __create_buttons_frame(self):
        # --- frame2（ボタン全体の親枠） ---
        # ここで背景色(bg)を「白」にし、枠線(relief)を設定します。
        self.frame2 = tk.Frame(self.root, padx=10, pady=10)
        self.frame2.pack(fill=tk.BOTH, expand=True)
        
    def __set_button_extend(self):
        # ボタン列の伸縮設定
        col_length = len(self.names[0])
        for col in range(col_length):
            self.frame2.columnconfigure(col, weight=1)

        # ボタン行の伸縮設定
        start_row = 2   #ディスプレイ用ラベル2行分を追加
        row_length = len(self.names)
        for row in range(start_row, row_length + start_row, 1):
            self.frame2.rowconfigure(row, weight=1)
        
    def __layout_buttons(self):
        # ボタンの設定情報
        size = Vector2(4,1) # ボタンの縦横幅
        pad = Vector2(5,5)  # ボタン配置間隔
        
        # ボタン作成
        last_index = self.names_sercher.get_list_length()
        offset_row = 2  #ディスプレイ用ラベル2行分を追加
        
        for i in range(0, last_index):
            row = self.names_sercher.get_index_row(i)
            col = self.names_sercher.get_index_col(i)
            name = self.names_sercher.get_data(i)
            self.__create_button(row + offset_row, col, size, pad, name, name)
            
        # ボタンのパラメータ設定
        self.__set_button_param()
        
    # ボタンの作成
    def __create_button(self, row, col, size:Vector2, pad:Vector2, name:str, order:str):
        action = partial(self.__push_button, order)
        button = tk.Button(self.frame2, text = name, width = size.x, height = size.y, command = action)
        button.grid(row=row, column=col, sticky="nsew", padx=pad.x, pady=pad.y)
        self.buttons[name] = button
        
    # ボタンを押された時の処理
    def __push_button(self, order : str):
        self.manager.order = order
        self.manager.execution()    #電卓の内部処理実行
        self.__update_display()            #ディスプレイの更新
        self.__err_lock()                #エラー発生時、解除時の胥吏
        self.manager.order = ""
        
    # ボタンの設定
    def __set_button_param(self):
        groupA = ["0","1","2","3","4","5","6","7","8","9","±",".",]
        groupB = ["%","1/X","X2","√","+","-","*","/","CE","C","x"]
        groupC = ["="]
        
        colorA = "#EBFEFF"
        colorB = "#647879"
        colorC = "#0D05D9"
        black = "#000000"
        white = "#ffffff"
        
        state_code = "normal"
        state_relief = "raised"
        
        for name in groupA:
            self.buttons[name].config(state = state_code, bg = colorA, fg = black, relief = state_relief)
        for name in groupB:
            self.buttons[name].config(state = state_code, bg = colorB, fg = white, relief = state_relief)
        for name in groupC:
            self.buttons[name].config(state = state_code, bg = colorC, fg = white, relief = state_relief)
    
    # ボタンの色設定
    def __set_button_param_err(self):
        groupA = ["0","1","2","3","4","5","6","7","8","9"]
        groupB = ["CE","C","x"]
        groupC = ["="]
        groupE = ["%","1/X","X2","√","+","-","*","/","±","."]
        
        colorA = "#EBFEFF"
        colorB = "#647879"
        colorC = "#0D05D9"
        colorE = "#eeeeee"
        black = "#000000"
        white = "#ffffff"
        gray = "#aaaaaa"
        
        state_code = "normal"
        state_relief = "raised"
        state_code_err = "disabled"     # 押せない状態にする
        state_relief_err = "groove"     # 立体感をなくして平らにする
        
        for name in groupA:
            self.buttons[name].config(state = state_code, bg = colorA, fg = black, relief = state_relief)
        for name in groupB:
            self.buttons[name].config(state = state_code, bg = colorB, fg = white, relief = state_relief)
        for name in groupC:
            self.buttons[name].config(state = state_code, bg = colorC, fg = white, relief = state_relief)
        for name in groupE:
            self.buttons[name].config(state = state_code_err, bg = colorE, fg = gray, relief = state_relief_err)
    
    #エラー発生時、ボタンが押せないようロック＆見た目の修正
    def __err_lock(self):
        if(self.err_lock_flg == False and self.manager.phase == -1):
            self.__set_button_param_err()
            self.err_lock_flg = True
        elif(self.err_lock_flg == True and self.manager.phase != -1):
            self.__set_button_param()
            self.err_lock_flg = False
        
    def __create_buttons(self):
        self.__create_buttons_frame()
        self.__set_button_extend()
        self.__layout_buttons()
        
# ==========================================================================
    
    def main(self):
        self.__set_root()
        self.__create_display()
        self.__create_buttons()
        
        # GUIを動かす
        tk.mainloop()
        
calc_gui = CalculatorGUI()
calc_gui.main()