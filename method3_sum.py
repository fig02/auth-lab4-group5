
from glob import glob
from progressbar import progressbar
import random
from PIL import Image, ImageStat
import math

class ScoreEntry:
    def __init__(self, score, f_file, s_file):
        self.score = score
        self.f_file = f_file
        self.s_file = s_file

class FingerPair:
    def __init__(self, f_gender, f_class, s_gender, s_class):
        self.f_gender = f_gender
        self.f_class = f_class
        self.s_gender = s_gender
        self.s_class = s_class


def sum_get_score(image_a, image_b):
    image_a_file = Image.open(image_a)
    image_b_file = Image.open(image_b)

    stat1 = ImageStat.Stat(image_a_file)
    stat2 = ImageStat.Stat(image_b_file)

    diff = math.fabs(stat1.sum2[0] - stat2.sum2[0])/(stat1.sum2[0])

    return(1-diff)

def get_gender_and_class(f_png_name, s_png_name):
    f_txt_name = f_png_name.replace("png", "txt")
    s_txt_name = s_png_name.replace("png", "txt")

    f_txt = open(f_txt_name, "r")
    s_txt = open(s_txt_name, "r")

    f_gender = f_txt.readline().split()[1]
    f_class = f_txt.readline().split()[1]
    s_gender = s_txt.readline().split()[1]
    s_class = s_txt.readline().split()[1]
    
    return FingerPair(f_gender, f_class, s_gender, s_class)

def main():
    f_pngs = glob("test/f*.png")
    s_pngs = glob("test/s*.png")

    false_positives = 0
    real_matches = 0
    i = 50
    highest_match = ScoreEntry(0, "", "")

    for i in progressbar(range(i)):
        f_png = random.choice(f_pngs)

        for s_png in s_pngs:
            score = sum_get_score(f_png, s_png)
            if score >= highest_match.score:
                highest_match = ScoreEntry(score, f_png, s_png)

        pair = get_gender_and_class(highest_match.f_file, highest_match.s_file)
        print()
        print(pair.f_gender + " " + pair.s_gender + " " + pair.f_class + " " + pair.s_class)
        if pair.f_class == pair.s_class:
            real_matches += 1
        else:
            false_positives += 1

    print("matches: " + str(real_matches))
    print("false positives: " + str(false_positives))

main()