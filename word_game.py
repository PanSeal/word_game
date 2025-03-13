import pyxel
import random
import copy
import platform
from dataclasses import dataclass

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

# ひらがなのセーブ座標
HIRAGANA_TEXT_SAVE_RECT = {}
start_positions_2 = [("た", 0, 80), ("ま", 0, 88), ("ゃ", 0, 96)]
kana_list_2 = (
    "あいうえおかきくけこさしすせそ"
    "たちつてとなにぬねのはひふへほ"
    "まみむめもやゆよらりるれろわをん"
    "ゃゅょっ"
)
x, y = 0, 72
for kana in kana_list_2:
    # 特定の文字でリセット
    for start_kana, new_x, new_y in start_positions_2:
        if kana == start_kana:
            x, y = new_x, new_y

    HIRAGANA_TEXT_SAVE_RECT[kana] = (x, y)
    x += 8  # X座標を増やす

print(HIRAGANA_TEXT_SAVE_RECT)

# 数字のセーブ座標
NUMBER_SAVE_RECT = []
for i in range(10):
    NUMBER_SAVE_RECT.append((8 * i, 56))


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)  # 初期化
        pyxel.load("word_game.pyxres")

        self.game_manager = Game_Manager
        self.game_manager.set_scene(Start_Up_Manager())

        # PC(非タップ端末)からの実行時のみマウスカーソルを表示する
        os_name = platform.system()
        is_pc = os_name == "Darwin"
        pyxel.mouse(is_pc)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.game_manager.update()

    def draw(self):
        pyxel.cls(COLOR_PALETTE["黒"])
        self.game_manager.draw()


# __ __ __ __ __ __ __ ゲーム進行 __ __ __ __ __ __ __
# シーン
class Scene:
    NAME: str


class Game_Manager:
    now_scene: Scene

    @classmethod
    def set_scene(cls, next_manager):
        cls.now_scene = next_manager

    @classmethod
    def update(cls):
        cls.now_scene.update()

    @classmethod
    def draw(cls):
        cls.now_scene.draw()


# __ __ __ __ __ __ __ スタートアップ進行 __ __ __ __ __ __ __
class Start_Up_Manager(Scene):
    NAME = "START_MANAGER"

    def __init__(self):
        """
        1.スタート画面
        2.プレイヤー人数の設定
        3.プレイヤーネームの設定
        """
        self.turn = (Start_Screen, Player_Number_Screen, Player_Name_Screen)

        self.now_screen = self.turn[0]()

    def update(self):
        """スタートアップの設定を行う

        Returns:
            _list_: プレイヤーの名前
        """
        result = self.now_screen.update()

        if result:
            if self.now_screen.NAME == "START":
                self.now_screen = self.turn[1]()
            elif self.now_screen.NAME == "NUMBER":
                self.now_screen = self.turn[2](result)
            elif self.now_screen.NAME == "NAME":
                # こここにゲーム進行マネージャーを登録
                Game_Manager.set_scene(Start_Up_Manager(result))

    def draw(self):
        self.now_screen.draw()


class Start_Screen:
    NAME = "START"

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
        draw_text((self.text_rect[0], self.text_rect[1]), self.text)


pns_padding = 5

PNS_TEXT = "フ゜レイ ニンス゛ウ", "ヲ センタク"
PNS_TEXT_RECT_X = WINDOW_WIDTH / 2 - int((len(PNS_TEXT[0]) / 2) * 8)
PNS_TEXT_RECTS_Y = pns_padding, pns_padding + 2 + 8

PNS_NEXT_BUTTON_RECT = (
    WINDOW_WIDTH - (8 * 3 + pns_padding + 2 * 2),  # x
    WINDOW_HEIGHT - (8 + pns_padding + 2 * 2),  # y
    8 * 3 + 2 * 2,  # w
    8 + 2 * 2,  # h
)

CHOICES_NUMBER_OF_PLAYER_NUMBER = 5
CIRCLE_RECT_X = 20
CIRCLE_RECTS_Y = [
    int(
        (
            WINDOW_HEIGHT
            - (8 * 2 + pns_padding + 2)
            - (PNS_NEXT_BUTTON_RECT[3] + pns_padding)
        )
        / (CHOICES_NUMBER_OF_PLAYER_NUMBER + 1)
        * (i + 0.5)
        + (8 * 2 + pns_padding + 2)
    )
    for i in range(5)
]
CIRCLE_DIAMETER = 8
PLAYER_NUMBER_STRINGS_RECT_X = 40


class Player_Number_Screen:
    NAME = "NUMBER"

    def __init__(self):

        self.text = PNS_TEXT
        self.text_rect_x = PNS_TEXT_RECT_X
        self.text_rects_y = PNS_TEXT_RECTS_Y
        self.select_number = 0

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y

            # 人数 円
            for i in range(CHOICES_NUMBER_OF_PLAYER_NUMBER):
                if (
                    CIRCLE_RECT_X <= mouse_x <= CIRCLE_RECT_X + CIRCLE_DIAMETER
                    and CIRCLE_RECTS_Y[i]
                    <= mouse_y
                    <= CIRCLE_RECTS_Y[i] + CIRCLE_DIAMETER
                ):
                    self.select_number = i + 2

            # 進む
            if (
                PNS_NEXT_BUTTON_RECT[0]
                <= mouse_x
                <= PNS_NEXT_BUTTON_RECT[0] + PNS_NEXT_BUTTON_RECT[2]
                and PNS_NEXT_BUTTON_RECT[1]
                <= mouse_y
                <= PNS_NEXT_BUTTON_RECT[1] + PNS_NEXT_BUTTON_RECT[3]
            ):
                if self.select_number:
                    return self.select_number

    def draw(self):
        # テキスト
        for i, text in enumerate(self.text):
            draw_text((self.text_rect_x, self.text_rects_y[i]), text)

        # 人数選択
        for i in range(CHOICES_NUMBER_OF_PLAYER_NUMBER):
            # 円
            pyxel.circ(
                CIRCLE_RECT_X + int(CIRCLE_DIAMETER / 2),
                CIRCLE_RECTS_Y[i] + int(CIRCLE_DIAMETER / 2),
                int(CIRCLE_DIAMETER / 2),
                COLOR_PALETTE["白"],
            )
            if self.select_number == i + 2:
                pyxel.circ(
                    CIRCLE_RECT_X + int(CIRCLE_DIAMETER / 2),
                    CIRCLE_RECTS_Y[i] + int(CIRCLE_DIAMETER / 2),
                    int(CIRCLE_DIAMETER / 2) - 1,
                    COLOR_PALETTE["桃"],
                )

            # 数字
            pyxel.blt(
                PLAYER_NUMBER_STRINGS_RECT_X,
                CIRCLE_RECTS_Y[i],
                0,
                NUMBER_SAVE_RECT[i + 2][0],
                NUMBER_SAVE_RECT[i + 2][1],
                8,
                8,
                0,
            )

        # 次に進むボタン
        if self.select_number:
            next_button_color = COLOR_PALETTE["橙"]
        else:
            next_button_color = COLOR_PALETTE["灰"]

        pyxel.rect(
            PNS_NEXT_BUTTON_RECT[0],
            PNS_NEXT_BUTTON_RECT[1],
            PNS_NEXT_BUTTON_RECT[2],
            PNS_NEXT_BUTTON_RECT[3],
            next_button_color,
        )

        draw_text((PNS_NEXT_BUTTON_RECT[0] + 2, PNS_NEXT_BUTTON_RECT[1] + 2), "ススム")


p_name_s_padding = 5

P_NAME_S_TEXT = "フ゜レイヤーめい を", "にゅうりょく"
P_NAME_S_TEXT_RECT_X = WINDOW_WIDTH / 2 - int((len(PNS_TEXT[0]) / 2) * 8)
P_NAME_S_TEXT_RECTS_Y = pns_padding, pns_padding + 2 + 8

P_NAME_S_NEXT_BUTTON_RECT = (
    WINDOW_WIDTH - (8 * 3 + p_name_s_padding + 2 * 2),  # x
    WINDOW_HEIGHT - (8 + p_name_s_padding + 2 * 2),  # y
    8 * 3 + 2 * 2,  # w
    8 + 2 * 2,  # h
)

P_NAME_S_ENTRY_RECT_X = 10


class Player_Name_Screen:
    NAME = "NAME"

    def __init__(self, number):
        self.player_number = number

        self.entrys = Entry_Flame_Manager(
            P_NAME_S_ENTRY_RECT_X,
            P_NAME_S_TEXT_RECTS_Y[1] + 8 + 2,
            P_NAME_S_NEXT_BUTTON_RECT[1],
            self.player_number,
        )

        self.names = ["" for i in range(self.player_number)]

        self.all_entry = False

    def update(self):
        # エントリーフレーム
        self.entrys.update()

        self.names = self.entrys.get_entry()

        if all(name != "" for name in self.names):
            self.all_entry = True
        else:
            self.all_entry = False

        # 進む
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.all_entry:
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
            if (
                P_NAME_S_NEXT_BUTTON_RECT[0]
                <= mouse_x
                <= P_NAME_S_NEXT_BUTTON_RECT[0] + PNS_NEXT_BUTTON_RECT[2]
                and P_NAME_S_NEXT_BUTTON_RECT[1]
                <= mouse_y
                <= P_NAME_S_NEXT_BUTTON_RECT[1] + PNS_NEXT_BUTTON_RECT[3]
            ):
                return self.names

    def draw(self):
        # テキスト
        for i, text in enumerate(P_NAME_S_TEXT):
            draw_text((P_NAME_S_TEXT_RECT_X, P_NAME_S_TEXT_RECTS_Y[i]), text)

        # 次に進むボタン
        if self.all_entry:
            next_button_color = COLOR_PALETTE["橙"]
        else:
            next_button_color = COLOR_PALETTE["灰"]
        pyxel.rect(
            P_NAME_S_NEXT_BUTTON_RECT[0],
            P_NAME_S_NEXT_BUTTON_RECT[1],
            P_NAME_S_NEXT_BUTTON_RECT[2],
            P_NAME_S_NEXT_BUTTON_RECT[3],
            next_button_color,
        )
        draw_text(
            (P_NAME_S_NEXT_BUTTON_RECT[0] + 2, P_NAME_S_NEXT_BUTTON_RECT[1] + 2),
            "ススム",
        )

        # エントリーフレーム
        self.entrys.draw()


# __ __ __ __ __ __ __ ゲームマネージャー __ __ __ __ __ __ __
class Game_Progress_Manager(Scene):
    NAME = "GAME_PROGRESS_MANAGER"

    def __init__(self):
        """
        1.スタート画面
        2.プレイヤー人数の設定
        3.プレイヤーネームの設定
        """
        self.turn = (Start_Screen, Player_Number_Screen, Player_Name_Screen)

        self.now_screen = self.turn[0]()

    def update(self):
        """スタートアップの設定を行う

        Returns:
            _list_: プレイヤーの名前
        """
        result = self.now_screen.update()

        if result:
            if self.now_screen.NAME == "START":
                self.now_screen = self.turn[1]()
            elif self.now_screen.NAME == "NUMBER":
                self.now_screen = self.turn[2](result)
            elif self.now_screen.NAME == "NAME":
                # こここにゲーム進行マネージャーを登録
                Game_Manager.set_scene(Start_Up_Manager(result))

    def draw(self):
        self.now_screen.draw()


@dataclass
class Player:
    number: int
    name: str
    score: int = 0
    answer: str = ""
    is_werewolf: bool = False

    def reset_answer(self):
        self.answer = ""


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
# キーボード外枠の座標
ALL_KEY_BORD_RECT = (
    0,
    KEY_BORD_RECTS["ア"][1] - (KEY_BORD_SIZE[1] + KEY_BORD_PADDING) - 1,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
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
# Enterキーのキーボード座標
ENTER_KEY_BORD_RECTS = (
    KEY_BORD_RECTS["ハ"][0] + KEY_BORD_PADDING + KEY_BORD_SIZE[0],
    KEY_BORD_RECTS["ハ"][1],
    KEY_BORD_SIZE[0],
    KEY_BORD_SIZE[1] * 3 + KEY_BORD_PADDING * 2,
)
# スペースキーのキーボード座標
SPACE_KEY_BORD_RECTS = (
    X,
    KEY_BORD_RECTS["タ"][1],
    KEY_BORD_SIZE[0],
    KEY_BORD_SIZE[1] * 3 + KEY_BORD_PADDING * 2,
)
# かな切り替えのキーボード座標
HIRAGANA_KEY_BORD_RECTS = (
    X,
    KEY_BORD_RECTS["ア"][1],
    KEY_BORD_SIZE[0],
    KEY_BORD_SIZE[1],
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
# キーボードイラスト セーブ座標
SMALL_KEY_SAVE_RECT = 0, 40
OTHER_KEY_SAVE_RECT = 8, 40
DELETE_KEY_SAVE_RECT = 16, 40
RETURN_SAVE_RECT = 24, 40
# ひらがなのカタカナ変換
CHANGE_HIRAGANA_LINE = {
    "ア": "あいうえお",
    "カ": "かきくけこ",
    "サ": "さしすせそ",
    "タ": "たちつてと",
    "ナ": "なにぬねの",
    "ハ": "はひふへほ",
    "マ": "まみむめも",
    "ヤ": "やゆよ",
    "ラ": "らりるれろ",
    "ワ": "わおん",
    "゛": "゛゜ー",
}
JAPANESE_SYLLABARY_HIRAGANA = (
    # 1列目
    "あいうえお",
    "かきくけこ",
    "さしすせそ",
    # 2列目
    "たちつてと",
    "なにぬねの",
    "はひふへほ",
    # 3列目
    "まみむめも",
    "やゆよ",
    "らりるれろ",
    # 4列目
    "わをん",
    "゛゜ー",
)


class Entry_Flame_Manager:
    def __init__(self, rect_x, rect_top, rect_under, number):
        # 入力フォームのx座標
        self.name_entry_rects_x = rect_x
        # 上限下限
        self.rect_top = rect_top
        self.rect_under = rect_under
        # 入力フォームの数
        self.player_number = number

        self.name_entry_rects_y = list(
            int(
                (self.rect_under - self.rect_top) / self.player_number * i
                + self.rect_top
            )
            for i in range(self.player_number)
        )  # ジェネレータのままだとインデックスアクセスできないので、リストに変換する。

        # 入力フォーム（インスタンス）を作成
        self.entrys = [
            Entry_Flame([self.name_entry_rects_x, self.name_entry_rects_y[i]], i)
            for i in range(self.player_number)
        ]

        # 現在アクティブな入力フォーム番号
        self.active_flame = None

    def update(self):
        """キーボード表示時に3番目に表示されるフレームをクリックすると、
        下のフレームが同一ループ内で連続的にactiveになっていくため、
        一番下のフレームまで連続的に選択することになってしまう。

        break で1ループ中に一回のみ反応するようにする"""

        for number, i in enumerate(self.entrys):
            result_1 = i.update()
            if result_1 == "active":
                only_per_flame = False
                self.active_flame = number
                self.change_flame_rect()

                break

            elif result_1 == "enter":
                for i in self.entrys:
                    i.reset_rect()

    def change_flame_rect(self):

        number = 3
        if self.active_flame == 0:
            numbers = [i for i in range(number)]
        elif (self.player_number - (self.active_flame + 1)) <= 1:
            numbers = [self.player_number - (3 - i) for i in range(number)]
        else:
            numbers = [self.active_flame - (i - 1) for i in range(number)]

        rand = random.randint(0, 10000)

        rects_y = [
            int((ALL_KEY_BORD_RECT[1] - self.rect_top) / number * i + self.rect_top)
            for i in range(number)
        ]  # ジェネレータのままだとインデックスアクセスできないので、リストに変換する。

        n = 0
        for num, i in enumerate(self.entrys):
            if num in numbers:
                i.change_rect(rect=[self.name_entry_rects_x, rects_y[n]], is_show=True)
                n += 1
            else:
                i.change_rect()

    def get_entry(self):
        entrys = []
        for i in self.entrys:
            n = i.get_entry()
            entrys.append(n)

        return entrys

    def draw(self):
        for i in self.entrys:
            i.draw()


class Entry_Flame:
    instances = []  # 全てのインスタンスを収納するリスト
    active = False

    def __init__(self, rect: list[int], number, max_count=10):
        """文字入力フォームを作成

        Args:
            rect (_list[int]_): (x, y, w, h) ※ w, h がない時は 8 * self.max_count, 10を入力
            max_count (int, optional): _description_. Defaults to 10.
        """
        self.original_rect = rect
        if len(self.original_rect) == 2:
            self.original_rect.append(8 * max_count)
            self.original_rect.append(10)
        self.rect = copy.copy(self.original_rect)
        self.number = number
        self.max_count = max_count
        self.entry: str = None
        self.keybord = KEY_BORD_Manager()

        self.is_show = True
        self.active = False
        Entry_Flame.instances.append(self)

        self.count = 0

    @classmethod
    def change_active(cls, instance):
        """指定されたインスタンスだけ `active=True` にし、他を `False` にする"""
        for obj in cls.instances:
            obj.active = False  # すべて `False` にする
        instance.active = True  # 指定されたインスタンスだけ `True` にする

        cls.active = True

    def change_rect(self, rect=[0, 0], is_show=False):
        self.is_show = is_show
        if self.is_show:
            self.rect = rect
            if len(self.rect) == 2:
                self.rect.append(8 * 10)
                self.rect.append(10)

    def reset_rect(self):
        self.rect = copy.copy(self.original_rect)
        self.is_show = True

    def update(self):
        """_summary_

        Returns:
            active: エントリーフレームをクリック
            enter: エンターキーをクリック
        """

        # 非表示の時反応しない
        if not self.is_show:
            return

        # エントリーフレームクリック時
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
            if (
                self.rect[0] <= mouse_x <= self.rect[0] + self.rect[2]
                and self.rect[1] <= mouse_y <= self.rect[1] + self.rect[3]
            ):
                # キーボードが有効な時、キーボードの範囲と重なるフレームを押せないようにする
                if not (Entry_Flame.active and ALL_KEY_BORD_RECT[1] <= mouse_y):
                    # 自分だけをactiveにする
                    Entry_Flame.change_active(self)
                    return "active"

        # アクティブでなければ入力処理を行わない
        if not self.active:
            return

        # キーボード アップデート
        result = self.keybord.update()

        # 入力された信号の処理
        if isinstance(result, list):
            if result[0] == "detect":
                if self.entry:
                    if len(self.entry) < self.max_count:
                        self.entry += result[1]
                else:
                    self.entry = result[1]
        elif result == "small":
            if self.entry and self.entry[-1] in "アイウエオヤユヨツやゆよつ":

                small_kana_map = str.maketrans(
                    "アイウエオヤユヨツやゆよつ", "ァィゥェォャュョッゃゅょっ"
                )
                self.entry = self.entry[:-1] + self.entry[-1].translate(small_kana_map)

            elif self.entry and self.entry[-1] in "ァィゥェォャュョッゃゅょっ":

                big_kana_map = str.maketrans(
                    "ァィゥェォャュョッゃゅょっ", "アイウエオヤユヨツやゆよつ"
                )
                self.entry = self.entry[:-1] + self.entry[-1].translate(big_kana_map)
        elif result == "delete":
            if self.entry:
                if len(self.entry) == 1:
                    self.entry = None
                else:
                    self.entry = self.entry[:-1]
        elif result == "enter":
            self.active = False
            Entry_Flame.active = False
            return "enter"
        elif result == "space":
            if self.entry:
                if len(self.entry) < self.max_count:
                    self.entry += " "
                else:
                    self.entry = " "

    def draw(self):
        if not self.is_show:
            return

        # 入力枠
        pyxel.rectb(
            self.rect[0],
            self.rect[1],
            self.rect[2],
            self.rect[3],
            COLOR_PALETTE["青"],
        )

        # 数字
        pyxel.blt(
            0,
            self.rect[1],
            0,
            NUMBER_SAVE_RECT[self.number + 1][0],
            NUMBER_SAVE_RECT[self.number + 1][1],
            8,
            8,
            0,
        )

        # 入力された文字を表示
        if self.entry:
            draw_text((self.rect[0], self.rect[1] + 1), self.entry)

        # アクティブな時だけ描写
        if self.active:
            self.count = (self.count + 1) % 20
            if self.count <= 10:

                if self.entry:
                    x = 8 * len(self.entry)
                else:
                    x = 0

                pyxel.rectb(
                    self.rect[0] + 2 + x,
                    self.rect[1] + 1,
                    2,
                    8,
                    COLOR_PALETTE["青"],
                )

            self.keybord.draw()

    def get_entry(self):
        return self.entry


class KEY_BORD_Manager:
    def __init__(self):
        self.key_bords = []
        for i in JAPANESE_SYLLABARY:
            self.key_bords.append(Key_Bord(i))

        self.hiragana_key_bords = []
        for i in JAPANESE_SYLLABARY:
            self.hiragana_key_bords.append(Hiragana_Key_Bord(i))

        self.now_hiragana = True

        # その他キーボード
        self.small_key = Small_Key()
        self.delete_key = Delet_Key()
        self.enter_key = Enter_Key()
        self.space_key = Space_Key()
        self.kana_key = Hiragana_Key()

        self.hold_key = None

    def update(self):

        # 　通常のキー監視
        is_hold = False

        if self.now_hiragana:
            for i in self.hiragana_key_bords:
                result = i.update(self.hold_key)
                if isinstance(result, list):
                    self.hold_key = None
                    return result
                elif result:
                    is_hold = True
                    self.hold_key = result
        else:
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

        # 小文字・デリート・エンターキー監視
        result_1 = self.small_key.update(self.hold_key)
        if result_1:
            return result_1
        result_2 = self.delete_key.update(self.hold_key)
        if result_2:
            return result_2
        result_3 = self.enter_key.update(self.hold_key)
        if result_3:
            return result_3
        result_4 = self.space_key.update(self.hold_key)
        if result_4:
            return result_4
        result_5 = self.kana_key.update(self.hold_key)
        if result_5:
            self.now_hiragana = not self.now_hiragana

    def draw(self):

        # キーボードの枠
        pyxel.rect(
            ALL_KEY_BORD_RECT[0],
            ALL_KEY_BORD_RECT[1],
            ALL_KEY_BORD_RECT[2],
            ALL_KEY_BORD_RECT[3],
            COLOR_PALETTE["紺"],
        )
        pyxel.rect(
            ALL_KEY_BORD_RECT[0],
            ALL_KEY_BORD_RECT[1],
            ALL_KEY_BORD_RECT[2],
            1,
            COLOR_PALETTE["薄緑"],
        )

        # キー描画
        if self.now_hiragana:
            for i in self.hiragana_key_bords:
                i.draw()
        else:
            for i in self.key_bords:
                i.draw()
        self.small_key.draw()
        self.delete_key.draw()
        self.enter_key.draw()
        self.space_key.draw()
        self.kana_key.draw()

        # "イウエオ" キー描画
        if self.now_hiragana:
            for i in self.hiragana_key_bords:
                i.second_draw()
        else:
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
                self.select_key = self.line[0]
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
            # 文字
            if self.key == "゛":
                pyxel.blt(
                    self.rects[0][0],
                    self.rects[0][1],
                    0,
                    OTHER_KEY_SAVE_RECT[0],
                    OTHER_KEY_SAVE_RECT[1],
                    8,
                    8,
                    0,
                )

            else:
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


class Hiragana_Key_Bord(Key_Bord):
    def __init__(self, line):
        super().__init__(line)

        self.line = CHANGE_HIRAGANA_LINE[self.key]


class Small_Key:
    def __init__(self):
        self.key = "small"

        self.rect = (
            SMALL_LETTER_KEY_BORD_RECTS[0],
            SMALL_LETTER_KEY_BORD_RECTS[1],
            KEY_BORD_SIZE[0],
            KEY_BORD_SIZE[1],
        )

        self.image_save_rect = SMALL_KEY_SAVE_RECT

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
                return self.key

    def draw(self):
        if self.active:
            pyxel.rectb(
                self.rect[0],
                self.rect[1],
                self.rect[2],
                self.rect[3],
                COLOR_PALETTE["薄緑"],
            )
            pyxel.blt(
                self.rect[0],
                self.rect[1],
                0,
                self.image_save_rect[0],
                self.image_save_rect[1],
                8,
                8,
                0,
            )

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

        self.image_save_rect = DELETE_KEY_SAVE_RECT


class Hiragana_Key(Small_Key):
    def __init__(self):
        super().__init__()
        self.key = "hiragana"

        self.rect = (
            HIRAGANA_KEY_BORD_RECTS[0],
            HIRAGANA_KEY_BORD_RECTS[1],
            HIRAGANA_KEY_BORD_RECTS[2],
            HIRAGANA_KEY_BORD_RECTS[3],
        )

        self.image_save_rect = 160, 160


class Enter_Key(Small_Key):
    def __init__(self):
        super().__init__()
        self.key = "enter"

        self.rect = (
            ENTER_KEY_BORD_RECTS[0],
            ENTER_KEY_BORD_RECTS[1],
            ENTER_KEY_BORD_RECTS[2],
            ENTER_KEY_BORD_RECTS[3],
        )

        self.image_save_rect = RETURN_SAVE_RECT


class Space_Key(Small_Key):
    def __init__(self):
        super().__init__()
        self.key = "space"

        self.rect = (
            SPACE_KEY_BORD_RECTS[0],
            SPACE_KEY_BORD_RECTS[1],
            SPACE_KEY_BORD_RECTS[2],
            SPACE_KEY_BORD_RECTS[3],
        )

        # 画像を表示しない
        self.image_save_rect = (160, 160)


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
        if i in HIRAGANA_TEXT_SAVE_RECT:
            pyxel.blt(
                rect[0] + number * 8,
                rect[1],
                0,
                HIRAGANA_TEXT_SAVE_RECT[i][0],
                HIRAGANA_TEXT_SAVE_RECT[i][1],
                8,
                8,
                0,
            )

        number += 1


quiz_light = [["シュミ ハ ナニ"], ["サイキンノ タノシミ"]]


"""

Q3: "実は苦手な食べ物や飲み物は？",
        Q4: "休日の過ごし方？",
        Q5: "好きな映画や音楽のジャンルは何ですか？",
        Q6: "あなたが最近買って良かったものは？",
        Q7: "研究のモチベーションは？",
        Q8: "バイトは？",
        Q9: "一日の中で一番好きな時間帯は？",
        Q10: "小さい頃の思い出の場所はどこですか？"
]

quiz_nomal = {
        Q1: "あなたが大切にしている価値観は何ですか？",
        Q2: "人生の中で一番印象に残っている経験は？",
        Q3: "今後挑戦してみたいことはありますか？",
        Q4: "あなたにとって理想の休暇とは？",
        Q5: "自分を一言で表すなら、どんな性格だと思いますか？",
        Q6: "最近達成した目標や、頑張ったことは何ですか？",
        Q7: "あなたがよく考える将来の夢や目標は？",
        Q8: "あなたが周りの人に与えたい影響は何ですか？",
        Q9: "あなたの友人や家族は、どんな人だと言いますか？",
        Q10: "あなたが普段気をつけている健康習慣は何ですか？"
    };

    let quiz_deep = {
        Q1: "あなたにとって「幸せ」とはどんなものですか？",
        Q2: "あなたが大きな壁に直面したとき、どう対処しますか？",
        Q3: "自分の中で最も大切だと感じる信念や信条は？",
        Q4: "あなたが一番恐れているものは何ですか？",
        Q5: "人生で最も後悔していることは？",
        Q6: "自分自身をもっと成長させたい分野やスキルは？",
        Q7: "あなたが困難に直面したときに支えになるものは？",
        Q8: "あなたがこれまでに経験した最も幸せな瞬間は？",
        Q9: "あなたの人生において、誰が一番影響を与えましたか？",
        Q10: "将来の自分に向けて、どんなメッセージを送りたいですか？"
"""

answer = [
    [
        """ギター ゲーム リョコウ エイガカンショウ ドクショ リョウリ シャシンサツエイ ツリ エイガカンショウ
オンガクカンショウ サンポ ジテンシャ カラオケ ダンス ボルダリング
スポーツカンセン アートカンショウ スポーツ ピクニック ペットトアソブ"""
    ],
    [],
]
App()
