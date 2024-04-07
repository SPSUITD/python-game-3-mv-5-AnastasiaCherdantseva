import arcade
import modules.myGame as myGame

arcade.load_font("resources/fonts/pix.ttf")


def main():
    window = myGame.MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
