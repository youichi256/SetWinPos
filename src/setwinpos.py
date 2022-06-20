#!/usr/bin/env python3
"""ウィンドウの位置を設定に従って調整"""
import logging.config
import os
import re
from argparse import ArgumentParser, Namespace
from logging import Logger
from typing import List, Dict, Any

import pywintypes
import win32api
import win32con
import win32gui
import win32process
import yaml

import windll_dwmapi
import windll_shcore


class SetWinPos:
    """ウィンドウ位置設定"""

    def __init__(self):
        self.logger = self.init_log()
        self.display_primary = -1
        self.display: List[Dict[str, int]] = []
        self.winset: Dict[str, Dict[str, Any]] = {}

    def main(self) -> None:
        """
        メイン処理

        :return: なし
        """
        arg = self.argparse()
        self.logger.info("start")
        self.set_dpi_awareness()
        if arg.mode == "list":
            self.get_window_pos()
        if arg.mode == "set":
            self.get_display_info()
            self.load_setlist()
            self.set_window_pos()

    @staticmethod
    def argparse() -> Namespace:
        """
        引数解析

        :return: 引数情報
        """
        parser = ArgumentParser(description="ウィンドウ位置の調整")
        subparsers = parser.add_subparsers(dest="mode")
        subparsers.add_parser("list", help="ウィンドウ情報リスト")
        subparsers.add_parser("set", help="ウィンドウ座標設定")
        return parser.parse_args()

    @staticmethod
    def set_dpi_awareness() -> None:
        """
        高DPI設定

        :return: なし
        """
        # 高DPIでもオリジナルの座標で扱う
        windll_shcore.SetProcessDpiAwareness(windll_shcore.PROCESS_PER_MONITOR_DPI_AWARE)

    def get_window_pos(self) -> None:
        """
        ウィンドウ座標取得

        :return: なし
        """
        win32gui.EnumWindows(self.callback_enumwindows, False)

    def get_display_info(self) -> None:
        for mon, m2, m3 in win32api.EnumDisplayMonitors():
            # self.logger.info(f"mon={mon.__dir__()}")
            # self.logger.info(f"m2={m2.__dir__()}")
            # self.logger.info(f"m3={m3.__dir__()}")
            # print(m3.index)
            # print(m3.count)
            # self.logger.info(f"mon={mon.handle}")
            info = win32api.GetMonitorInfo(mon.handle)
            # self.logger.debug(f"info={info['Work']}")
            if info["Flags"] == 1:
                self.display_primary = len(self.display)
            self.display.append({
                "left": info["Work"][0],
                "top": info["Work"][1],
                "right": info["Work"][2],
                "bottom": info["Work"][3],
                "dpi": windll_shcore.GetDpiForMonitor(mon.handle, windll_shcore.MDT_EFFECTIVE_DPI)["x"],
            })
            # self.logger.debug(info)
            # print(windll_shcore.GetDpiForMonitor(mon.handle, windll_shcore.MDT_EFFECTIVE_DPI))
        self.logger.debug(self.display)

    def load_setlist(self):
        try:
            with open("conf/setlist.yaml", "r", encoding="utf-8") as fh_yaml:
                data: Dict[str, Dict[str, str]] = yaml.load(fh_yaml, Loader=yaml.FullLoader)
        except FileNotFoundError as err:
            raise err
        if not isinstance(data, dict):
            raise TypeError("setlistの構造が不正(all)")
        for name in data:
            data_name = data[name]
            if not isinstance(data_name, dict):
                raise TypeError(f"setlistの構造が不正({name})")
            filename = ""
            rect: Dict[str, int] = {}
            for key in data_name:
                data_key = data_name[key]
                if key == "title":
                    if not isinstance(data_key, str):
                        raise TypeError(f"setlistの値が不正({name},{key})")
                    # TODO: 未対応
                elif key == "class":
                    if not isinstance(data_key, str):
                        raise TypeError(f"setlistの値が不正({name},{key})")
                    # TODO: 未対応
                elif key == "filename":
                    if not isinstance(data_key, str):
                        raise TypeError(f"setlistの値が不正({name},{key})")
                    filename = data_key
                elif key == "display":
                    if not isinstance(data_key, int):
                        raise TypeError(f"setlistの値が不正({name},{key})")
                    # TODO: 未対応
                elif key in ["left", "top", "right", "bottom"]:
                    if isinstance(data_key, int):
                        rect[key] = data_key
                    elif isinstance(data_key, str):
                        match = re.search("^([0-9]+)%$", data_key)  # noqa
                        par = int(match.group(1))
                        if par > 100:
                            raise TypeError(f"setlistの値が不正({name},{key})")
                        rect[key] = int(self.display[self.display_primary][key] * par / 100)  # TODO: 計算方法検討
                    else:
                        raise TypeError(f"setlistの値が不正({name},{key})")
                else:
                    raise TypeError(f"setlistのキーが不正({name},{key})")
            if filename == "":
                raise TypeError(f"setlistの値が未設定({name},filename)")
            for key in ["left", "top", "right", "bottom"]:
                if key not in rect:
                    raise TypeError(f"setlistの値が未設定({name},{key})")
            if rect["right"] < rect["left"]:
                raise TypeError(f"rightがleftより小さい({name})")
            if rect["bottom"] < rect["top"]:
                raise TypeError(f"bottomがtopより小さい({name})")
            self.winset[name] = {
                "filename": filename,
                # "title": "",
                # "display": 0,
            }
            self.winset[name].update(rect)
        self.logger.debug(self.winset)

    def set_window_pos(self) -> None:
        """
        ウィンドウ座標設定

        :return: なし
        """

        # ee = win32print.EnumMonitors(None, 2)
        # print(ee)
        # # for idx in range(0, 4):
        #     disp0 = win32api.EnumDisplayDevices(None, idx)
        #     print("-----")
        #     print(f"display:{idx}")
        #     print(disp0.Size)
        #     print(disp0.DeviceName)
        #     print(disp0.DeviceString)
        #     print(disp0.StateFlags)
        #     print(disp0.DeviceID)
        #     print(disp0.DeviceKey)
        #     print(disp0.__dir__())

        win32gui.EnumWindows(self.callback_enumwindows, True)

        # cx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        # cy = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        # self.logger.info("metrics:cx=%d,cy=%d", cx, cy)

    def callback_enumwindows(self, hwnd: int, is_set: bool) -> bool:
        title: str = win32gui.GetWindowText(hwnd)
        clazz: str = win32gui.GetClassName(hwnd)
        _tid, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            process = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False,
                                           pid)
        except pywintypes.error:  # noqa
            return True
        filename: str = win32process.GetModuleFileNameEx(process, 0)
        win_visible = win32gui.IsWindowVisible(hwnd)
        win32api.CloseHandle(process)
        if win_visible == 1:
            rect1: List[int] = win32gui.GetWindowRect(hwnd)
            # self.logger.debug("rect1:left=%d,top=%d,right=%d,bottom=%d",
            #                   rect1[0], rect1[1], rect1[2], rect1[3])
            rect2 = windll_dwmapi.DwmGetWindowAttribute(hwnd, windll_dwmapi.DWMWA_EXTENDED_FRAME_BOUNDS)
            # self.logger.debug("rect2:left=%d,top=%d,right=%d,bottom=%d",
            #                   rect2.left, rect2.top, rect2.right, rect2.bottom)
            margin_left = int(str(rect2.left)) - rect1[0]
            margin_top = int(str(rect2.top)) - rect1[1]
            margin_right = rect1[2] - int(str(rect2.right)) + margin_left
            margin_bottom = rect1[3] - int(str(rect2.bottom)) + margin_top
            dpi = self.display[self.display_primary]["dpi"]
            if dpi % 96 >= 48 and margin_right > 0:
                # 拡大率が整数でないときの端数調整
                margin_right = margin_right + 1
                margin_bottom = margin_bottom + 1
            if is_set:
                for name, winset in self.winset.items():
                    if filename.endswith("\\" + winset["filename"]):
                        # ss = win32gui.GetWindow(hwnd, win32con.GW_HWNDPREV)
                        # self.logger.info(ss)

                        self.logger.debug(
                            "hwnd=0x%08x,pid=%05d,title=%s,filename=%s", hwnd, pid, title, filename)

                        self.logger.info("set:0x%08x,%s", hwnd, name)
                        win32gui.SetWindowPos(
                            hwnd, 0,
                            winset["left"] - margin_left,
                            winset["top"] - margin_top,
                            winset["right"] - winset["left"] + margin_right,
                            winset["bottom"] - winset["top"] + margin_bottom,
                            win32con.SWP_NOACTIVATE | win32con.SWP_NOZORDER)
            else:
                self.logger.debug(
                    "hwnd=0x%08x,pid=%05d,title=%s,class=%s,filename=%s", hwnd, pid, title, clazz, filename)

        return True

    @staticmethod
    def init_log() -> Logger:
        """
        ロガー初期化

        :return: ロガー
        """
        try:
            with open("conf/log.yaml", "r", encoding="utf-8") as fh_yaml:
                data = yaml.load(fh_yaml, Loader=yaml.FullLoader)
        except FileNotFoundError as err:
            raise err
        logging.config.dictConfig(data)
        return logging.getLogger(__name__)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__) + "/..")
    SetWinPos().main()
