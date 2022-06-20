"""dwmapi"""
import ctypes.wintypes

DWMWA_EXTENDED_FRAME_BOUNDS = 9


def DwmGetWindowAttribute(hwnd: int, flag: int) -> ctypes.wintypes.RECT:  # noqa # pylint: disable=invalid-name
    """
    DwmGetWindowAttribute

    :param hwnd: ウィンドウハンドル
    :param flag: フラグ
    :return: RECT
    """
    rect = ctypes.wintypes.RECT()
    ctypes.windll.dwmapi.DwmGetWindowAttribute(
        ctypes.wintypes.HWND(hwnd),
        ctypes.wintypes.DWORD(flag),
        ctypes.byref(rect),
        ctypes.sizeof(rect),
    )
    return rect
