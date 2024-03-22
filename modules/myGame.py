import arcade
import modules.characters as characters
import modules.WindowView as WindowView

SCREEN_WIDTH=1400
SCREEN_HEIGHT=850
SCREEN_TITLE="Игра"

PLAYER_START_X = 1100
PLAYER_START_Y = 2100

TILE_SCALING = 0.5 # масштаб спрайта игрока

#позиция инвентаря
INVENTORY_X = 1150
INVENTORY_Y = 130
#позиция выбранного элемента инвентаря
INVENTORY_SELECTED_X = 1058
INVENTORY_SELECTED_Y = 130
INVENTORY_SELECTED_CHANGE_VALUE = 88
class MyGame(arcade.Window): # класс окна

   #  конструктор
    def __init__(self):
        # обращаемся к конструктору главного класса и создаем окно с заданными параметрами
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        #объект сцены. Сцена - инструмент для управления несколькими различными списками спрайтов путем присвоения каждому имени и поддержания порядка рисования.
        self.scene = None
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

        self.camera = arcade.Camera(self.width, self.height) #камера

        self.gui_camera = arcade.Camera(self.width, self.height)

        self.scene = arcade.Scene()  # запуск новой сцены

        self.scene.add_sprite_list("Player") #  записываем в сцену пока пустой список спрайта игрока
        self.scene.add_sprite_list("Inventory") #  записываем в сцену пока пустой список спрайта игрока
        self.scene.add_sprite_list("Walls", use_spatial_hash=True) #  записываем в сцену пока пустой список спрайта объектов

        map_name = "resources/map_res/map.tmj"

        layer_options = {
            "water": {
                "use_spatial_hash": False,
                 "hit_box_algorithm": "Simple",
            },
            "zabor": {
                "use_spatial_hash": False,
                "hit_box_algorithm": "Simple",
            },
            "ground": {
                # "hit_box_algorithm": "Simple",
            },
        }
        #загружаем карту
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_sprite = characters.PlayerCharacter()

        self.player_sprite.center_x = PLAYER_START_X #  задаем изначальную позицию игрока по х
        self.player_sprite.center_y = PLAYER_START_Y #  задаем изначальную позицию игрока по у

        self.inventory_sprite = WindowView.WindowView("inventar.png", INVENTORY_X, INVENTORY_Y)
        self.inventory_selected_sprite = WindowView.WindowView("selected.png", INVENTORY_SELECTED_X, INVENTORY_SELECTED_Y)


        self.scene.add_sprite(characters.LAYER_NAME_PLAYER, self.player_sprite) #  добавляем спрайт игрока в лист игрока текущей сцены


        # подключение физики. 1 параметр - объект над котом работает физика, 2 - с чем работает его физика
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=0, walls=self.scene["water"]
        )


    def on_update(self, delta_time): # покадровое обновление
        """Movement and game logic"""

        #обновление физики и перемещения объектов сцены
        self.physics_engine.update()
        self.inventory_sprite.update()

        self.scene.update_animation(
            delta_time, [characters.LAYER_NAME_PLAYER, ]
        )
        #Обновляем камеру
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
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.KEY_1:
            self.player_sprite.inventory[0].isSelected = True
            self.player_sprite.inventory[1].isSelected = False
            self.player_sprite.inventory[2].isSelected = False
        if key == arcade.key.KEY_2:
            self.player_sprite.inventory[0].isSelected = False
            self.player_sprite.inventory[1].isSelected = True
            self.player_sprite.inventory[2].isSelected = False
        if key == arcade.key.KEY_3:
            self.player_sprite.inventory[0].isSelected = False
            self.player_sprite.inventory[1].isSelected = False
            self.player_sprite.inventory[2].isSelected = True

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


   #вся отрисовка здесь
    def on_draw(self):
        self.clear() #очищаем старое

        self.camera.use()

        #  рисуем сцену

        self.scene.draw()

        self.gui_camera.use()

        self.inventory_sprite.draw()

        index = 0;
        for i in self.player_sprite.inventory:
            if i.isSelected == True:
                self.inventory_selected_sprite.position_X = INVENTORY_SELECTED_X + index*INVENTORY_SELECTED_CHANGE_VALUE
                self.inventory_selected_sprite.draw()
            i.texture_view.draw()
            i.count_view.draw()
            if i.count is None:
                pass
            else:
                arcade.draw_text(
                i.count,
                i.count_view.position_X-5 if i.count < 10 else i.count_view.position_X - 11,
                i.count_view.position_Y-7,
                arcade.csscolor.BROWN,
                14
            )
            index += 1

