"""
GUIパーツの生成クラス（アトミックデザインでいう Atom に相当）。

「ウィジェットを生成し、GuiStyle でデザインを適用して返す」ことだけを担当する。
配置（pack/grid）は画面の都合によって変わるため、ここでは行わず画面クラスに任せる。
"""

import tkinter as tk
from functools import partial

from gui_style import GuiStyle
from commons.vector2 import Vector2


class GuiParts:

    # ===========================================================
    # ウィンドウ
    # ===========================================================
    @staticmethod
    def create_window() -> tk.Tk:
        root = tk.Tk()
        GuiStyle.apply_window(root)
        return root

    # ===========================================================
    # フレーム
    # ===========================================================
    @staticmethod
    def create_display_frame(parent) -> tk.Frame:
        frame = tk.Frame(parent)
        GuiStyle.apply_display_frame(frame)
        return frame

    @staticmethod
    def create_button_frame(parent) -> tk.Frame:
        frame = tk.Frame(parent)
        GuiStyle.apply_button_frame(frame)
        return frame

    # ===========================================================
    # ラベル
    # ===========================================================
    @staticmethod
    def create_display_label_sub(parent, text_var: tk.StringVar) -> tk.Label:
        """ディスプレイ上段（計算式表示用）。"""
        label = tk.Label(parent, textvariable=text_var)
        GuiStyle.apply_display_label_sub(label)
        return label

    @staticmethod
    def create_display_label_main(parent, text_var: tk.StringVar) -> tk.Label:
        """ディスプレイ下段（入力値・結果表示用）。"""
        label = tk.Label(parent, textvariable=text_var)
        GuiStyle.apply_display_label_main(label)
        return label

    # ===========================================================
    # ボタン
    # ===========================================================
    @staticmethod
    def create_button(parent, name: str, order: str, size: Vector2, command) -> tk.Button:
        """電卓のボタンを1つ生成して返す（配置は呼び出し側で行う）。

        command には押下時に呼ぶ関数を渡す。
        order（ボタンが表す命令）は partial で束縛して渡す。
        """
        action = partial(command, order)
        button = tk.Button(
            parent,
            text=name,
            width=size.x,
            height=size.y,
            command=action,
        )
        return button
