import PyxelUniversalFont as puf  # type: ignore

TEXT_FONT = puf.Writer("mymod/fonts/x12y12pxMaruMinya.ttf")

ISSUCCESS = False

if TEXT_FONT:
    ISSUCCESS = True
