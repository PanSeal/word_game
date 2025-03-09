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

TEXT_SAVE_RECT = {}
start_positions = [("ア", 0, 0), ("タ", 0, 8), ("ミ", 0, 16)]
kana_list = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワ"
TEXT_SAVE_RECT["ー"] = (128, 128)

x, y = 0, 0
for kana in kana_list:
    TEXT_SAVE_RECT[kana] = (x, y)
    x += 8  # X座標を増やす

    # 特定の文字でリセット
    for start_kana, new_x, new_y in start_positions:
        if kana == start_kana:
            x, y = new_x, new_y


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)  # 初期化
        pyxel.load("word_game.pyxres")

        self.now_screen = Start_Screen()

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.now_screen.update()

    def draw(self):
        self.now_screen.draw()


class Start_Screen:
    def __init__(self):

        self.text = "スタート"
        self.font_size = 16
        self.text_rect = (
            WINDOW_WIDTH / 2 - int(len(self.text) / 2 * self.font_size),
            WINDOW_HEIGHT / 2 - int(self.font_size / 2),
        )

    def update(self):
        pass

    def draw(self):
        pyxel.cls(COLOR_PALETTE["黒"])

        draw_text((self.text_rect[0], self.text_rect[1]), self.text)


def draw_text(rect, strings):
    for number, i in enumerate(strings):
        pyxel.blt(
            rect[0] + number * 8,
            rect[1],
            0,
            TEXT_SAVE_RECT[i][0],
            TEXT_SAVE_RECT[i][1],
            8,
            8,
            0,
        )


App()
