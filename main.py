#!/usr/bin/env python3
"""ウィンドウの位置を設定に従って調整"""
import logging.config

import win32api
import win32com.client
import win32gui
import win32process
import yaml


class SetWinPos:
    logger = None

    def __init__(self):
        self.init_log()

    def main(self) -> None:
        self.logger.info("start")
        self.get_window_list()
        # self.test01()

    def get_window_list(self):
        def ttt(hwnd: int, _) -> bool:
            name: str = win32gui.GetWindowText(hwnd)
            clazz: str = win32gui.GetClassName(hwnd)
            _tid, pid = win32process.GetWindowThreadProcessId(hwnd)
            win32api.GetModuleFileNameW(hwnd)
            print(f"0x{hwnd:08x},{name},{clazz},{pid}")
            return True
        win32gui.EnumWindows(ttt, 0)

    def test01(self):
        wsh_shell = win32com.client.Dispatch("WScript.Shell")
        wsh_shell.Run("notepad.exe")

    def init_log(self):
        try:
            with open("log.yaml", "r", encoding="utf-8") as fh_yaml:
                data = yaml.load(fh_yaml, Loader=yaml.FullLoader)
        except FileNotFoundError as err:
            raise err
        logging.config.dictConfig(data)
        self.logger = logging.getLogger(__name__)


if __name__ == "__main__":
    SetWinPos().main()
