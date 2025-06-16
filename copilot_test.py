import os
import platform
import time

def get_system_uptime():
    """
    Returns the system uptime in a human-readable format.
    Works on Linux, macOS, and Windows.
    """
    if platform.system() == 'Windows':
        # On Windows, use uptime from system boot time
        import ctypes
        import datetime

        class SYSTEM_TIME(ctypes.Structure):
            _fields_ = [
                ("wYear", ctypes.c_uint16),
                ("wMonth", ctypes.c_uint16),
                ("wDayOfWeek", ctypes.c_uint16),
                ("wDay", ctypes.c_uint16),
                ("wHour", ctypes.c_uint16),
                ("wMinute", ctypes.c_uint16),
                ("wSecond", ctypes.c_uint16),
                ("wMilliseconds", ctypes.c_uint16),
            ]

        class SYSTEM_INFO(ctypes.Structure):
            _fields_ = [
                ("dwOemId", ctypes.c_uint32),
                ("dwPageSize", ctypes.c_uint32),
                ("lpMinimumApplicationAddress", ctypes.c_void_p),
                ("lpMaximumApplicationAddress", ctypes.c_void_p),
                ("dwActiveProcessorMask", ctypes.c_void_p),
                ("dwNumberOfProcessors", ctypes.c_uint32),
                ("dwProcessorType", ctypes.c_uint32),
                ("dwAllocationGranularity", ctypes.c_uint32),
                ("wProcessorLevel", ctypes.c_uint16),
                ("wProcessorRevision", ctypes.c_uint16),
            ]

        # GetTickCount64 returns milliseconds since boot
        GetTickCount64 = ctypes.windll.kernel32.GetTickCount64
        GetTickCount64.restype = ctypes.c_ulonglong
        uptime_millis = GetTickCount64()
        uptime_seconds = uptime_millis // 1000

    elif platform.system() == 'Linux':
        # On Linux, read /proc/uptime
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
    elif platform.system() == 'Darwin':
        # On macOS, use sysctl
        import subprocess
        boot_time = subprocess.check_output(['sysctl', '-n', 'kern.boottime']).decode()
        import re
        match = re.search(r'{ sec = (\d+),', boot_time)
        if match:
            boot_time_sec = int(match.group(1))
            uptime_seconds = time.time() - boot_time_sec
        else:
            uptime_seconds = 0
    else:
        # Fallback for unknown systems
        uptime_seconds = 0

    # Convert seconds to days, hours, minutes, seconds
    days = int(uptime_seconds // (24 * 3600))
    hours = int((uptime_seconds % (24 * 3600)) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)

    return f"{days}d {hours}h {minutes}m {seconds}s"

if __name__ == "__main__":
    print("System Uptime:", get_system_uptime())
