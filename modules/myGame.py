import time
import arcade
import modules.characters as characters
import modules.WindowView as WindowView
import modules.scripts.orders as ORDERS


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


translater = {
    'apple': 'Яблоки',
    'onion': 'Лук',
    'radish': 'Редиска',
    'tomato': 'Помидоры',
    'wheat': 'Пшеница',
    'money' : 'Монет'
}

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Игра"

PLAYER_START_X = 1400
PLAYER_START_Y = 1900

TILE_SCALING = 0.5  #
GROW_RESOURCE_SCALING = 0.25  #

# позиция инвентаря
INVENTORY_X = 1150
INVENTORY_Y = 130
# позиция выбранного элемента инвентаря
INVENTORY_SELECTED_X = 1058
INVENTORY_SELECTED_Y = 130
INVENTORY_SELECTED_CHANGE_VALUE = 88

HOME_INVENTORY_X = 550
HOME_INVENTORY_Y = 450

THOUGHT_TIME = 3
SHOP = [{'name': 'wheat', 'price': 1}, {'name': 'tomato', 'price': 3}, {'name': 'radish', 'price': 8},
        {'name': 'onion', 'price': 12}]
SALE = {
    'apple' : 2,
    'wheat' : 4,
    'tomato' : 5,
    'radish' : 10,
    'onion' : 15
}

POINTS = [
    [Point(185, 620), Point(250, 555)],
    [Point(280, 620), Point(345, 555)],
    [Point(375, 620), Point(440, 555)],
    [Point(470, 620), Point(535, 555)],
    [Point(185, 530), Point(250, 465)],
    [Point(280, 530), Point(345, 465)],
    [Point(375, 530), Point(440, 465)],
    [Point(470, 530), Point(535, 465)],
    [Point(185, 440), Point(250, 375)],
    [Point(280, 440), Point(345, 375)],
    [Point(375, 440), Point(440, 375)],
    [Point(470, 440), Point(535, 375)],
    [Point(185, 350), Point(250, 285)],
    [Point(280, 350), Point(345, 285)],
    [Point(375, 350), Point(440, 285)],
    [Point(470, 350), Point(535, 285)],

    [Point(730, 410), Point(790, 350)],
    [Point(840, 410), Point(900, 350)],
    [Point(730, 320), Point(790, 265)],
    [Point(840, 320), Point(900, 265)],

    [Point(1030, 160), Point(1100, 100)],
    [Point(1120, 160), Point(1190, 100)],
    [Point(1210, 160), Point(1280, 100)],

    [Point(705, 630), Point(910, 560)]
]

scriptText = {
    1: {
        "max": 3,
        1: "Привет, новый друг! Меня зовут Лили и я работаю на своей маленькой ферме вместе со своими родителями. Недавно они отправились в путешествие и теперь я одна слежу  за фермой. Мне бы очень пригодилась твоя помощь!",
        2: "Давай я расскажу тебе, что тут, да как. ",
        3: "На севере острова находятся поля, на которые можно посадить, а позже и собрать разные культуры. Сейчас у меня с собой есть пшеница. Пойдем попробуем.",
    },
    2: {
        "max": 2,
        1: "Отлино! Ты посадил первую пшеницу. Давай посадим остальное и соберем. Также ты можешь собрать яблоки на яблонях ниже. Они уже поспели!",
        2: "Потом пойдем в дом и оставим все там."
    },
    3: {
        "max": 3,
        1:"В доме я храню все,что не помещается у меня в инвентарь. Также по завершении дня я отправляю все заказы именно из дома, так что, если нужных товаров не окажется дома, заказ пропадет.",
        2: "Ты можешь перемещать объекты из инвентаря в дом, кликнув по ним. Также ты можешь покупать нужные семена в магазине. Бюжет показан сверху от инвентаря. Ориентируйся на эту цифру.",
        3: "Заказы приходят в почтовый ящик возле выхода в единый океан. Давай положим весь урожай в дом и посмотрим, какие заказы нам пришли."
    },
    4: {
        "max": 2,
        1: "В ящике каждое утро появляются заказы. Проверяй ящик в начале каждого дня на наличие заказов. Чтобы принять заказ, нажми 'пробел'.",
        2: "Все принятые заказы я записываю в лист заказов. Его можно открыть, нажав на кнопку 'tab'. Так ты сможешь лучше ориентироваться в том, что тебе нужно подготовить к концу дня на отправку."
    },
    5: {
        "max": 2,
        1: "О нет! Мои родители был похищены!",
        2: "Нужно как можно скорее собрать деньги на выкуп. У нас всего три дня!",
    }
}


def interaction_button_draw(x, y):
    arcade.draw_circle_filled(
        x,
        y,
        12,
        [243, 229, 194]
    )
    arcade.Text(
        "E",
        x - 6,
        y - 5,
        arcade.csscolor.BROWN,
        12,
        0,
        'left',
        ("Comic Sans MS pixel rus eng", 'pix'),
        True,
        True,
    ).draw()


class GrowResource(arcade.Sprite):
    def __init__(self, name, x, y, thisTime):
        super().__init__()
        self.path = name
        self.name = name
        self.cur_texture_anima = 0
        self.texture = arcade.load_texture(f"resources/img/view/game_resources/{name}/state_growth_1.png")
        self.hit_box = self.texture.hit_box_points
        self.center_x = x + 2
        self.center_y = y + 10
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
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.set_mouse_visible(False)
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.scene = None
        self.curs = None
        self.money_sprite = None

        self.home_hit_list = None
        self.box_hit_list = None
        self.lunka_hit_list = None

        self.apple_hit_list = None
        #  спрайт игрока
        self.player_sprite = None

        self.inventory_sprite = None

        self.home_inventory_sprite = None
        self.home_inventory_is_active = False

        self.orderList_sprite = None
        self.orderList_is_active = False

        self.mailBox_sprite = None
        self.mailBox_sprite_is_active = False
        self.mailBox_orders = None

        self.home_resources = []
        #  инициализация карты
        self.tile_map = None

        self.camera = None
        # камера для неподвижных элементов интерфейса
        self.gui_camera = None
        #  задний фон

        self.day = 3
        self.next_day = False

        self.isWin = 0
        self.isEnd = 0

        self.scriptActive = True
        self.numberScript = 1
        self.partScript = 1
    # arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    #  запуск игры
    def setup(self):

        self.camera = arcade.Camera(self.width, self.height)  # камера

        self.curs = WindowView.WindowView("curs.png", 100, 50)

        self.winIMG = WindowView.WindowView("win.png", SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.loseIMG = WindowView.WindowView("lose.png", SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

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
            "lunka": {
                "hit_box_algorithm": "Detailed"
            },
            "apple": {
                "hit_box_algorithm": "Detailed"
            },
            "box": {
                "hit_box_algorithm": "Detailed"
            },
            "home": {
                "use_spatial_hash": False,
                "hit_box_algorithm": "Detailed"
            },
            "homeActive": {
                "use_spatial_hash": False,
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

        for i in range(0, 16):
            self.home_resources.append(characters.Resource("null", 0, i))

        self.inventory_sprite = WindowView.WindowView("inventar.png", INVENTORY_X, INVENTORY_Y)
        self.inventory_selected_sprite = WindowView.WindowView("selected.png", INVENTORY_SELECTED_X,
                                                               INVENTORY_SELECTED_Y)

        self.home_inventory_sprite = WindowView.WindowView("home_inventory.png", HOME_INVENTORY_X, HOME_INVENTORY_Y)
        self.playerPortet = WindowView.WindowView("plauerscript.png", 200, 400)
        self.playerPortet.scale = 0.5
        self.orderList_sprite = WindowView.WindowView("paper.png", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.mailBox_sprite = WindowView.WindowView("paper.png", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.mailBox_orders = ORDERS.DAYS[self.day]

        self.scene.add_sprite(characters.LAYER_NAME_PLAYER,
                              self.player_sprite)  # добавляем спрайт игрока в лист игрока текущей сцены
        self.money_sprite = WindowView.WindowView("money.png", SCREEN_WIDTH - 150, INVENTORY_Y + 100)
        # подключение физики. 1 параметр - объект над котом работает физика, 2 - с чем работает его физика
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=0, walls=[self.scene["water"], self.scene["home"]]
        )

    def on_update(self, delta_time):  # покадровое обновление
        """Movement and game logic"""
        # обновление физики и перемещения объектов сцены
        self.physics_engine.update()

        self.home_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["homeActive"]
        )
        self.lunka_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["lunka"]
        )
        self.apple_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["apple"]
        )
        self.box_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["box"]
        )

        self.curs.center_x = self.player_sprite.center_x
        self.curs.center_y = self.player_sprite.center_y

        self.inventory_selected_sprite.position_X = INVENTORY_SELECTED_X + 88 * self.player_sprite.inventory_selected_index

        self.scene.update_animation(
            delta_time + 3, [characters.LAYER_NAME_PLAYER, ]
        )
        # удаляем нулевые объекты инвентаря
        for res in self.player_sprite.inventory:
            if res.name != "null" and res.count == 0:
                self.player_sprite.inventory[res.index] = (characters.Resource("null", 0, res.index))

        # рост лунок
        for lunka in self.scene["lunka"]:
            if lunka.isUsed and lunka.resource.texture_index != 3 and time.time() - lunka.resource.texture_timing > lunka.resource.grow_time:
                lunka.resource.texture_timing = time.time()
                lunka.resource.texture_index += 1
                if lunka.resource.texture_index == 4: lunka.resource.texture_index = 0
                lunka.texture = lunka.resource.textures_list[lunka.resource.texture_index]

        # рост яблок
        for tree in self.scene["apple"]:
            if tree.resource.texture_index != 3 and time.time() - tree.resource.texture_timing > tree.resource.grow_time:
                tree.resource.texture_timing = time.time()
                tree.resource.texture_index += 1
                if tree.resource.texture_index == 4: tree.resource.texture_index = 0
                tree.texture = tree.resource.textures_list[tree.resource.texture_index]

        if self.home_inventory_is_active or self.orderList_is_active or self.mailBox_sprite_is_active or self.scriptActive:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0

        if self.next_day:
            self.mailBox_orders = ORDERS.DAYS[self.day]
            self.next_day = False

        # следим за мыслями
        if time.time() - self.player_sprite.thought_timer > THOUGHT_TIME:
            self.player_sprite.thought_timer = time.time()
            self.player_sprite.thought = "weather"

        # Обновляем камеру
        self.center_camera_to_player()

    def process_keychange(self):
        # Process up/down
        if not self.home_inventory_is_active:
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
            self.inventory_selected_sprite.position_X = INVENTORY_SELECTED_X * self.player_sprite.inventory_selected_index

        if key == arcade.key.KEY_2:
            self.player_sprite.inventory_selected_index = 1
            self.inventory_selected_sprite.position_X = INVENTORY_SELECTED_X * self.player_sprite.inventory_selected_index

        if key == arcade.key.KEY_3:
            self.player_sprite.inventory_selected_index = 2
            self.inventory_selected_sprite.position_X = INVENTORY_SELECTED_X * self.player_sprite.inventory_selected_index

        if key == arcade.key.E:
            for lunka in self.lunka_hit_list:
                if not lunka.isUsed:
                    if  self.numberScript == 2:
                        self.scriptActive = True
                    if (self.player_sprite.inventory[self.player_sprite.inventory_selected_index].name is not None
                            and "BackPack" in self.player_sprite.inventory[
                                self.player_sprite.inventory_selected_index].state
                            and self.player_sprite.inventory[self.player_sprite.inventory_selected_index].count > 0):
                        lunka.isUsed = True
                        lunka.resource = GrowResource(
                            self.player_sprite.inventory[self.player_sprite.inventory_selected_index].name,
                            lunka.center_x, lunka.center_y, 5.0)
                        lunka.texture = lunka.resource.textures_list[0]
                        self.player_sprite.inventory[self.player_sprite.inventory_selected_index].count -= 1
                    else:
                        self.player_sprite.thought = "не получится"
                        self.player_sprite.thought_timer = time.time()
                elif lunka.texture == lunka.resource.textures_list[3]:
                    res_inventory_founded = False
                    for res in self.player_sprite.inventory:
                        if res.name == lunka.resource.name and res.state == "/product":
                            res.count += 3
                            res_inventory_founded = True
                            break
                    if res_inventory_founded == False:
                        for res in self.player_sprite.inventory:
                            if res.name == "null":
                                self.player_sprite.inventory[res.index] = characters.Resource(lunka.resource.name, 3,
                                                                                              res.index, "/product")
                                res_inventory_founded = True
                                break
                    if res_inventory_founded == True:
                        lunka.texture = lunka.resource.textures_list[4]
                        lunka.isUsed = False
                    else:
                        self.player_sprite.thought = "Нет места"
                else:
                    self.player_sprite.thought = "Еще не выросло.."
            for tree in self.apple_hit_list:
                if tree.texture == tree.resource.textures_list[3]:
                    res_inventory_founded = False
                    for res in self.player_sprite.inventory:
                        if res.name == tree.resource.name:
                            res.count += 3
                            res_inventory_founded = True
                            break
                    if res_inventory_founded == False:
                        for res in self.player_sprite.inventory:
                            if res.name == "null":
                                self.player_sprite.inventory[res.index] = characters.Resource(tree.resource.name, 3,
                                                                                              res.index, "/product")
                                res_inventory_founded = True
                                break
                    if res_inventory_founded == True:
                        tree.resource.texture_index = -1
                    else:
                        self.player_sprite.thought = "Нет места"
                else:
                    self.player_sprite.thought = "Еще не выросло.."
            for door in self.home_hit_list:
                if self.numberScript == 3:
                    self.scriptActive = True
                if self.home_inventory_is_active == True:
                    self.home_inventory_is_active = False
                else:
                    self.home_inventory_is_active = True
                break
            for box in self.box_hit_list:
                if self.numberScript == 4 or self.numberScript == 5:
                    self.scriptActive = True
                if self.mailBox_sprite_is_active:
                    self.mailBox_sprite_is_active = False
                else:
                    if len(self.mailBox_orders) > 0 and self.numberScript > 3:
                        self.mailBox_sprite_is_active = True
                    else:
                        self.player_sprite.thought = "Ничего нет"

        if key == arcade.key.TAB: self.orderList_is_active = not self.orderList_is_active

        if key == arcade.key.SPACE and self.mailBox_sprite_is_active:
            if len(self.mailBox_orders) > 0:
                self.player_sprite.order.append(
                    {
                        'name': self.mailBox_orders[0]['name'],
                        'orderList': self.mailBox_orders[0]['orderList']
                    }
                )
                print(self.player_sprite.order)
                self.mailBox_orders.pop(0)

        if key == arcade.key.ENTER:
            if self.scriptActive:
                if scriptText[self.numberScript]["max"] > self.partScript:
                    self.partScript += 1
                else:
                    self.numberScript+=1
                    self.partScript = 1
                    self.scriptActive = False
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

    def on_draw(self):
        self.clear()  # очищаем старое

        self.camera.use()

        #  рисуем сцену

        self.scene.draw()

        for door in self.home_hit_list:
            interaction_button_draw(self.player_sprite.center_x - 50, self.player_sprite.center_y)

        for lunka in self.lunka_hit_list:
            interaction_button_draw(self.player_sprite.center_x - 50, self.player_sprite.center_y)

        for tree in self.apple_hit_list:
            interaction_button_draw(self.player_sprite.center_x - 50, self.player_sprite.center_y)

        for box in self.box_hit_list:
            interaction_button_draw(self.player_sprite.center_x - 50, self.player_sprite.center_y)

        if self.player_sprite.thought != "weather":
            self.player_sprite.thoughtWindow.position_X = self.player_sprite.center_x + 90
            self.player_sprite.thoughtWindow.position_Y = self.player_sprite.center_y + 60
            self.player_sprite.thoughtWindow.draw()
            self.player_sprite.thoughtWindow.draw_text(self.player_sprite.thought,
                                                       self.player_sprite.thoughtWindow.position_X - 60,
                                                       self.player_sprite.thoughtWindow.position_Y)

        self.gui_camera.use()

        self.inventory_sprite.draw()
        self.inventory_selected_sprite.draw()
        self.money_sprite.draw()
        self.money_sprite.draw_text(self.player_sprite.money, self.money_sprite.position_X - 30,
                                    self.money_sprite.position_Y - 5, (182, 137, 98), 18)

        arcade.Text(
            "Day " + str(self.day) + "/3",
            10,
            25,
            (182, 137, 98),
            20,
            0,
            "left",
            ("Comic Sans MS pixel rus eng", 'pix'),
        ).draw()

        for res in self.player_sprite.inventory:
            res.texture_view.draw()
            res.count_view.draw()
            if res.count != 0:
                if res.count < 10:
                    res.count_view.draw_text(str(res.count), res.count_view.position_X - 5,
                                             res.count_view.position_Y - 7)
                else:
                    res.count_view.draw_text(str(res.count), res.count_view.position_X - 11,
                                             res.count_view.position_Y - 7)

        if self.home_inventory_is_active:
            self.home_inventory_sprite.draw()
            self.home_inventory_sprite.draw_text("Спать", 760, 590, (232, 207, 166), 30)
            for res in self.home_resources:
                if res.name != "null":
                    res.texture_view.draw()
                    res.count_view.draw()
                    if res.count != 0:
                        if res.count < 10:
                            res.count_view.draw_text(str(res.count), res.count_view.position_X - 5,
                                                     res.count_view.position_Y - 7)
                        else:
                            res.count_view.draw_text(str(res.count), res.count_view.position_X - 11,
                                                     res.count_view.position_Y - 7)
            self.curs.draw()

        if self.mailBox_sprite_is_active:
            if len(self.mailBox_orders) > 0 :
                self.mailBox_sprite.draw()
                line = 0
                for text in self.mailBox_orders[0]['massage']:
                    self.mailBox_sprite.draw_text(text, SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 + 100 - line,
                                                  (182, 137, 98), 15, 550, True)
                    line += 20
                if self.mailBox_orders[0]['name'] != 'Похитители':
                    self.mailBox_sprite.draw_text("С уважением, " + self.mailBox_orders[0]['name'], SCREEN_WIDTH / 2 + 90, SCREEN_HEIGHT / 2 - 150)
            else:
                self.mailBox_sprite_is_active = False

        if self.orderList_is_active:
            self.orderList_sprite.draw()
            line = 0
            for orders in self.player_sprite.order:
                gap = 10
                self.orderList_sprite.draw_text(orders['name'], SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 + 150 - line)
                line += 20
                for text in orders['orderList']:
                    self.orderList_sprite.draw_text(translater[text['name']] + ":  " + text['amount'] + "шт.", SCREEN_WIDTH / 2 - 250 + gap, SCREEN_HEIGHT / 2 + 150 - line)
                    line += 20
                line += 20

        if self.scriptActive:
            if self.numberScript != 5 or (self.numberScript == 5 and len(self.player_sprite.order)):
                arcade.draw_rectangle_filled(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,SCREEN_WIDTH,SCREEN_HEIGHT,(0,0,0,150))
                arcade.draw_rectangle_filled(SCREEN_WIDTH/2,SCREEN_HEIGHT/9,SCREEN_WIDTH,SCREEN_HEIGHT/4,(10,30,30,255))
                self.playerPortet.draw()
                arcade.Text(scriptText[self.numberScript][self.partScript],100,100,(255,255,255),18,1300,"left",("Comic Sans MS pixel rus eng", 'pix'), False,
                False,
                'left',
                'baseline',
                True).draw()

        if self.isEnd:
            if self.isWin:
                self.winIMG.draw()
            else:
                self.loseIMG.draw()


    def on_mouse_motion(self, x, y, dx, dy):
        self.curs.position_X = x
        self.curs.position_Y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.home_inventory_is_active:
            if button == arcade.MOUSE_BUTTON_LEFT:
                for i in range(0, 16):
                    if x > POINTS[i][0].x and x < POINTS[i][1].x and y > POINTS[i][1].y and y < POINTS[i][0].y:
                        if self.home_resources[i].name != "null":
                            isGet = False
                            for res in self.player_sprite.inventory:
                                if res.name == self.home_resources[i].name and res.state == self.home_resources[
                                    i].state:
                                    res.count += self.home_resources[i].count
                                    self.home_resources[i] = characters.Resource("null", 0, i)
                                    isGet = True
                                    break
                            if isGet == False:
                                for res in self.player_sprite.inventory:
                                    if res.name == "null":
                                        self.home_resources[i].index = res.index
                                        self.home_resources[i].texture_view.position_X = res.texture_view.position_X
                                        self.home_resources[i].count_view.position_X = res.count_view.position_X
                                        self.home_resources[i].texture_view.position_Y = res.texture_view.position_Y
                                        self.home_resources[i].count_view.position_Y = res.count_view.position_Y
                                        self.player_sprite.inventory[res.index] = self.home_resources[i]
                                        self.home_resources[i] = characters.Resource("null", 0, i)
                for i in range(16, 20):
                    if x > POINTS[i][0].x and x < POINTS[i][1].x and y > POINTS[i][1].y and y < POINTS[i][0].y:
                        if self.player_sprite.money >= SHOP[i - 16]['price']:
                            isBuy = False
                            for item in self.home_resources:
                                if item.name == SHOP[i - 16]['name'] and item.state == "/BackPack":
                                    item.count += 3
                                    self.player_sprite.money -= SHOP[i - 16]['price']
                                    isBuy = True
                                    break
                            if isBuy == False:
                                index = self.home_index()
                                if index != None:
                                    self.home_resources[index] = characters.Resource(SHOP[i - 16]['name'], 3, index,
                                                                                     "/BackPack")
                                    self.home_resources[index].texture_view.position_X = POINTS[index][0].x + 27
                                    self.home_resources[index].texture_view.position_Y = POINTS[index][1].y + 40
                                    self.home_resources[index].count_view.position_X = POINTS[index][0].x + 60
                                    self.home_resources[index].count_view.position_Y = POINTS[index][1].y + 10
                                    self.player_sprite.money -= SHOP[i - 16]['price']
                for i in range(20, 23):
                    if x > POINTS[i][0].x and x < POINTS[i][1].x and y > POINTS[i][1].y and y < POINTS[i][0].y:
                        index = self.home_index()
                        isGet = False
                        if self.player_sprite.inventory[i - 20].name != "null":
                            for item in self.home_resources:
                                if item.name == self.player_sprite.inventory[i - 20].name and item.state == \
                                        self.player_sprite.inventory[i - 20].state:
                                    item.count += self.player_sprite.inventory[i - 20].count
                                    self.player_sprite.inventory[i - 20] = characters.Resource("null", 0, i - 20)
                                    isGet = True
                                    break
                            if isGet == False:
                                if index != None:
                                    self.player_sprite.inventory[i - 20].texture_view.position_X = POINTS[index][
                                                                                                       0].x + 27
                                    self.player_sprite.inventory[i - 20].texture_view.position_Y = POINTS[index][
                                                                                                       1].y + 40
                                    self.player_sprite.inventory[i - 20].count_view.position_X = POINTS[index][0].x + 60
                                    self.player_sprite.inventory[i - 20].count_view.position_Y = POINTS[index][1].y + 10
                                    self.home_resources[index] = self.player_sprite.inventory[i - 20]
                                    self.player_sprite.inventory[i - 20] = characters.Resource("null", 0, i - 20)
                if x > POINTS[23][0].x and x < POINTS[23][1].x and y > POINTS[23][1].y and y < POINTS[23][0].y:
                    for order in self.player_sprite.order:
                        if order['name'] != 'Похитители':
                            for orderList in order['orderList']:
                                for res in self.home_resources:
                                    if res.name == orderList['name'] and int(res.count) >= int(orderList['amount']):
                                        res.count = int(res.count) - int(orderList['amount'])
                                        self.player_sprite.money += SALE[orderList['name']] * int(orderList['amount'])
                    del self.player_sprite.order[1:len(self.player_sprite.order)]
                    if self.day < 3 :
                        self.day += 1
                        self.next_day = True
                    else:
                        self.isEnd = True
                        if self.player_sprite.money >= 520:
                            self.isWin=True

    def home_index(self):
        for item in self.home_resources:
            if item.name == "null": return item.index
        return None
