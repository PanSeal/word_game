import pyxel

from .specification import ISSUCCESS

ISSUCCESS = False

WINDOW_WIDTH, WINDOW_HEIGHT = 200, 200


class Process:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)  # 初期化

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(2)

        pyxel.rect(20, 39, 30, 56, 1)

        if ISSUCCESS:
            pyxel.rect(30, 50, 40, 60, 6)
