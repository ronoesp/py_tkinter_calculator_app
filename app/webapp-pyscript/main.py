"""
PyScript版 電卓アプリの起動スクリプト。

計算ロジック本体（calculator_manager.py など）は一切変更していない。
このファイルが担うのは、元の calculator_gui.py / gui_parts.py / gui_style.py
が担っていた「画面の組み立てとイベント連携」の部分だけであり、
Tkinterの代わりにブラウザのDOM APIを直接Pythonから呼び出している。
"""

import sys
sys.path.insert(0, ".")  # pyscript.jsonで配置したファイルを確実にimportできるようにする

from pyscript import document
from pyodide.ffi import create_proxy

from calculator_manager import CalculatorManager
from calculator_phase import Phase


# ボタンの並び（元の calculator_gui.py の BUTTON_NAMES と同一）
BUTTON_NAMES = [
    ["%", "CE", "C", "x"],
    ["1/X", "X2", "\u221A", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["\u00B1", "0", ".", "="],
]

ROLE_NUMBER = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "\u00B1", "."]
ROLE_EQUAL = ["="]
ERROR_ENABLED = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "CE", "C", "x", "="]

manager = CalculatorManager()
button_els = {}
_event_proxies = []  # create_proxyで作ったプロキシがGCされないよう保持しておく

display_main = document.getElementById("display-main")
display_sub = document.getElementById("display-sub")
buttons_container = document.getElementById("buttons")


def update_display():
    display_main.textContent = manager.create_message_main()
    display_sub.textContent = manager.create_message_sub()


def apply_error_lock(is_error: bool):
    for name, btn in button_els.items():
        btn.disabled = bool(is_error and name not in ERROR_ENABLED)


def make_handler(order: str):
    """ボタン1つ分のクリックハンドラを作る（元の __push_button 相当）。"""

    def handler(event):
        manager.order = order
        manager.execution()
        update_display()
        apply_error_lock(manager.phase == Phase.ERROR)
        manager.order = ""

    return handler


def role_class(name: str) -> str:
    if name in ROLE_NUMBER:
        return "role-number"
    if name in ROLE_EQUAL:
        return "role-equal"
    return "role-function"


def build_buttons():
    for row in BUTTON_NAMES:
        for name in row:
            btn = document.createElement("button")
            btn.textContent = name
            btn.className = f"calc-btn {role_class(name)}"
            proxy = create_proxy(make_handler(name))
            _event_proxies.append(proxy)
            btn.addEventListener("click", proxy)
            button_els[name] = btn
            buttons_container.appendChild(btn)


build_buttons()
update_display()
