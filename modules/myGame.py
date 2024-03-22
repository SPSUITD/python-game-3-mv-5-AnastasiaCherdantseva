import time
import arcade
import modules.characters as characters
import modules.WindowView as WindowView


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 850
SCREEN_TITLE = "Игра"

PLAYER_START_X = 1100
PLAYER_START_Y = 2100

TILE_SCALING = 0.5  #
GROW_RESOURCE_SCALING = 0.25  #

# позиция инвентаря
INVENTORY_X = 1150
INVENTORY_Y = 130
# позиция выбранного элемента инвентаря
INVENTORY_SELECTED_X = 1058
INVENTORY_SELECTED_Y = 130
INVENTORY_SELECTED_CHANGE_VALUE = 88

THOUGHT_TIME = 3

def interaction_button_draw(x, y):
    arcade.draw_circle_filled(
        x,
        y,
        12,
        [243, 229, 194]
    )
    arcade.draw_text(
        "e",
        x - 6,
        y - 5,
        arcade.csscolor.BROWN,
        12,
        0,
        'left',
        ("pix", 'arial'),
        True,
        True,

    )

class GrowResource(arcade.Sprite):
    def __init__(self, name,x,y, thisTime):
        super().__init__()
        self.path = name
        self.name = name
        self.cur_texture_anima = 0
        self.texture = arcade.load_texture(f"resources/img/view/game_resources/{name}/state_growth_1.png")
        self.hit_box = self.texture.hit_box_points
        self.center_x = x+2
        self.center_y = y+10
        self.scale = GROW_RESOURCE_SCALING
        self.textures_list = []
        self.texture_index = 0
        self.grow_time = thisTime
        self.texture_timing = time.time()
        # загружаем текстуры передвижения
        index = 1
        for i in range(1, 5):
            texture = arcade.load_texture(f"resources/img/view/game_resources/{name}/state_growth_{index}.png")
            self.textures_list.append(texture)
            index += 1
        if name != "apple":
            self.textures_list.append(arcade.load_texture(f"resources/img/view/game_resources/lunka.png"))


class MyGame(arcade.Window):  # класс окна

    #  конструктор
    def __init__(self):
        # обращаемся к конструктору главного класса и создаем окно с заданными параметрами
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # объект сцены. Сцена - инструмент для управления несколькими различными списками спрайтов путем присвоения каждому имени и поддержания порядка рисования.
        self.scene = None

        self.lunka_hit_list = None

        self.apple_hit_list = None
        #  спрайт игрока
        self.player_sprite = None

        self.inventory_sprite = None
        #  инициализация карты
        self.tile_map = None

        self.camera = None
        # камера для неподвижных элементов интерфейса
        self.gui_camera = None
        #  задний фон
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    #  запуск игры
    def setup(self):

        self.camera = arcade.Camera(self.width, self.height)  # камера

        self.gui_camera = arcade.Camera(self.width, self.height)

        self.scene = arcade.Scene()  # запуск новой сцены

        self.scene.add_sprite_list("Player")  # записываем в сцену пока пустой список спрайта игрока
        self.scene.add_sprite_list("Walls",
                                   use_spatial_hash=True)  # записываем в сцену пока пустой список спрайта объектов

        map_name = "resources/map_res/map.tmj"

        layer_options = {
            "water": {
                "use_spatial_hash": False,
                "hit_box_algorithm": "Simple",
            },
            "zabor": {
                "use_spatial_hash": False,
                "hit_box_algorithm": "Simple",
                "offset": (0, 0),
            },
            "ground": {
                # "hit_box_algorithm": "Simple",
            },
            "lunka": {
                "hit_box_algorithm": "Detailed"
            },
            "apple":{
                "hit_box_algorithm": "Detailed"
            }

        }
        # загружаем карту
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        for lunka in self.scene["lunka"]:
            lunka.isUsed = False
            lunka.resource = None

        for tree in self.scene["apple"]:
            tree.resource = GrowResource("apple", tree.center_x, tree.center_y, 2.0)

        self.player_sprite = characters.PlayerCharacter()

        self.player_sprite.center_x = PLAYER_START_X  # задаем изначальную позицию игрока по х
        self.player_sprite.center_y = PLAYER_START_Y  # задаем изначальную позицию игрока по у


        self.inventory_sprite = WindowView.WindowView("inventar.png", INVENTORY_X, INVENTORY_Y)
        self.inventory_selected_sprite = WindowView.WindowView("selected.png", INVENTORY_SELECTED_X,
                                                               INVENTORY_SELECTED_Y)

        self.scene.add_sprite(characters.LAYER_NAME_PLAYER,
                              self.player_sprite)  # добавляем спрайт игрока в лист игрока текущей сцены

        # подключение физики. 1 параметр - объект над котом работает физика, 2 - с чем работает его физика
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=0, walls=self.scene["water"]
        )

    def on_update(self, delta_time):  # покадровое обновление
        """Movement and game logic"""

        # обновление физики и перемещения объектов сцены
        self.physics_engine.update()

        self.lunka_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["lunka"]
        )
        self.apple_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["apple"]
        )

        self.inventory_sprite.update()
        self.inventory_selected_sprite.position_X = INVENTORY_SELECTED_X + 88* self.player_sprite.inventory_selected_index

        self.scene.update_animation(
            delta_time+3, [characters.LAYER_NAME_PLAYER, ]
        )
        # удаляем нулевые объекты инвентаря
        for res in self.player_sprite.inventory:
            if res.name != "null" and res.count == 0:
                self.player_sprite.inventory.append(characters.Resource("null", 0, res.index))
                self.player_sprite.inventory.remove(res)

        # рост лунок
        for lunka in self.scene["lunka"]:
            if lunka.isUsed and lunka.resource.texture_index != 3 and time.time() - lunka.resource.texture_timing > lunka.resource.grow_time:
                    lunka.resource.texture_timing = time.time()
                    lunka.resource.texture_index +=1
                    if lunka.resource.texture_index == 4: lunka.resource.texture_index = 0
                    lunka.texture = lunka.resource.textures_list[lunka.resource.texture_index]

        # рост яблок
        for tree in self.scene["apple"]:
            if tree.resource.texture_index != 3 and time.time() - tree.resource.texture_timing > tree.resource.grow_time:
                tree.resource.texture_timing = time.time()
                tree.resource.texture_index += 1
                if tree.resource.texture_index == 4 : tree.resource.texture_index = 0
                tree.texture = tree.resource.textures_list[tree.resource.texture_index]


        #следим за мыслями
        if time.time() - self.player_sprite.thought_timer > THOUGHT_TIME:
            self.player_sprite.thought_timer = time.time()
            self.player_sprite.thought = "weather"




        # Обновляем камеру
        self.center_camera_to_player()

    def process_keychange(self):
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = characters.PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -characters.PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = characters.PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -characters.PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    # отслеживание игрока по НАЖАТИЮ кнопки
    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.KEY_1:
            self.player_sprite.inventory_selected_index = 0
            self.inventory_selected_sprite.position_X = INVENTORY_SELECTED_X*self.player_sprite.inventory_selected_index

        if key == arcade.key.KEY_2:
            self.player_sprite.inventory_selected_index = 1
            self.inventory_selected_sprite.position_X = INVENTORY_SELECTED_X*self.player_sprite.inventory_selected_index

        if key == arcade.key.KEY_3:
            self.player_sprite.inventory_selected_index = 2
            self.inventory_selected_sprite.position_X = INVENTORY_SELECTED_X*self.player_sprite.inventory_selected_index


        if key == arcade.key.E:
            for lunka in self.lunka_hit_list:
                if not lunka.isUsed:
                    if (self.player_sprite.inventory[self.player_sprite.inventory_selected_index].name is not None
                    and "BackPack" in self.player_sprite.inventory[self.player_sprite.inventory_selected_index].state
                    and self.player_sprite.inventory[self.player_sprite.inventory_selected_index].count > 0):
                        lunka.isUsed = True
                        lunka.resource = GrowResource(self.player_sprite.inventory[self.player_sprite.inventory_selected_index].name,lunka.center_x,lunka.center_y, 5.0)
                        lunka.texture = lunka.resource.textures_list[0]
                        self.player_sprite.inventory[self.player_sprite.inventory_selected_index].count-=1
                    else:
                        self.player_sprite.thought = "не получится"
                        self.player_sprite.thought_timer = time.time()
                elif lunka.texture == lunka.resource.textures_list[3]:
                    lunka.texture = lunka.resource.textures_list[4]
                    lunka.isUsed = False
                    res_inventory_founded = False
                    for res in self.player_sprite.inventory:
                        if res.name == lunka.resource.name and res.state =="/product":
                            res.count+= 3
                            res_inventory_founded = True
                            break
                    if res_inventory_founded == False:
                        for res in self.player_sprite.inventory:
                            if res.name == "null":
                                self.player_sprite.inventory[res.index] = characters.Resource(lunka.resource.name, 3, res.index, "/product")
                                break
                else:
                    self.player_sprite.thought = "Еще не выросло.."
            for tree in self.apple_hit_list:
                if tree.texture == tree.resource.textures_list[3]:
                    tree.resource.texture_index = -1
                    res_inventory_founded = False
                    for res in self.player_sprite.inventory:
                        if res.name == tree.resource.name:
                            res.count += 3
                            res_inventory_founded = True
                            break
                    if res_inventory_founded == False:
                        for res in self.player_sprite.inventory:
                            if res.name == "null":
                                self.player_sprite.inventory[res.index] = characters.Resource(tree.resource.name, 3, res.index, "/product")
                                break
                else:
                    self.player_sprite.thought = "Еще не выросло.."



        self.process_keychange()

    # остановка игрока при ОТПУСКАНИИ кнопки
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = screen_center_x
        if screen_center_y < 0:
            screen_center_y = screen_center_y
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    # вся отрисовка здесь
    def on_draw(self):
        self.clear()  # очищаем старое

        self.camera.use()

        #  рисуем сцену

        self.scene.draw()

        for lunka in self.lunka_hit_list:
            interaction_button_draw(self.player_sprite.center_x - 50, self.player_sprite.center_y)

        for tree in self.apple_hit_list:
            interaction_button_draw(self.player_sprite.center_x - 50, self.player_sprite.center_y)


        if self.player_sprite.thought != "weather":
            self.player_sprite.thoughtWindow.position_X = self.player_sprite.center_x+90
            self.player_sprite.thoughtWindow.position_Y = self.player_sprite.center_y+60
            self.player_sprite.thoughtWindow.draw()
            self.player_sprite.thoughtWindow.draw_text(self.player_sprite.thought, self.player_sprite.thoughtWindow.position_X-60,self.player_sprite.thoughtWindow.position_Y)

        self.gui_camera.use()

        self.inventory_sprite.draw()
        self.inventory_selected_sprite.draw()

        for res in self.player_sprite.inventory:
            res.texture_view.draw()
            res.count_view.draw()
            if res.count != 0:
                if res.count < 10:
                    res.count_view.draw_text(str(res.count),res.count_view.position_X-5,res.count_view.position_Y-7)
                else:
                    res.count_view.draw_text(str(res.count),res.count_view.position_X-11,res.count_view.position_Y-7)

