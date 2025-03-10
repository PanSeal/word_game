import pyxel
import random
import platform

WINDOW_WIDTH, WINDOW_HEIGHT = 100, 160

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

# カタガナのセーブ座標
TEXT_SAVE_RECT = {}
start_positions = [("タ", 0, 8), ("マ", 0, 16), ("ァ", 0, 24)]
kana_list = (
    "アイウエオカキクケコサシスセソ"
    "タチツテトナニヌネノハヒフヘホ"
    "マミムメモヤユヨラリルレロワヲン"
    "ァィゥェォャュョッ゛゜ー"
)
x, y = 0, 0
for kana in kana_list:
    # 特定の文字でリセット
    for start_kana, new_x, new_y in start_positions:
        if kana == start_kana:
            x, y = new_x, new_y

    TEXT_SAVE_RECT[kana] = (x, y)
    x += 8  # X座標を増やす


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)  # 初期化
        pyxel.load("word_game.pyxres")

        self.now_screen = Start_Screen()

        # PC(非タップ端末)からの実行時のみマウスカーソルを表示する
        os_name = platform.system()
        is_pc = os_name == "Darwin"
        pyxel.mouse(is_pc)

        pyxel.run(self.update, self.draw)

    def update(self):
        result = self.now_screen.update()
        if result:
            self.now_screen = Enter_Respondent()

    def draw(self):
        self.now_screen.draw()


class Start_Screen:
    def __init__(self):

        self.text = "スタート"
        self.font_size = 8
        self.text_rect = (
            WINDOW_WIDTH / 2 - int((len(self.text) / 2) * self.font_size),
            WINDOW_HEIGHT / 2 - int(self.font_size / 2),
        )

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return True

    def draw(self):
        pyxel.cls(COLOR_PALETTE["黒"])

        draw_text((self.text_rect[0], self.text_rect[1]), self.text)


class Player_Number_Screen:
    def __init__(self):

        self.text = "フ゜レイ ニンス゛ウ センタク"
        self.font_size = 8
        self.text_rect = (
            WINDOW_WIDTH / 2 - int((len(self.text) / 2) * self.font_size),
            10,
        )

    def update(self):
        pass

    def draw(self):
        pyxel.cls(COLOR_PALETTE["黒"])

        draw_text((self.text_rect[0], self.text_rect[1]), self.text)


class Enter_Respondent:
    def __init__(self):
        self.respondent = None
        rect = (10, 10, 80, 10)
        self.entry_flame = Entry_Flame(rect)

    def update(self):
        result = self.entry_flame.update()
        if result:
            self.respondent = result

    def draw(self):
        pyxel.cls(COLOR_PALETTE["黒"])

        self.entry_flame.draw()


# __ __ __ __ __ __ __ キーボード設定 __ __ __ __ __ __ __
# キーボード設定
KEY_BORD_PADDING = 2
KEY_BORD_SIZE = (int((WINDOW_WIDTH - 6 * KEY_BORD_PADDING) / 5), 12)
# キーボードの行列
LINES = (("ア", "カ", "サ"), ("タ", "ナ", "ハ"), ("マ", "ヤ", "ラ"), ("゛", "ワ"))
# ア段のキーボード座標
KEY_BORD_RECTS = {}
X = 3
y = WINDOW_HEIGHT - (KEY_BORD_PADDING + KEY_BORD_SIZE[1]) * (len(LINES) + 1)
for line in LINES:
    x = X
    y += KEY_BORD_PADDING + KEY_BORD_SIZE[1]
    for row in line:
        x += KEY_BORD_PADDING + KEY_BORD_SIZE[0]
        KEY_BORD_RECTS[row] = x, y
# イウエオ　拡張キーボード座標
LINE_KEY_BORD_RECTS = (
    (0, 0),
    (-KEY_BORD_SIZE[0], 0),
    (0, -KEY_BORD_SIZE[1]),
    (KEY_BORD_SIZE[0], 0),
    (0, KEY_BORD_SIZE[1]),
)
# 小文字変換のキーボード座標
SMALL_LETTER_KEY_BORD_RECTS = (
    KEY_BORD_RECTS["ワ"][0] + KEY_BORD_PADDING + KEY_BORD_SIZE[0],
    KEY_BORD_RECTS["ワ"][1],
)
# BackSpaceのキーボード座標
DELETE_KEY_BORD_RECTS = (
    KEY_BORD_RECTS["サ"][0] + KEY_BORD_PADDING + KEY_BORD_SIZE[0],
    KEY_BORD_RECTS["サ"][1],
)
# 50音
JAPANESE_SYLLABARY = (
    # 1列目
    "アイウエオ",
    "カキクケコ",
    "サシスセソ",
    # 2列目
    "タチツテト",
    "ナニヌネノ",
    "ハヒフヘホ",
    # 3列目
    "マミムメモ",
    "ヤユヨ",
    "ラリルレロ",
    # 4列目
    "ワヲン",
    "゛゜ー",
)


class Entry_Flame:
    def __init__(self, rect):
        self.rect = rect
        self.entry: str = None
        self.keybord = KEY_BORD_Manager()

    def update(self):
        result = self.keybord.update()
        if isinstance(result, list):
            if result[0] == "detect":
                if self.entry:
                    self.entry += result[1]
                else:
                    self.entry = result[1]
            else:
                print(result)

    def draw(self):
        pyxel.rectb(
            self.rect[0],
            self.rect[1],
            self.rect[2],
            self.rect[3],
            COLOR_PALETTE["青"],
        )

        if self.entry:
            draw_text((self.rect[0], self.rect[1]), self.entry)

        self.keybord.draw()


class KEY_BORD_Manager:
    def __init__(self):
        self.key_bords = []
        for i in JAPANESE_SYLLABARY:
            self.key_bords.append(Key_Bord(i))

        # その他キーボード
        self.small_key = Small_Key()
        self.delete_key = Delet_Key()

        self.hold_key = None

    def update(self):

        # 　通常のキー監視
        is_hold = False

        for i in self.key_bords:
            result = i.update(self.hold_key)
            if isinstance(result, list):
                self.hold_key = None
                return result
            elif result:
                is_hold = True
                self.hold_key = result

        if not is_hold:
            self.hold_key = None

        # 小文字・デリートキー監視
        result_1 = self.small_key.update(self.hold_key)
        if result_1:
            return result_1
        result_2 = self.delete_key.update(self.hold_key)
        if result_2:
            return result_2

    def draw(self):
        for i in self.key_bords:
            i.draw()

        self.small_key.draw()
        self.delete_key.draw()

        for i in self.key_bords:
            i.second_draw()


class Key_Bord:
    def __init__(self, line):
        self.line = line
        self.key = self.line[0]
        self.rects = []
        for number, i in enumerate(self.line):
            self.rects.append(
                (
                    KEY_BORD_RECTS[self.key][0] + LINE_KEY_BORD_RECTS[number][0],
                    KEY_BORD_RECTS[self.key][1] + LINE_KEY_BORD_RECTS[number][1],
                    KEY_BORD_SIZE[0],
                    KEY_BORD_SIZE[1],
                )
            )
        self.click = False
        self.active = True

        self.select_key = None

    def update(self, key):
        # 他のキーを押している時には反応しない
        if not (self.key == key or key == None):
            self.active = False
            return
        else:
            self.active = True

        # ボタンを離した時
        if self.click and not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.click = False
            result = self.select_key
            self.select_key = None
            return ["detect", result]

        # ボタンクリック時
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
            if (
                self.rects[0][0] <= mouse_x <= self.rects[0][0] + self.rects[0][2]
                and self.rects[0][1] <= mouse_y <= self.rects[0][1] + self.rects[0][3]
            ):
                self.click = True
                self.select_key = self.key
                return self.key

        # ボタンホールド時
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if self.click:
                mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y

                for n, rect in enumerate(self.rects):
                    if (
                        rect[0] <= mouse_x <= rect[0] + rect[2]
                        and rect[1] <= mouse_y <= rect[1] + rect[3]
                    ):
                        self.select_key = self.line[n]
                return self.key

    def draw(self):
        if self.select_key == self.key:
            color = COLOR_PALETTE["橙"]
        else:
            color = COLOR_PALETTE["薄緑"]

        if self.active:
            pyxel.rectb(
                self.rects[0][0],
                self.rects[0][1],
                self.rects[0][2],
                self.rects[0][3],
                color,
            )
            draw_text(self.rects[0], self.line[0])
        else:
            pyxel.rectb(
                self.rects[0][0],
                self.rects[0][1],
                self.rects[0][2],
                self.rects[0][3],
                COLOR_PALETTE["灰"],
            )

    def second_draw(self):
        if self.click:
            for number, i in enumerate(self.line[1:]):
                if self.select_key == i:
                    color = COLOR_PALETTE["橙"]
                else:
                    color = COLOR_PALETTE["薄緑"]

                pyxel.rect(
                    self.rects[number + 1][0],
                    self.rects[number + 1][1],
                    self.rects[number + 1][2],
                    self.rects[number + 1][3],
                    COLOR_PALETTE["黒"],
                )
                pyxel.rectb(
                    self.rects[number + 1][0],
                    self.rects[number + 1][1],
                    self.rects[number + 1][2],
                    self.rects[number + 1][3],
                    color,
                )
                draw_text(
                    (
                        self.rects[number + 1][0],
                        self.rects[number + 1][1],
                    ),
                    i,
                )


class Small_Key:
    def __init__(self):
        self.key = "small"

        self.rect = (
            SMALL_LETTER_KEY_BORD_RECTS[0],
            SMALL_LETTER_KEY_BORD_RECTS[1],
            KEY_BORD_SIZE[0],
            KEY_BORD_SIZE[1],
        )

        self.active = True

    def update(self, key):
        if key:
            self.active = False
            return
        else:
            self.active = True

        # ボタンクリック時
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
            if (
                self.rect[0] <= mouse_x <= self.rect[0] + self.rect[2]
                and self.rect[1] <= mouse_y <= self.rect[1] + self.rect[3]
            ):
                return [self.key, self.key]

    def draw(self):
        if self.active:
            pyxel.rectb(
                self.rect[0],
                self.rect[1],
                self.rect[2],
                self.rect[3],
                COLOR_PALETTE["薄緑"],
            )
            pyxel.text(self.rect[0], self.rect[1], self.key, COLOR_PALETTE["白"])
        else:
            pyxel.rectb(
                self.rect[0],
                self.rect[1],
                self.rect[2],
                self.rect[3],
                COLOR_PALETTE["灰"],
            )


class Delet_Key(Small_Key):
    def __init__(self):
        super().__init__()
        self.key = "delete"

        self.rect = (
            DELETE_KEY_BORD_RECTS[0],
            DELETE_KEY_BORD_RECTS[1],
            KEY_BORD_SIZE[0],
            KEY_BORD_SIZE[1],
        )


def draw_text(rect, strings):
    number = 0

    for i in strings:

        if i in TEXT_SAVE_RECT:
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

        number += 1


App()
