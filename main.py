import arcade
import modules.myGame as myGame


def main():
    window = myGame.MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()