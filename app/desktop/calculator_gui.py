"""
電卓の画面クラス。

GuiParts でパーツを生成し、配置（pack/grid）と
CalculatorManager とのイベント連携だけを担当する。
見た目の値は GuiStyle 側に集約しているため、ここには色やフォントを書かない。
"""

import tkinter as tk

from calculator_manager import CalculatorManager as cmanager
from calculator_phase import Phase
from gui_parts import GuiParts
from gui_style import GuiStyle
from commons.vector2 import Vector2


class CalculatorGUI:

    # ボタンの並び（画面上の見た目そのままの2次元配列）
    BUTTON_NAMES = [
        ["%", "CE", "C", "x"],
        ["1/X", "X2", "√", "/"],
        ["7", "8", "9", "*"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["±", "0", ".", "="],
    ]

    # ボタンの役割分類（どのデザインを適用するかの判断に使う）
    ROLE_NUMBER = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "±", ".")
    ROLE_EQUAL = ("=",)
    # 上記以外はすべて ROLE_FUNCTION として扱う

    # エラー発生時でも操作を許可するボタン
    # （これ以外は押せないようロックする）
    ERROR_ENABLED = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "CE", "C", "x", "=")

    # ディスプレイ用ラベル2行分のオフセット
    DISPLAY_ROW_OFFSET = 2

    BUTTON_SIZE = Vector2(4, 1)   # ボタンの縦横幅
    BUTTON_PAD = Vector2(5, 5)    # ボタン配置間隔

    def __init__(self):
        self.err_lock_flg = False
        self.buttons = {}
        self.manager = cmanager()

    # ===========================================================
    # ディスプレイ
    # ===========================================================
    def __create_display(self):
        self.frame_display = GuiParts.create_display_frame(self.root)
        self.frame_display.pack(fill=tk.X, padx=10, pady=10)

        # 表示内容はmanagerから取得するため、初期値は空でよい
        self.sub_str = tk.StringVar()    # 上段：計算式用
        self.main_str = tk.StringVar()   # 下段：入力値・結果用

        self.label_sub = GuiParts.create_display_label_sub(self.frame_display, self.sub_str)
        self.label_sub.pack(fill=tk.X, padx=0, pady=0)

        self.label_main = GuiParts.create_display_label_main(self.frame_display, self.main_str)
        self.label_main.pack(fill=tk.X, padx=0, pady=0)

        self.__update_display()

    def __update_display(self):
        self.main_str.set(self.manager.create_message_main())
        self.sub_str.set(self.manager.create_message_sub())

    # ===========================================================
    # ボタン
    # ===========================================================
    def __create_buttons(self):
        self.frame_buttons = GuiParts.create_button_frame(self.root)
        self.frame_buttons.pack(fill=tk.BOTH, expand=True)

        self.__set_button_extend()
        self.__layout_buttons()
        self.__apply_button_theme()

    def __set_button_extend(self):
        """ウィンドウのリサイズに合わせてボタンが伸縮するよう設定する。"""
        # ボタン列の伸縮設定
        for col in range(len(self.BUTTON_NAMES[0])):
            self.frame_buttons.columnconfigure(col, weight=1)

        # ボタン行の伸縮設定
        start_row = self.DISPLAY_ROW_OFFSET
        for row in range(start_row, len(self.BUTTON_NAMES) + start_row):
            self.frame_buttons.rowconfigure(row, weight=1)

    def __layout_buttons(self):
        """2次元配列の並びどおりにボタンを生成・配置する。"""
        for row, row_names in enumerate(self.BUTTON_NAMES):
            for col, name in enumerate(row_names):
                button = GuiParts.create_button(
                    self.frame_buttons,
                    name=name,
                    order=name,
                    size=self.BUTTON_SIZE,
                    command=self.__push_button,
                )
                button.grid(
                    row=row + self.DISPLAY_ROW_OFFSET,
                    column=col,
                    sticky="nsew",
                    padx=self.BUTTON_PAD.x,
                    pady=self.BUTTON_PAD.y,
                )
                self.buttons[name] = button

    def __apply_button_theme(self, is_error: bool = False):
        """全ボタンにデザインを適用する。

        通常時とエラー時の違いは「エラー時はERROR_ENABLED以外が押せなくなる」
        という点だけなので、以前のように2つのメソッドに分けず1つにまとめている。
        """
        for name, button in self.buttons.items():
            if is_error and name not in self.ERROR_ENABLED:
                GuiStyle.apply_button_disabled(button)
            elif name in self.ROLE_NUMBER:
                GuiStyle.apply_button_number(button)
            elif name in self.ROLE_EQUAL:
                GuiStyle.apply_button_equal(button)
            else:
                GuiStyle.apply_button_function(button)

    def __push_button(self, order: str):
        """ボタンが押された時の処理。"""
        self.manager.order = order
        self.manager.execution()    # 電卓の内部処理実行
        self.__update_display()     # ディスプレイの更新
        self.__err_lock()           # エラー発生時、解除時の処理
        self.manager.order = ""

    def __err_lock(self):
        """エラー発生時、ボタンが押せないようロック＆見た目の修正。"""
        is_error = (self.manager.phase == Phase.ERROR)

        if not self.err_lock_flg and is_error:
            self.__apply_button_theme(is_error=True)
            self.err_lock_flg = True
        elif self.err_lock_flg and not is_error:
            self.__apply_button_theme(is_error=False)
            self.err_lock_flg = False

    # ===========================================================
    # 起動
    # ===========================================================
    def main(self):
        self.root = GuiParts.create_window()
        self.__create_display()
        self.__create_buttons()
        self.root.mainloop()