#!/usr/bin/env python3
"""ウィンドウの位置を設定に従って調整"""
import ctypes.wintypes
import logging.config

import win32api
import win32con
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

    def get_window_list(self):
        def ttt(hwnd: int, ee: dict) -> bool:
            name: str = win32gui.GetWindowText(hwnd)
            # print(name)
            # if name.startswith("neptune"):
            if name.startswith("SetWinPos"):
                _tid, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False,
                                               pid)
                filename: str = win32process.GetModuleFileNameEx(process, 0)
                win32api.CloseHandle(process)
                self.logger.info(f"0x{hwnd:08x},{pid:5d},{name},{filename}")
                # if filename.endswith("\\ttermpro.exe"):
                if filename.endswith("\\pycharm64.exe"):
                    ee["ss"] = hwnd

                    rect1 = win32gui.GetWindowRect(hwnd)
                    self.logger.info("rect1:left=%d,top=%d,right=%d,bottom=%d", rect1[0], rect1[1], rect1[2], rect1[3])

                    f01 = ctypes.windll.dwmapi.DwmGetWindowAttribute
                    rect2 = ctypes.wintypes.RECT()
                    DWMWA_EXTENDED_FRAME_BOUNDS = 9
                    f01(ctypes.wintypes.HWND(hwnd),
                        ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
                        ctypes.byref(rect2),
                        ctypes.sizeof(rect2),
                        )
                    self.logger.info("rect2:left=%d,top=%d,right=%d,bottom=%d", rect2.left, rect2.top, rect2.right,
                                     rect2.bottom)
            return True

        uuu = {}
        win32gui.EnumWindows(ttt, uuu)
        self.logger.info("%08x", uuu['ss'])

        # win32gui.SetWindowPos(uuu['ss'], 0, 1073, 0, 2560-1073, 1409, win32con.SWP_NOACTIVATE | win32con.SWP_NOZORDER)

        cx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        cy = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self.logger.info("metrics:cx=%d,cy=%d", cx, cy)

        PROCESS_PER_MONITOR_DPI_AWARE = 2
        ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

        f02 = ctypes.windll.shcore.GetDpiForMonitor
        MDT_EFFECTIVE_DPI = 0
        dpiX = ctypes.c_uint()
        dpiY = ctypes.c_uint()

        for mon, _, _ in win32api.EnumDisplayMonitors():
            self.logger.info(f"mon={mon.handle}")
            info = win32api.GetMonitorInfo(mon.handle)
            f02(mon.handle, MDT_EFFECTIVE_DPI, ctypes.byref(dpiX), ctypes.byref(dpiY))
            self.logger.info(f"info={info['Work']},dpi={dpiX.value},{dpiY.value}")
        # win32gui.SystemParametersInfo()

    def init_log(self):
        try:
            with open("../conf/log.yaml", "r", encoding="utf-8") as fh_yaml:
                data = yaml.load(fh_yaml, Loader=yaml.FullLoader)
        except FileNotFoundError as err:
            raise err
        logging.config.dictConfig(data)
        self.logger = logging.getLogger(__name__)


if __name__ == "__main__":
    SetWinPos().main()
