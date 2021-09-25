# Works Cited
# https://www.blog.pythonlibrary.org/2018/04/12/adding-svg-files-in-reportlab/
# https://www.kite.com/python/answers/how-to-save-a-dictionary-to-a-file-with-pickle-in-python#:~:text=Use%20pickle.,the%20dictionary%20in%20the%20file.


from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas as c
from svglib.svglib import svg2rlg
import pickle

import os, sys
from datetime import datetime
from math import ceil
import labanotation_data

PATH = "./labanotation_symbols/"
BEAT = 28.35
COL = {"right_support": 165, "left_support": 159.15, "right_leg": 180.5, "left_leg": 143.65,
       "right_body": None, "left_body": None, "right_arm": 193.25, "left_arm": 130.9}


def prep_staff(canvas):
    staff = svg2rlg(PATH + "staff_lines.svg")
    renderPDF.draw(staff, canvas, 0.75, 0.75)
    facing = svg2rlg(PATH + "downstagefacing.svg")
    renderPDF.draw(facing, canvas, 100, 170-BEAT)
    canvas.drawString(80, 170-BEAT, "4")
    canvas.drawString(80, 180-BEAT, "4")

def draw_symbol(lnd, canvas):
    print(lnd)
    try:
        renderPDF.draw(svg2rlg(PATH + f"{lnd.get_symbol()}.svg"),
                       canvas,
                       COL[lnd.get_column()],
                       170-BEAT + lnd.get_beat() * BEAT)
    except:
        pass


def number_measures(canvas, num):
    for measure in range(num):
        canvas.drawString(80, 180 + measure*BEAT*4, str(measure+1))

def finish_score(canvas, beats):
    barline = svg2rlg(PATH + "barline.svg")
    renderPDF.draw(barline, canvas, 136.67, 169.8 + (beats + (4-beats)%4)*BEAT)


def draw_score(lnd_list,name):
    timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    canvas = c.Canvas(f"./{name}_{timestamp}.pdf")
    prep_staff(canvas)

    beats = 0
    for staff in lnd_list:
        for lnd in staff:
            draw_symbol(lnd, canvas)
            if lnd.get_beat() > beats:
                beats = lnd.get_beat()

    number_measures(canvas, ceil(beats/4))
    finish_score(canvas, beats)
    canvas.save()


if __name__ == "__main__":
    pass
    # canvas = canvas.Canvas(PATH + "staff.pdf")
    # staff = svg2rlg(PATH + "staff_lines.svg")


    # rightforwardmiddle = svg2rlg(PATH + "rightforwardmiddle.svg")
    # leftforwardmiddle = svg2rlg(PATH + "leftforwardmiddle.svg")
    # renderPDF.draw(staff, canvas, 0.75, 0.75)
    # for i in range(8):
    #     renderPDF.draw(rightforwardmiddle, canvas, C["r_arm"], 170 + i*BEAT*2)
    # for i in range(8):
    #     renderPDF.draw(leftforwardmiddle, canvas, C["l_support"], 198.35 + i*BEAT*2)
    # canvas.save()
