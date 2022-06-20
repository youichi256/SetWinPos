"""shcore"""
import ctypes
from typing import Dict

PROCESS_PER_MONITOR_DPI_AWARE = 2
MDT_EFFECTIVE_DPI = 0


def SetProcessDpiAwareness(value: int) -> None:  # noqa # pylint: disable=invalid-name
    """
    SetProcessDpiAwareness

    :param value: PROCESS_DPI_AWARENESS
    :return: なし
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(value)


def GetDpiForMonitor(mon_handle: int, dpi_type: int) -> Dict[str, int]:  # noqa # pylint: disable=invalid-name
    """
    GetDpiForMonitor

    :param mon_handle: モニタハンドル
    :param dpi_type: タイプ
    :return: DPI情報
    """
    dpi_x = ctypes.c_uint()
    dpi_y = ctypes.c_uint()
    ctypes.windll.shcore.GetDpiForMonitor(mon_handle, dpi_type, ctypes.byref(dpi_x), ctypes.byref(dpi_y))
    return {"x": dpi_x.value, "y": dpi_y.value}
