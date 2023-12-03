
from glob import glob
from progressbar import progressbar
import random
from PIL import Image, ImageStat, ImageChops
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

def rms_get_score(image_a, image_b):
    im_a_file = Image.open(image_a)
    im_b_file = Image.open(image_b)

    stat_a = ImageStat.Stat(im_a_file)
    stat_b = ImageStat.Stat(im_b_file)

    difference = math.fabs(stat_a.rms[0] - stat_b.rms[0])/(stat_a.rms[0])

    return(1-difference)

def histogram_get_score(image_a, image_b):
    image_a_file = Image.open(image_a)
    image_b_file = Image.open(image_b)

    h = ImageChops.difference(image_a_file, image_b_file).histogram()
    val = math.sqrt(sum(h*(i**2) for i, h in enumerate(h)) / (float(image_a_file.size[0]) * image_b_file.size[1]))
    difference = val/100

    return(1-difference)

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

    highest_sum_match = ScoreEntry(0, "", "")
    highest_rms_match = ScoreEntry(0, "", "")
    highest_histogram_match = ScoreEntry(0, "", "")

    for i in progressbar(range(i)):
        f_png = random.choice(f_pngs)

        for s_png in s_pngs:
            sum_score = sum_get_score(f_png, s_png)
            if sum_score >= highest_sum_match.score:
                highest_sum_match = ScoreEntry(sum_score, f_png, s_png)

            rms_score = rms_get_score(f_png, s_png)
            if rms_score >= highest_rms_match.score:
                highest_rms_match = ScoreEntry(rms_score, f_png, s_png)

            histogram_score = histogram_get_score(f_png, s_png)
            if histogram_score >= highest_histogram_match.score:
                highest_histogram_match = ScoreEntry(histogram_score, f_png, s_png)


        sum_pair = get_gender_and_class(highest_sum_match.f_file, highest_sum_match.s_file)
        rms_pair = get_gender_and_class(highest_rms_match.f_file, highest_rms_match.s_file)
        histogram_pair = get_gender_and_class(highest_histogram_match.f_file, highest_histogram_match.s_file)
        print()

        if sum_pair.f_class == sum_pair.s_class and (rms_pair.f_class == rms_pair.s_class or histogram_pair.f_class == histogram_pair.s_class):
            real_matches += 1
        else:
            false_positives += 1

    print("matches: " + str(real_matches))
    print("false positives: " + str(false_positives))

main()