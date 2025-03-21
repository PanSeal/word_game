import pyxel
import random
import math
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
    "ァィゥェォャュョッ゛゜ー？！"
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

# 数字のセーブ座標
NUMBER_SAVE_RECT = []
for i in range(10):
    NUMBER_SAVE_RECT.append((8 * i, 56))

NUMBERS_SAVE_RECT = {}
number_list = "0123456789."
for num, i in enumerate(number_list):
    NUMBERS_SAVE_RECT[i] = (8 * num, 56)

# 動物アイコンのセーブ座標
WOLF_SAVE_RECT = 0, 112
RED_WOLF_SAVE_RECT = 8, 112
CHARACTERS_SAVE_RECTS = {
    "human": (16, 112),
    "chicken": (24, 112),
    "cat": (32, 112),
    "goat": (40, 112),
    "sheep": (48, 112),
    "pig": (56, 112),
    "cow": (64, 112),
}
NPC_SAVE_RECT = (72, 112)

# アルファベットのセーブ座標
ALPHABET_TEXT_SAVE_RECT = {}
start_positions_3 = [("O", 0, 136), ("a", 0, 144), ("b", 0, 152)]
alpha_list = "ABCDEFGHIJKLMN" "OPQRSTUVWXYZ" "abcdefghijklmn" "opqrstuvwxyz"
x, y = 0, 128
for kana in alpha_list:
    # 特定の文字でリセット
    for start_kana, new_x, new_y in start_positions_3:
        if kana == start_kana:
            x, y = new_x, new_y

    HIRAGANA_TEXT_SAVE_RECT[kana] = (x, y)
    x += 8  # X座標を増やす


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)  # 初期化
        pyxel.load("word_game.pyxres")

        self.game_manager = Game_Manager
        self.game_manager.set_scene(Start_Up_Manager())
        #self.game_manager.set_scene(Maintenance_Manager())

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


# 開発時の仮想環境管理
class Maintenance_Manager(Scene):
    NAME = "MAINTENANCE_MANAGER"

    def __init__(self):
        super().__init__()

        players = [
            Player(0, "たかし"),
            Player(1, "さとし"),
            Non_Player_Character(2, "ひろし"),
        ]

        players[0].answer = "さとう"
        players[1].answer = "しお"
        players[2].answer = "しょうゆ"

        players[0].is_werewolf = True

        self.turn = [Vote_Werewolf_Screen, Vote_Result_Screen, Score_Result_Screen]

        self.turn = [Quiz_Random_Screen]

        # self.now_screen = self.turn[0](players)
        self.now_screen = self.turn[0]()

    def update(self):
        result = self.now_screen.update()
        if result:
            if self.now_screen.NAME == "VOTE_WEREWOLF":
                self.now_screen = self.turn[1](result)
            elif self.now_screen.NAME == "VOTE_RESULT":
                self.now_screen = self.turn[2](result)
            elif self.now_screen.NAME == "QUIZ_CHOOSE":
                print("成功")

    def draw(self):
        self.now_screen.draw()


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
                Game_Manager.set_scene(Game_Progress_Manager(result))

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

        Click_To_Continue.update()

    def draw(self):
        draw_text((self.text_rect[0], self.text_rect[1]), self.text)

        Click_To_Continue.draw()


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

P_NAME_S_ENTRY_RECT_X = 15


class Player_Name_Screen:
    NAME = "NAME"

    def __init__(self, number):
        self.player_number = number

        # アイコン
        icones = []
        icones_rect = list(CHARACTERS_SAVE_RECTS.items())  # 辞書をリストに変換
        for _ in range(self.player_number):
            index = random.randint(
                0, len(icones_rect) - 1
            )  # ランダムなインデックスを選択
            icone_key, icone_value = icones_rect.pop(index)
            icones.append(icone_key)

        # エントリーフレーム作成
        self.entrys = Entry_Flame_Manager(
            P_NAME_S_ENTRY_RECT_X,
            P_NAME_S_TEXT_RECTS_Y[1] + 8 + 2,
            P_NAME_S_NEXT_BUTTON_RECT[1],
            self.player_number,
            icones,
        )

        self.players = ["" for i in range(self.player_number)]

        self.all_entry = False

    def update(self):
        # エントリーフレームマネジャー
        self.entrys.update()
        self.players = self.entrys.get_entry()
        entryflame_is_active = self.entrys.check_is_active()

        if all(name for is_player, name in self.players):
            self.all_entry = True
        else:
            self.all_entry = False

        # 進む
        if (
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            and self.all_entry  # 全て入力されている
            and not entryflame_is_active  # 入力中でない
        ):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
            if (
                P_NAME_S_NEXT_BUTTON_RECT[0]
                <= mouse_x
                <= P_NAME_S_NEXT_BUTTON_RECT[0] + PNS_NEXT_BUTTON_RECT[2]
                and P_NAME_S_NEXT_BUTTON_RECT[1]
                <= mouse_y
                <= P_NAME_S_NEXT_BUTTON_RECT[1] + PNS_NEXT_BUTTON_RECT[3]
            ):
                return self.players

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

    def __init__(self, players):

        self.players = []
        for p_number, (is_player, p_name) in enumerate(players):
            if is_player:
                self.players.append(Player(p_number, p_name))
            else:
                self.players.append(Non_Player_Character(p_number, p_name))

        self.turn = (
            Game_Start_Screen,
            Quiz_Show_Screen,
            Answer_Input_Screen,
            Show_Zinrou_Answer_Screen,
            Vote_Werewolf_Screen,
            Vote_Result_Screen,
            Score_Result_Screen,
        )
        self.now_screen = self.turn[0](self.players)

    def update(self):
        result = self.now_screen.update()

        if result:
            if self.now_screen.NAME == "START":
                self.now_screen = self.turn[1]()
            elif self.now_screen.NAME == "QUIZ":
                self.now_screen = self.turn[2](self.players, result[0], result[1])
            elif self.now_screen.NAME == "ANSWER_INPUT":
                self.now_screen = self.turn[3](self.players)
            elif self.now_screen.NAME == "SHOW_ZINROU_ANSWER":
                self.now_screen = self.turn[4](self.players)
            elif self.now_screen.NAME == "VOTE_WEREWOLF":
                self.now_screen = self.turn[5](self.players)
            elif self.now_screen.NAME == "VOTE_RESULT":
                self.now_screen = self.turn[6](self.players)
            elif self.now_screen.NAME == "SCORE_RESULT":
                for i in self.players:
                    i.reset_date()
                self.now_screen = self.turn[1]()

    def draw(self):
        self.now_screen.draw()


class Player:
    def __init__(self, number, name):
        self.number = number
        self.icone = None
        self.name = name
        self.attribute = "player"
        self.score = []
        self.vote = None
        self.answer = ""
        self.is_werewolf = False

    def reset_date(self):
        self.vote = None
        self.answer = ""
        self.is_werewolf = False

    def print_information(self):
        print(
            self.number, self.name, self.score, self.vote, self.answer, self.is_werewolf
        )


class Non_Player_Character(Player):
    def __init__(self, number, name):
        super().__init__(number, name)
        self.attribute = "non_player"

    def make_answer(self, quiz_number):
        self.answer = random.choice(ANSWER_LIGHT[quiz_number])


class Game_Start_Screen:
    NAME = "START"

    def __init__(self, plyers):
        self.players = plyers

        # 入力フォームのx座標
        self.name_rects_x = 10
        # 上限下限
        self.rect_top = 10
        self.rect_under = 150
        # 入力フォームの数
        self.player_number = len(plyers)

        self.name_rects_y = list(
            int(
                (self.rect_under - self.rect_top) / self.player_number * i
                + self.rect_top
            )
            for i in range(self.player_number)
        )

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return True

        Click_To_Continue.update()

    def draw(self):

        for i, player in enumerate(self.players):
            draw_text((self.name_rects_x, self.name_rects_y[i]), player.name)

        Click_To_Continue.draw()


CARD_W = 40
CARD_H = 16
CARD_Y_PADDING = 7
CARD_RECTS = []
for n in range(2):
    for m in range(5):
        CARD_RECTS.append(
            (
                (5 + (CARD_W + 10) * n),
                (20 + (CARD_H + CARD_Y_PADDING) * m),
            )
        )


# 裏返したカードを選択
class Quiz_Chose_Screen:
    NAME = "QUIZ_CHOOSE"

    def __init__(self):

        self.title_rect = 5, 5
        self.title = "カート゛を せんたく"

        q_numbers = Quiz_Que.get_quiz_numbers()
        self.quiz_numbers = []
        for key in q_numbers:
            self.quiz_numbers.append(int(key[1]))

        self.selected_number = None

        self.button = PNS_NEXT_BUTTON_RECT

        self.count = 0
        self.count_start_flag = False

    def update(self):

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y

            # カード
            for rect in self.quiz_numbers:
                if (
                    CARD_RECTS[rect - 1][0]
                    <= mouse_x
                    <= CARD_RECTS[rect - 1][0] + CARD_W
                    and CARD_RECTS[rect - 1][1]
                    <= mouse_y
                    <= CARD_RECTS[rect - 1][1] + CARD_H
                ):
                    self.selected_number = rect

            # ボタン
            if (
                P_NAME_S_NEXT_BUTTON_RECT[0]
                <= mouse_x
                <= P_NAME_S_NEXT_BUTTON_RECT[0] + P_NAME_S_NEXT_BUTTON_RECT[2]
                and P_NAME_S_NEXT_BUTTON_RECT[1]
                <= mouse_y
                <= P_NAME_S_NEXT_BUTTON_RECT[1] + P_NAME_S_NEXT_BUTTON_RECT[3]
            ):
                self.count_start_flag = True

        if self.count_start_flag:
            self.count += 1
            if self.count > 90:
                return True

    def draw(self):

        # タイトル
        draw_text(self.title_rect, self.title)

        # カード
        for rect in self.quiz_numbers:

            # 赤枠
            if rect == self.selected_number and not 1 <= self.count <= 8:
                pyxel.rect(
                    CARD_RECTS[rect - 1][0] - 1,
                    CARD_RECTS[rect - 1][1] - 1,
                    CARD_W + 2,
                    CARD_H + 2,
                    COLOR_PALETTE["赤"],
                )

            rect_x = CARD_RECTS[rect - 1][0]
            rect_y = CARD_RECTS[rect - 1][1]
            width = CARD_W
            if 1 <= self.count <= 8 and rect == self.selected_number:
                width = max(
                    int(math.cos(math.pi * self.count / 8) * CARD_W), 1
                )  # カードが細くなっていく
                rect_x = CARD_RECTS[rect - 1][0] + int((CARD_W - width) / 2)
                rect_y = CARD_RECTS[rect - 1][1] + int(3)

            # カード本体
            pyxel.rect(
                rect_x,
                rect_y,
                width,
                CARD_H,
                COLOR_PALETTE["緑"],
            )

            if self.count > 10 and rect == self.selected_number:
                draw_text(CARD_RECTS[rect - 1], "もしれつ")
                draw_text(
                    (CARD_RECTS[rect - 1][0], CARD_RECTS[rect - 1][1] + 8), "もしれつ"
                )

        # 次に進むボタン
        if self.selected_number:
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


# クイズをランダムに選択
class Quiz_Random_Screen:
    NAME = "QUIZ_CHOOSE"

    def __init__(self):

        self.title_rect = 5, 5
        self.title = "ランタ゛ムにせんたく"

        self.original_quizes = Quiz_Que.get_quiz_list()
        self.quizes = []
        for i in self.original_quizes:
            self.quizes.append(self.original_quizes[i])
        self.max_quiz_number = len(self.quizes) - 1
        self.now_quiz_number = 0

        self.one_turn_count = 2

        self.count = 0
        self.click_flag = False

    def update(self):

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.click_flag = True

        if self.click_flag:
            return True

        if not self.click_flag:
            self.count = (self.count + 1) % self.one_turn_count
            if self.count == (self.one_turn_count - 1):
                self.now_quiz_number = (self.now_quiz_number + 1) % self.max_quiz_number

    def draw(self):

        # タイトル
        draw_text(self.title_rect, self.title)

        # クイズ
        if isinstance(self.quizes[self.now_quiz_number], tuple):
            for number, i in enumerate(self.quizes[self.now_quiz_number]):
                draw_text((5, 30 + 9 * number), i)
        else:
            draw_text((5, 30), self.quizes[self.now_quiz_number])

        # 次に進むボタン
        if True:
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


class Quiz_Show_Screen:
    NAME = "QUIZ"

    def __init__(self):
        self.quiz_number, self.now_quiz = Quiz_Que.get_quiz()

        self.text_rect_x = PNS_TEXT_RECT_X
        self.text_rects_y = PNS_TEXT_RECTS_Y

    def update(self):
        """クリック時に次のScreenに情報を渡す

        Returns:
            self.quiz_number
            self.now_quiz
        """

        Click_To_Continue.update()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return self.quiz_number, self.now_quiz

    def draw(self):
        # クイズテキスト
        if isinstance(self.now_quiz, tuple):
            for i, text in enumerate(self.now_quiz):
                draw_text((self.text_rect_x, self.text_rects_y[i]), text)
        else:
            draw_text((self.text_rect_x, self.text_rects_y[0]), self.now_quiz)

        Click_To_Continue.draw()


class Answer_Input_Screen:
    NAME = "ANSWER_INPUT"

    def __init__(self, players, quiz_number, now_quiz):
        self.players = players

        self.quiz_number = quiz_number
        self.now_quiz = now_quiz

        self.text_rect_x = PNS_TEXT_RECT_X
        self.text_rects_y = PNS_TEXT_RECTS_Y

        self.entry_flame_rect = [
            P_NAME_S_ENTRY_RECT_X,
            P_NAME_S_TEXT_RECTS_Y[1] + 16 + 2,
        ]

        self.now_answer_player_number = 0
        self.now_entry_flame = Entry_Flame(
            self.entry_flame_rect,
            0,
            icone=self.players[self.now_answer_player_number].icone,
        )

    def update(self):
        self.now_entry_flame.update()

        # 進む
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
            if (
                PNS_NEXT_BUTTON_RECT[0]
                <= mouse_x
                <= PNS_NEXT_BUTTON_RECT[0] + PNS_NEXT_BUTTON_RECT[2]
                and PNS_NEXT_BUTTON_RECT[1]
                <= mouse_y
                <= PNS_NEXT_BUTTON_RECT[1] + PNS_NEXT_BUTTON_RECT[3]
            ):
                entry = self.now_entry_flame.get_entry()[1]
                self.players[self.now_answer_player_number].answer = entry
                self.now_entry_flame = Entry_Flame(
                    self.entry_flame_rect,
                    0,
                    icone=self.players[self.now_answer_player_number].icone,
                )

                if self.now_answer_player_number >= len(self.players) - 1:
                    return True
                elif self.now_answer_player_number == 1 and len(self.players) == 3:
                    self.players[2].make_answer(self.quiz_number)

                    return True
                else:
                    self.now_answer_player_number += 1

    def draw(self):
        # クイズテキスト
        if isinstance(self.now_quiz, tuple):
            for i, text in enumerate(self.now_quiz):
                draw_text((self.text_rect_x, self.text_rects_y[i]), text)
        else:
            draw_text((self.text_rect_x, self.text_rects_y[0]), self.now_quiz)

        # プレイヤー名
        draw_text(
            (self.text_rect_x, self.text_rects_y[1] + 2 + 8),
            self.players[self.now_answer_player_number].name,
        )

        # エントリーフレーム
        self.now_entry_flame.draw()

        # 次に進むボタン
        if True:
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


class Show_Zinrou_Answer_Screen:
    NAME = "SHOW_ZINROU_ANSWER"

    def __init__(self, players):
        self.zinrou = self.random_choice_zinrou(players)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return True

        Click_To_Continue.update()

    def draw(self):
        draw_text((10, 100), self.zinrou.answer)

        Click_To_Continue.draw()

    def random_choice_zinrou(self, players):
        zinrou = random.choice(players)
        zinrou.is_werewolf = True

        return zinrou


class Vote_Werewolf_Screen:
    NAME = "VOTE_WEREWOLF"

    def __init__(self, players):
        self.players = players
        for i in self.players:
            if i.is_werewolf:
                self.werewolf = i
                break

        self.text = "し゛んろうは た゛れ？"

        self.text_rect_x = PNS_TEXT_RECT_X
        self.text_rects_y = PNS_TEXT_RECTS_Y

        self.now_answer_player_number = 0
        self.now_vote = Individual_Vote_Zinrou(
            self.players, self.players[self.now_answer_player_number]
        )

    def update(self):
        result = self.now_vote.update()
        if result:
            result_1 = self.next_vote_player()
            if result_1:
                return self.players

    def next_vote_player(self):

        self.now_answer_player_number += 1

        # プレイヤーの人数以上
        if self.now_answer_player_number >= len(self.players):
            return True
        elif self.players[self.now_answer_player_number].attribute == "non_player":
            return True
        else:
            self.now_vote = Individual_Vote_Zinrou(
                self.players, self.players[self.now_answer_player_number]
            )

    def draw(self):
        # せつめいテキスト
        draw_text((self.text_rect_x, self.text_rects_y[0]), self.text)

        self.now_vote.draw()

        # 次に進むボタン
        if True:
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


class Individual_Vote_Zinrou:
    def __init__(self, players, player):

        # 全てのプレイヤー
        self.players = players
        # 投票するプレイヤー
        self.vote_player = player

        self.player_number = len(players)

        self.text_rect_x = PNS_TEXT_RECT_X
        self.text_rects_y = PNS_TEXT_RECTS_Y

        self.select_number = None

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y

            # 人数 円
            n = 0
            for i in range(self.player_number):
                if self.players[i] == self.vote_player:
                    pass
                else:
                    if (
                        5 <= mouse_x <= 5 + CIRCLE_DIAMETER
                        and CIRCLE_RECTS_Y[n]
                        <= mouse_y
                        <= CIRCLE_RECTS_Y[n] + CIRCLE_DIAMETER
                    ):
                        self.select_number = i

                    n += 1

            # 進む
            if (
                PNS_NEXT_BUTTON_RECT[0]
                <= mouse_x
                <= PNS_NEXT_BUTTON_RECT[0] + PNS_NEXT_BUTTON_RECT[2]
                and PNS_NEXT_BUTTON_RECT[1]
                <= mouse_y
                <= PNS_NEXT_BUTTON_RECT[1] + PNS_NEXT_BUTTON_RECT[3]
            ):
                self.vote_player.vote = self.select_number
                return True

    def draw(self):

        # 名前
        draw_text(
            (CIRCLE_RECT_X, CIRCLE_RECTS_Y[0] - 8 - 2),
            f"{self.vote_player.name}のとうひょう",
        )

        # 投票
        n = 0
        for i in range(self.player_number):
            if self.players[i] == self.vote_player:
                pass
            else:
                # 円
                pyxel.circ(
                    5 + int(CIRCLE_DIAMETER / 2),
                    CIRCLE_RECTS_Y[n] + int(CIRCLE_DIAMETER / 2),
                    int(CIRCLE_DIAMETER / 2),
                    COLOR_PALETTE["白"],
                )
                if self.select_number == i:
                    pyxel.circ(
                        5 + int(CIRCLE_DIAMETER / 2),
                        CIRCLE_RECTS_Y[n] + int(CIRCLE_DIAMETER / 2),
                        int(CIRCLE_DIAMETER / 2) - 1,
                        COLOR_PALETTE["桃"],
                    )

                # 名前
                draw_text(
                    (15, CIRCLE_RECTS_Y[n]),
                    self.players[i].name,
                )

                n += 1

        # 人狼への説明コメント
        pyxel.blt(
            13,
            CIRCLE_RECTS_Y[self.player_number - 1] - 4,
            0,
            WOLF_SAVE_RECT[0],
            WOLF_SAVE_RECT[1],
            8,
            8,
        )
        pyxel.text(
            23,
            CIRCLE_RECTS_Y[self.player_number - 1] - 4,
            "opponent is not",
            COLOR_PALETTE["白"],
        )
        pyxel.text(
            55,
            CIRCLE_RECTS_Y[self.player_number - 1] + 2,
            "a werewolf",
            COLOR_PALETTE["白"],
        )


class Vote_Result_Screen:
    NAME = "VOTE_RESULT"

    def __init__(self, players):
        self.all_players = players

        self.players = []
        self.non_player = None
        for i in players:
            if i.attribute == "player":
                self.players.append(i)
            else:
                self.non_player = i

        self.count = 0
        self.show_flag = False

        for i in self.players:
            if i.is_werewolf:
                self.werewolf = i

    def update(self):
        if self.count <= 30:
            self.count += 1
        else:
            self.show_flag = True

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return self.all_players

        Click_To_Continue.update()

    def draw(self):
        for number, i in enumerate(self.players):
            draw_text((5, 30 * (number + 1)), f"{i.name} は")
            for n in self.all_players:
                if i.vote == n.number:
                    draw_text((15, 30 * (number + 1) + 10), f"{n.name} にとうひょう")

        if self.non_player:
            draw_text((5, 30 * len(self.all_players)), f"{self.non_player.name} ")

        if self.show_flag:
            draw_text((10, 120), f"し゛んろうは {self.werewolf.name}")

        Click_To_Continue.draw()


SCORE_ONE = 1  # 2人プレイの時、相手が人狼であると見破った時の点数
SCORE_TWO = 0.5  # 2人プレイの時、相手が人狼でないと見破った時の点数（自分は人狼）


class Score_Result_Screen:
    NAME = "SCORE_RESULT"

    def __init__(self, players):
        self.all_players = players

        self.players = []
        self.non_player = None
        for i in players:
            if i.attribute == "player":
                self.players.append(i)
            else:
                self.non_player = i

        for i in self.players:
            if i.is_werewolf:
                self.werewolf = i

        self.player_number = len(self.players)

        self.caluculate_score()

    def caluculate_score(self):
        if self.player_number == 2:
            score = []

            for player in self.players:
                # 人狼でない人の投票
                if player.is_werewolf == False:
                    if player.vote == self.werewolf.number:
                        player.score.append(SCORE_ONE)
                    else:
                        player.score.append(0)
                # 人狼による投票
                else:
                    # 2人目の人狼に投票
                    if (
                        self.all_players[player.vote].is_werewolf
                        and not self.all_players[player.vote] == self.werewolf
                    ):
                        player.score.append(SCORE_ONE)
                    elif len(self.players) == 2:
                        for n in self.players:
                            if not player.name == n.name:
                                another_player = n

                        if (
                            another_player.is_werewolf == False
                            and self.all_players[player.vote].name
                            == self.non_player.name
                        ):
                            player.score.append(SCORE_TWO)
                        else:
                            player.score.append(0)
                    else:
                        player.score.append(0)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return True

        Click_To_Continue.update()

    def draw(self):
        draw_text((5, 5), "とくてん")
        draw_text((5, 15), "フ゜レイヤー とくてん こ゛うけい")

        for number, i in enumerate(self.players):
            draw_text(
                (5, 30 * (number + 1)), f"{i.name}  {i.score[-1]}  {sum(i.score)}"
            )

        Click_To_Continue.draw()


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
    def __init__(self, rect_x, rect_top, rect_under, number, icones):
        # 入力フォームのx座標
        self.name_entry_rects_x = rect_x
        # 上限下限
        self.rect_top = rect_top
        self.rect_under = rect_under

        # プレイヤー人数
        self.player_number = number

        # 入力フォームの数
        self.entry_flame_number = number
        if number == 2:
            self.entry_flame_number = 3
        # エントリーフレームのy座標
        self.name_entry_rects_y = list(
            int(
                (self.rect_under - self.rect_top) / self.entry_flame_number * i
                + self.rect_top
            )
            for i in range(self.entry_flame_number)
        )  # ジェネレータのままだとインデックスアクセスできないので、リストに変換する。

        # 入力フォーム（インスタンス）を作成
        self.entrys = [
            Entry_Flame(
                [self.name_entry_rects_x, self.name_entry_rects_y[i]],
                i,
                icone=icones[i],
            )
            for i in range(self.player_number)
        ]
        # 2人プレイのときNPC用入力フォーム（インスタンス）を追加
        if number == 2:
            self.entrys.append(
                Entry_Flame(
                    [self.name_entry_rects_x, self.name_entry_rects_y[2]],
                    2,
                    is_player=False,
                    icone="npc",
                )
            )

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
                self.active_flame = number
                self.change_flame_rect()

                break

            elif result_1 == "enter":
                self.active_flame = None
                for i in self.entrys:
                    i.reset_rect()

    def change_flame_rect(self):

        number = 3  # キーボード表示中に表示するエントリーフレームの数
        if self.active_flame == 0:
            numbers = [i for i in range(number)]
        elif (self.entry_flame_number - (self.active_flame + 1)) <= 1:
            numbers = [self.entry_flame_number - (3 - i) for i in range(number)]
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

    def check_is_active(self):
        return self.active_flame

    def draw(self):
        for i in self.entrys:
            i.draw()


class Entry_Flame:
    instances = []  # 全てのインスタンスを収納するリスト
    active = False

    def __init__(
        self,
        rect: list[int],
        number,
        max_count=10,
        is_player=True,
        icone=None,
    ):
        """文字入力フォームを作成

        Args:
            rect (_list[int]_): (x, y, w, h) ※ w, h がない時は 8 * self.max_count, 10を入力
            max_count (int, optional): _description_. Defaults to 10.
        """
        # 座標
        self.original_rect = rect
        if len(self.original_rect) == 2:
            self.original_rect.append(8 * max_count)
            self.original_rect.append(10)
        self.rect = copy.copy(self.original_rect)
        # 番号
        self.number = number
        # 最大文字数
        self.max_count = max_count
        # デフォルトエントリー
        self.is_player = is_player
        if self.is_player:
            self.entry: str = None
        else:
            self.entry: str = "NPC"
        # インスタンス作成
        self.keybord = KEY_BORD_Manager()
        # アイコン
        self.icone = icone
        # エントリーフレームを表示する
        self.is_show = True
        # Trueのときキーボードを表示
        self.active = False
        # 自身を追加
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

        # アイコン
        if self.icone == "npc":
            pyxel.blt(
                5,
                self.rect[1],
                0,
                NPC_SAVE_RECT[0],
                NPC_SAVE_RECT[1],
                8,
                8,
                0,
            )
        else:
            pyxel.blt(
                5,
                self.rect[1],
                0,
                CHARACTERS_SAVE_RECTS[self.icone][0],
                CHARACTERS_SAVE_RECTS[self.icone][1],
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
        return (self.is_player, self.entry)


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


# __ __ __ __ __ __ __ グローバル関数 __ __ __ __ __ __ __
def draw_text(rect, strings):
    number = 0

    for i in strings:

        if i in TEXT_SAVE_RECT:
            pyxel.blt(
                rect[0] + int(number * 8),
                rect[1],
                0,
                TEXT_SAVE_RECT[i][0],
                TEXT_SAVE_RECT[i][1],
                8,
                8,
                0,
            )
        elif i in HIRAGANA_TEXT_SAVE_RECT:
            pyxel.blt(
                rect[0] + int(number * 8),
                rect[1],
                0,
                HIRAGANA_TEXT_SAVE_RECT[i][0],
                HIRAGANA_TEXT_SAVE_RECT[i][1],
                8,
                8,
                0,
            )
        elif i in NUMBERS_SAVE_RECT:
            pyxel.blt(
                rect[0] + int(number * 8),
                rect[1],
                0,
                NUMBERS_SAVE_RECT[i][0],
                NUMBERS_SAVE_RECT[i][1],
                8,
                8,
                0,
            )
        elif i in ALPHABET_TEXT_SAVE_RECT:
            pyxel.blt(
                rect[0] + int(number * 8),
                rect[1],
                0,
                ALPHABET_TEXT_SAVE_RECT[i][0],
                ALPHABET_TEXT_SAVE_RECT[i][1],
                8,
                8,
                0,
            )

        if i in ("."):
            number += 0.5
        else:
            number += 1


class Click_To_Continue:
    text = "click to continue"

    rect = WINDOW_WIDTH - (len(text) * 4 + 2), WINDOW_HEIGHT - 10

    tri_rect = [
        rect[0] - 9,
        rect[1] - 1,
        rect[0] - 1,
        rect[1] - 1,
        rect[0] - 5,
        rect[1] + 3,
    ]

    rect_change_y = 1
    count = 0.0

    @classmethod
    def update(cls):
        if not (cls.count % 10):
            for i in (1, 3, 5):
                cls.tri_rect[i] += cls.rect_change_y

        if cls.count >= 20:
            cls.rect_change_y = cls.rect_change_y * (-1)

        cls.count = (cls.count + 1) % 21

    @classmethod
    def draw(cls):
        pyxel.text(cls.rect[0], cls.rect[1], cls.text, COLOR_PALETTE["白"])

        pyxel.tri(
            cls.tri_rect[0],
            cls.tri_rect[1],
            cls.tri_rect[2],
            cls.tri_rect[3],
            cls.tri_rect[4],
            cls.tri_rect[5],
            COLOR_PALETTE["白"],
        )


# __ __ __ __ __ __ __ クイズ __ __ __ __ __ __ __
QUIZ_LIGHT = {
    "Q1": "しゅみは なに？",
    "Q2": ("さいきんの", "たのしみは？"),
    "Q3": ("し゛つはにか゛てな", "たへ゛もの のみもの"),
    "Q4": ("きゅうし゛つの", "すこ゛しかた"),
    "Q5": ("すきなえいか゛や", "おんか゛くシ゛ャンル"),
}


"""
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

ANSWER_LIGHT = {
    "Q1": """ギター,ゲーム,りょこう,えいがかんしょう,どくしょ,りょうり,しゃしん,つり,えいが,おんがくを きく,
さんぽ,じてんしゃ,カラオケ,ダンス,ボルダリング,スポーツかんせん,アートかんしょう,スポーツ,ピクニック,ペットとあそぶ,
ネットサーフィン,ぼんさい,さどう,けんどう,からて,あいきどう,おんがくフェス,ライブ,ポケモン,えをかく,
やきゅう,きょじん,はんしん,おんせん,さっかー,しゅげい,おりがみ,とざん,スキー,スノボ,
""".replace(
        "\n", ""
    ).split(
        ","
    ),
    "Q2": """カフェめぐり,ゲーム,さけ,たばこ,かいかつクラブ,まんが,おわらい,つり,べんとう,しごと,""".replace(
        "\n", ""
    ).split(
        ","
    ),
    "Q3": """アボカド,パクチー,コーヒー,セロリ,ブルーチーズ,なっとう,レバー,カキ,ウニ,ドリアン,
グリンピース,ピーマン,ゴーヤ,にがうり,ししゃも,チーズ,ラッキョウ,ミョウガ,しいたけ,たけのこ,
ぎゅうにゅう,うめぼし,ホルモン,カニみそ,アンチョビ,なまクリーム,にんにく,わさび,からし,チョコミント
""".replace(
        "\n", ""
    ).split(
        ","
    ),
    "Q4": """カフェめぐり,ゲーム,さけ,たばこ,ネットサーフィン,えいがかんしょう,ドライブ,サイクリング,キャンプ,どくしょ,
りょうり,しゃしんさつえい,スポーツかんせん,ジョギング,カラオケ,ダンス,ボルダリング,びじゅつかん,おんせんりょこう,つり,
アニメ,マンガ,ショッピング,ボードゲーム,とざん,しゅげい,ディー アイ ワイ,えんげい,ピクニック,ライブかんしょう
""".replace(
        "\n", ""
    ).split(
        ","
    ),
    "Q5": """アクション,ホラー,サスペンス,コメディ,ファンタジー,ミュージカル,ラブロマンス,ヒューマンドラマ,エスエフ,アニメ,
せんそうえいが,ドキュメンタリー,れきしえいが,スポーツえいが,ミステリー,はんざいえいが,アドベンチャー,スリラー,せいぶげき,モンスターえいが,
クラシック,ジャズ,ポップス,ロック,ヘビーメタル,ヒップホップ,あーる あんど びー,ブルース,テクノ,レゲエ
""".replace(
        "\n", ""
    ).split(
        ","
    ),
    "Q6": """,,,,,,,,,,""".replace("\n", "").split(","),
}


class Quiz_Que:
    quiz = copy.deepcopy(QUIZ_LIGHT)

    @classmethod
    def get_quiz(cls):
        if cls.quiz:
            key = random.choice(list(cls.quiz.keys()))  # ランダムなキーを取得
            question = cls.quiz.pop(key)

            return key, question
        else:
            print("クイズがありません")

    @classmethod
    def get_quiz_list(cls):
        if cls.quiz:
            return cls.quiz
        else:
            print("クイズがありません")

    @classmethod
    def get_particular_quiz(cls, quiz_number):
        cls.quiz.remove(quiz_number)

    @classmethod
    def get_quiz_numbers(cls):
        if cls.quiz:
            key = list(cls.quiz.keys())

            return key


""",,,,,,,,,,"""

App()
