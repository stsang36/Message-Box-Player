from player import Player
import os


def main():

    #get music sheet path
    music_sheet_path = os.path.join(os.path.dirname(__file__), "music_sheet.txt")

    player = Player()
    player.load_music_sheet(music_sheet_path)
    print(player)
    player.play()

if __name__ == "__main__":
    main()
