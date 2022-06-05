import ctypes

PROCESS_PER_MONITOR_DPI_AWARE = 2


def SetProcessDpiAwareness(value: int) -> int:  # noqa
    return ctypes.windll.shcore.SetProcessDpiAwareness(value)
