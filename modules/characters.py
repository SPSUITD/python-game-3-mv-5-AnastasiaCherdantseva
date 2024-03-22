import arcade
import modules.WindowView as WindowView

CHARACTER_SCALING = 2 # масштаб игрока

LAYER_NAME_PLAYER = "Lily"
PLAYER_MOVEMENT_SPEED = 5 # скорость игрока

RESOURCE_POSITION_START_X = 1058
RESOURCE_POSITION_START_Y = 135

class Resource:
    def __init__(self):
        self.texture_view = WindowView.WindowView("null.png", RESOURCE_POSITION_START_X,
                                                  RESOURCE_POSITION_START_Y)
        self.count_view = WindowView.WindowView("null.png", RESOURCE_POSITION_START_X,
                                                  RESOURCE_POSITION_START_Y)
        self.count = None
        self.isSelected = False

    def new(self,name,count):
        self.texture_view = WindowView.WindowView(f"game_resources/{name}.png", RESOURCE_POSITION_START_X,
                                                  RESOURCE_POSITION_START_Y)
        self.count_view = WindowView.WindowView("score.png", RESOURCE_POSITION_START_X + 30,
                                                RESOURCE_POSITION_START_Y - 25)
        self.count = count

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.inventory = [Resource(), Resource(), Resource()]
        self.inventory[0].new("wheat/BackPack",5)

        self.cur_texture_side = 0 #определяем сторону в которую смотрит игрок
        self.cur_texture_anima = 0 #определяем кадр анимации
        self.scale = CHARACTER_SCALING

        main_path = "resources/img/sprites/Lily_sprite/"  #  переменная в которой путь к спрайту игрока

        self.idle_texture_pair = arcade.load_texture(f"{main_path}1/1.png") #текстура в неподвижном состоянии

        self.walk_textures = [] #ТЕКСТУРЫ ПЕРЕДВИЖЕНИЯ
        #загружаем текстуры передвижения
        for i in range(1,5):
            texture = []
            for j in range(1,10):
                texture.append(arcade.load_texture(f"{main_path}{i}/{j}.png"))
            self.walk_textures.append(texture)


        self.texture = self.idle_texture_pair #задаем стартовую текстуру

        self.hit_box = self.texture.hit_box_points #задаем границы текстурам

    def update_animation(self, delta_time: float = 1 / 60):

        if self.change_x < 0:
            self.cur_texture_side = 1
        elif self.change_x > 0:
            self.cur_texture_side = 2
        elif self.change_y < 0:
            self.cur_texture_side = 0
        elif self.change_y > 0:
            self.cur_texture_side = 3

            #контролируем неподвижность персонажа
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair
            return

        self.cur_texture_anima += 1
        if self.cur_texture_anima > 8:
            self.cur_texture_anima = 0

        self.texture = self.walk_textures[self.cur_texture_side][self.cur_texture_anima]

