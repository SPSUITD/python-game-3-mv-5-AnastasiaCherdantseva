import arcade



class WindowView(arcade.Sprite):
    def __init__(self, name,x,y):
        super().__init__()
        main_path = "resources/img/view/"  #
        self.idle_texture_pair = arcade.load_texture(f"{main_path}{name}")  # текстура в неподвижном состоянии
        self.texture = self.idle_texture_pair # задаем стартовую текстуру
        self.hit_box = self.texture.hit_box_points  # задаем границы текстурам
        self.position_X = x
        self.position_Y = y
        self.width =self.idle_texture_pair.width
        self.height =self.idle_texture_pair.height
        self.opacity = 255

    def draw(self):
        arcade.draw_texture_rectangle(
            self.position_X,
            self.position_Y,
            self.width,
            self.height,
            self.texture,
            0,
            self.opacity
        )
    def draw_text(self,text,x,y, color = (182,137,98) , font = 15, width = 0,line=False,bold=False):
        arcade.Text(
            str(text),
            x,
            y,
            color,
            font,
            width,
            "left",
            ("Comic Sans MS pixel rus eng", 'pix'),
            bold,
            False,
            'left',
            'baseline',
            line

        ).draw()