from win32api import MessageBox
import win32gui
import win32con
from enum import Enum
import threading
import time
from ctypes import windll


# Window procedure
try:
    windll.shcore.SetProcessDpiAwareness(1)  # System DPI aware
except Exception:
    windll.user32.SetProcessDPIAware()  # Fallback for older Windows


class MBIcon(Enum):
    ERROR = win32con.MB_ICONERROR
    QUESTION = win32con.MB_ICONQUESTION
    WARNING = win32con.MB_ICONWARNING
    INFORMATION = win32con.MB_ICONINFORMATION

class MBType(Enum):
    OK = win32con.MB_OK
    OKCANCEL = win32con.MB_OKCANCEL
    ABORTRETRYIGNORE = win32con.MB_ABORTRETRYIGNORE
    YESNOCANCEL = win32con.MB_YESNOCANCEL
    YESNO = win32con.MB_YESNO
    RETRYCANCEL = win32con.MB_RETRYCANCEL

class DefaultButton(Enum):
    '''Order of buttons: left to right, top to bottom'''
    BUTTON1 = win32con.MB_DEFBUTTON1
    BUTTON2 = win32con.MB_DEFBUTTON2
    BUTTON3 = win32con.MB_DEFBUTTON3
    BUTTON4 = win32con.MB_DEFBUTTON4


def generate_msg(title: str, body: str, type_msg: str, icon: str) -> None:
    # convert the type and icon from string to int

    type_int = getattr(win32con, type_msg)
    icon_int = getattr(win32con, icon)

    # Set the position of the message box
    
    MessageBox(
        0, body, title,
        icon_int | type_int | DefaultButton.BUTTON1.value
    )





def geneate_msg_threaded(title: str, body: str, type_msg: str, icon: str, x_pos:int, y_pos:int, abs_time: float) -> None:

    time.sleep(abs_time)
    try:
        thread = threading.Thread(target=generate_msg, args=(title, body, type_msg, icon))
        thread.start()
    except Exception as e:
        print(f"Error generating message box: {e}")

    hwnd = None
    c = 0
    while hwnd is None or c < 100:
        hwnd = win32gui.FindWindow("#32770", title)
        c += 1
        time.sleep(0.001)

    if hwnd:
        win32gui.SetWindowPos(hwnd, None, x_pos, y_pos, 0, 0,
                              win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE)
    else:
        print("Message box window not found.")

    vel = 5

    # make bounce on screen
    while True:
        hwnd = win32gui.FindWindow("#32770", title)
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]

            if rect[0] + width >= x_pos + 200 or rect[0] <= 0:
                vel = -vel

            win32gui.SetWindowPos(hwnd, None, rect[0] + vel, rect[1], 0, 0,
                                  win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE)
            time.sleep(0.01)
        else:
            break
    
