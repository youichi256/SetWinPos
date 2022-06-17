import ctypes
from typing import Dict

PROCESS_PER_MONITOR_DPI_AWARE = 2
MDT_EFFECTIVE_DPI = 0


def SetProcessDpiAwareness(value: int) -> int:  # noqa
    return ctypes.windll.shcore.SetProcessDpiAwareness(value)

def GetDpiForMonitor(mon_handle: int, dpi_type: int) -> Dict[str, int]:  # noqa
    dpi_x = ctypes.c_uint()
    dpi_y = ctypes.c_uint()
    ctypes.windll.shcore.GetDpiForMonitor(mon_handle, dpi_type, ctypes.byref(dpi_x), ctypes.byref(dpi_y))
    return {"x": dpi_x.value, "y": dpi_y.value}
