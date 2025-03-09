import pyxel
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 70, 130

COLOR_PALETTE = {
    "黒": 0,
    "紺": 1,
    "紫": 2,
    "緑": 3,
    "茶": 4,
    "青": 5,
    "水色": 6,
    "白": 7,
    "赤": 8,
    "橙": 9,
    "黄": 10,
    "薄緑": 11,
    "薄青": 12,
    "灰": 13,
    "桃": 14,
    "肌色": 15,
}


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)  # 初期化

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

        self.now_screen = Start_Screen()

    def update(self):
        self.now_screen.update()

    def draw(self):
        self.now_screen.update()


class Start_Screen:
    def __init__(self):
        self.text = "スタート"
        self.font_size = 16
        self.tect_rect = (
            WINDOW_WIDTH / 2 - int(len(self.text) / 2 * self.font_size),
            WINDOW_HEIGHT / 2 - int(self.font_size / 2),
        )

    def update(self):
        pass

    def draw(self):
        pyxel.cls(COLOR_PALETTE["肌"])

        pyxel.text(
            self.text_rect[0], self.tect_rect[1], "self.text", COLOR_PALETTE["黒"]
        )


class Start_Screen:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


App()
