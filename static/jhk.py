from PIL.Image import open
from PIL import UnidentifiedImageError
from os.path import getsize,splitext
from os import walk,remove

for i, j, k in walk("test"):
    for c in k:
        x = f"{i}/{c}"
        if getsize(x) == 0:
            remove(x)
            continue
        try:
            a = open(x)
        except UnidentifiedImageError:
            print(x, "not image or can't read")
            continue
        e = splitext(c)[0].replace(".", "")
        d = i + '/' + e + ".webp"

        a.save(d,quality=100)
        if d != x:
            remove(x)
