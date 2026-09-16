"""
GUIパーツのデザイン定義クラス（CSSのような役割）。

色・フォント・余白などの見た目に関する値をここに集約し、
apply_xxx(widget) の形で、引数で渡されたウィジェットに configure で適用する。

見た目を変えたい時はこのファイルだけを修正すればよく、
パーツクラスや画面クラスには手を入れずに済む。
"""

import tkinter as tk


class GuiStyle:
    # ===========================================================
    # カラーパレット
    # ===========================================================
    COLOR_NUMBER_BG = "#EBFEFF"      # 数字系ボタンの背景
    COLOR_FUNCTION_BG = "#647879"    # 記号・機能系ボタンの背景
    COLOR_EQUAL_BG = "#0D05D9"       # ＝ボタンの背景
    COLOR_DISABLED_BG = "#eeeeee"    # 無効化されたボタンの背景

    COLOR_BLACK = "#000000"
    COLOR_WHITE = "#ffffff"
    COLOR_GRAY = "#aaaaaa"
    COLOR_DISPLAY_BG = "#ffffff"
    COLOR_DISPLAY_SUB_FG = "gray"    # ディスプレイ上段（計算式）の文字色
    COLOR_DISPLAY_MAIN_FG = "#000000"

    # ===========================================================
    # フォント
    # ===========================================================
    FONT_DISPLAY_SUB = ("Helvetica", 10)
    FONT_DISPLAY_MAIN = ("Helvetica", 20, "bold")

    # ===========================================================
    # ウィジェットの状態（見た目）
    # ===========================================================
    STATE_NORMAL = "normal"
    STATE_DISABLED = "disabled"
    RELIEF_NORMAL = "raised"
    RELIEF_DISABLED = "groove"       # 立体感をなくして平らにする

    # ===========================================================
    # ウィンドウ
    # ===========================================================
    WINDOW_TITLE = "電卓"
    WINDOW_GEOMETRY = "500x500"
    WINDOW_MAX_SIZE = (500, 500)
    WINDOW_MIN_SIZE = (300, 300)

    # ===========================================================
    # 適用メソッド（引数のウィジェットをconfigureする）
    # ===========================================================
    @staticmethod
    def apply_window(root: tk.Tk):
        root.title(GuiStyle.WINDOW_TITLE)
        root.geometry(GuiStyle.WINDOW_GEOMETRY)
        root.maxsize(*GuiStyle.WINDOW_MAX_SIZE)
        root.minsize(*GuiStyle.WINDOW_MIN_SIZE)

    @staticmethod
    def apply_display_frame(frame: tk.Frame):
        """ディスプレイ全体の親枠。白背景＋実線の外枠。"""
        frame.configure(
            bg=GuiStyle.COLOR_DISPLAY_BG,
            bd=2,
            relief=tk.SOLID,
        )

    @staticmethod
    def apply_button_frame(frame: tk.Frame):
        frame.configure(padx=10, pady=10)

    @staticmethod
    def apply_display_label_sub(label: tk.Label):
        """ディスプレイ上段（計算式）。小さめ・グレーで控えめに。"""
        label.configure(
            font=GuiStyle.FONT_DISPLAY_SUB,
            bg=GuiStyle.COLOR_DISPLAY_BG,
            fg=GuiStyle.COLOR_DISPLAY_SUB_FG,
            anchor="e",
            padx=10,
            pady=5,
        )

    @staticmethod
    def apply_display_label_main(label: tk.Label):
        """ディスプレイ下段（現在の入力値や結果）。大きく太い文字。"""
        label.configure(
            font=GuiStyle.FONT_DISPLAY_MAIN,
            bg=GuiStyle.COLOR_DISPLAY_BG,
            fg=GuiStyle.COLOR_DISPLAY_MAIN_FG,
            anchor="e",
            padx=10,
            pady=5,
        )

    # --- ボタンの役割ごとの配色 -------------------------------
    @staticmethod
    def apply_button_number(button: tk.Button):
        button.configure(
            state=GuiStyle.STATE_NORMAL,
            bg=GuiStyle.COLOR_NUMBER_BG,
            fg=GuiStyle.COLOR_BLACK,
            relief=GuiStyle.RELIEF_NORMAL,
        )

    @staticmethod
    def apply_button_function(button: tk.Button):
        button.configure(
            state=GuiStyle.STATE_NORMAL,
            bg=GuiStyle.COLOR_FUNCTION_BG,
            fg=GuiStyle.COLOR_WHITE,
            relief=GuiStyle.RELIEF_NORMAL,
        )

    @staticmethod
    def apply_button_equal(button: tk.Button):
        button.configure(
            state=GuiStyle.STATE_NORMAL,
            bg=GuiStyle.COLOR_EQUAL_BG,
            fg=GuiStyle.COLOR_WHITE,
            relief=GuiStyle.RELIEF_NORMAL,
        )

    @staticmethod
    def apply_button_disabled(button: tk.Button):
        """押せない状態にし、立体感をなくして平らにする。"""
        button.configure(
            state=GuiStyle.STATE_DISABLED,
            bg=GuiStyle.COLOR_DISABLED_BG,
            fg=GuiStyle.COLOR_GRAY,
            relief=GuiStyle.RELIEF_DISABLED,
        )
