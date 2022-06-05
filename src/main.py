#!/usr/bin/env python3
"""ウィンドウの位置を設定に従って調整"""
import logging.config
from typing import List

import pywintypes
import win32api
import win32con
import win32gui
import win32process
import yaml

import windll_dwmapi
import windll_shcore


class SetWinPos:
    logger = None

    def __init__(self):
        self.init_log()

    def main(self) -> None:
        self.logger.info("start")
        self.get_window_list()

    def get_window_list(self):
        windll_shcore.SetProcessDpiAwareness(windll_shcore.PROCESS_PER_MONITOR_DPI_AWARE)

        def ttt(hwnd: int, handles: List[int]) -> bool:
            title: str = win32gui.GetWindowText(hwnd)
            clazz: str = win32gui.GetClassName(hwnd)
            # if name.startswith("neptune"):
            # if title.startswith("SetWinPos"):
            _tid, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False,
                                               pid)
            except pywintypes.error:  # noqa
                return True
            filename: str = win32process.GetModuleFileNameEx(process, 0)
            win32api.CloseHandle(process)
            # if filename.endswith("\\ttermpro.exe"):
            # if filename.endswith("\\pycharm64.exe"):
            if filename.endswith("\\Code.exe"):
                ss = win32gui.GetWindow(hwnd, win32con. GW_HWNDPREV)
                self.logger.info(ss)

                handles.append(hwnd)

                self.logger.debug(f"hwnd=0x{hwnd:08x},pid={pid:5d},title={title},class={clazz},filename={filename}")
                rect1 = win32gui.GetWindowRect(hwnd)
                self.logger.info("rect1:left=%d,top=%d,right=%d,bottom=%d", rect1[0], rect1[1], rect1[2], rect1[3])
                rect2 = windll_dwmapi.DwmGetWindowAttribute(hwnd, windll_dwmapi.DWMWA_EXTENDED_FRAME_BOUNDS)
                self.logger.info("rect2:left=%d,top=%d,right=%d,bottom=%d", rect2.left, rect2.top, rect2.right,
                                 rect2.bottom)
            return True

        window_handles = []
        win32gui.EnumWindows(ttt, window_handles)
        self.logger.info("hwnd=%08x", window_handles[0])

        # DwmSetWindowAttribute()での設定がうまく出来ないため、SetWindowPos()で代用する。
        # TODO: 拡大率が整数でないときに端数がおかしくなる？
        win32gui.SetWindowPos(window_handles[0], 0, 1610, 0, 3840 - 1610 + 11, 2114 + 11,
                              win32con.SWP_NOACTIVATE | win32con.SWP_NOZORDER)

        cx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        cy = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self.logger.info("metrics:cx=%d,cy=%d", cx, cy)

        for mon, _, _ in win32api.EnumDisplayMonitors():
            self.logger.info(f"mon={mon.handle}")
            info = win32api.GetMonitorInfo(mon.handle)
            self.logger.info(f"info={info['Work']}")

    def init_log(self):
        try:
            with open("conf/log.yaml", "r", encoding="utf-8") as fh_yaml:
                data = yaml.load(fh_yaml, Loader=yaml.FullLoader)
        except FileNotFoundError as err:
            raise err
        logging.config.dictConfig(data)
        self.logger = logging.getLogger(__name__)


if __name__ == "__main__":
    SetWinPos().main()
