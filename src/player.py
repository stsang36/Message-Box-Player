import win32api
import win32con
import time
from message_box import geneate_msg_threaded
import random
import threading

CASCADE = (20, 20)

class Line:
    def __init__(self, wait_seconds: float, title: str, body: str, type_msg: str, icon: str):
        self.wait_seconds:float = wait_seconds
        self.title: str = title
        self.body:str = body
        self.type_msg:str = type_msg
        self.icon:str = icon


class Player:

    def __init__(self):
        self._spread_sheet_file: str = ""
        self._is_playing: bool = False
        self._current_x: int = 0
        self._current_y: int = 0
        self._music_sheet: list[Line] = []
        self._copy_of_music_sheet: list = []
        self._screen_width = win32api.GetSystemMetrics(0)
        self._screen_height = win32api.GetSystemMetrics(1)
        self._threads: list[threading.Thread] = []




    def __str__(self) -> str:
        return f"Player(spread_sheet_file={self._spread_sheet_file}, is_playing={self._is_playing}, current_x={self._current_x}, current_y={self._current_y}, music_sheet_length={len(self._music_sheet)})"

    def _parse_spread_sheet(self, file_path: str) -> list:
        music_sheet = []
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Expecting format: (wait_seconds, "Title", "Body", "Type", "Icon")
                    try:
                        parts = eval(line)
                        if len(parts) != 5:
                            print(f"Skipping invalid line (wrong number of elements): {line}")
                            continue
                        wait_seconds, title, body, type_msg, icon = parts
                        if not isinstance(wait_seconds, float) or not isinstance(title, str) or not isinstance(body, str) or not isinstance(type_msg, str) or not isinstance(icon, str):
                            print(f"Skipping invalid line (wrong types): {line}")
                            continue
                        music_sheet.append(Line(wait_seconds, title, body, type_msg, icon))
                    except Exception as e:
                        print(f"Error parsing line '{line}': {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found.")
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {e}")
        
        return music_sheet

    def load_music_sheet(self, file_path: str) -> None:
        self._music_sheet_file = file_path
        self._music_sheet = self._parse_spread_sheet(file_path)
        self._copy_of_music_sheet = self._music_sheet.copy()

    def is_empty(self) -> bool:
        if len(self._music_sheet) == 0:
            return True
        return False


    def pop(self) -> Line:
        if not self._music_sheet:
            raise ValueError("Music sheet is empty.")
        return self._music_sheet.pop(0)
    
    def reset(self) -> None:
        self._music_sheet = self._copy_of_music_sheet.copy()
        self._current_x = 0
        self._current_y = 0
        self._is_playing = False

    
    def play(self) -> None:
        if not self._music_sheet_file:
            raise ValueError("No spreadsheet file loaded.")
        
        print(f"Playing spreadsheet from {self._music_sheet_file}")

        self._is_playing = True


        while self._is_playing and not self.is_empty():
            line = self.pop()

            if line.wait_seconds == -1 and line.title.upper() == "RESET":
                print("Putting message box to random position on screen.")
                self._current_x = random.randint(0, self._screen_width - 200)
                self._current_y = random.randint(0, self._screen_height - 100)
                continue

            print(f"Displaying message box at position ({self._current_x}, {self._current_y}) with title '{line.title}'")
            t = threading.Thread(target=geneate_msg_threaded, args=(line.title, line.body, line.type_msg, line.icon, self._current_x, self._current_y, line.wait_seconds))
            
            t.start()
            self._threads.append(t)

            # if hit the edge of the screen, reset to 0 for respective axis
            if self._current_x + CASCADE[0] > self._screen_width - 200:
                self._current_x = 0
            else:
                self._current_x += CASCADE[0]
            
            if self._current_y + CASCADE[1] > self._screen_height - 100:
                self._current_y = 0
            else:
                self._current_y += CASCADE[1]
        
        # wait for all threads to finish
        for t in self._threads:
            t.join()
        self._is_playing = False
        print("Finished playing music sheet.")
        




'''
# music sheet should be denoted as:
# (wait_seconds, "Title", "Body", "Type", "Icon")
# RESET this will put a box to a random position on screen

# Example:
music_sheet = [
    (5, "Info", "This is an information message.", "MB_OK", "MB_ICONINFORMATION"),
    (3, "Warning", "This is a warning message.", "MB_OKCANCEL", "MB_ICONWARNING"),
    (4, "Error", "This is an error message.", "MB_RETRYCANCEL", "MB_ICONERROR"),
    (-1, "RESET", "", "", ""),  # Puts next message box to random position
    (2, "Question", "Do you want to continue?", "MB_YESNO", "MB_ICONQUESTION"),
]

'''

