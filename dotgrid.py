#!/usr/bin/python3
"""Generate PostScript to print dotgrid paper.

Generate PostScript which will print a dotgrid on A4 paper.

By default, an 8mm dotgrid is generated. The size can be overridden with
the --gridsize option.

The PostScript output can be piped into ps2pdf to generate PDF.

For example:

    python3 dotgrid.py --gridsize=8 | ps2pdf - >8mm-dotgrid.pdf
"""

import sys
import argparse
from numpy import linspace

default_grid_size = 8.0  # millimetres

a4_width = 210  # millimetres
a4_height = 297  # millimetres

point = 25.4/72  # millimetres

page_width = a4_width
page_height = a4_height

top_margin = 5  # millimetres
bottom_margin = top_margin  # millimetres
left_margin = 6.5  # millimetres
right_margin = left_margin  # millimetres


def main():
    set_grid_size_from_argument_or_default()
    (x_number_of_dots, x_grid_size) = fit_grid_size_to_printable_length(
            page_width,
            left_margin,
            right_margin)
    (y_number_of_dots, y_grid_size) = fit_grid_size_to_printable_length(
            page_height,
            bottom_margin,
            top_margin)
    print_grid_size_fitting_summary(x_grid_size, y_grid_size)
    print(postscript_header(grid_size))
    print(postscript_set_page_size(page_width, page_height))
    for page_number in [1, 2]:
        print_postscript_dotgrid_page(x_number_of_dots, y_number_of_dots)


def set_grid_size_from_argument_or_default():
    global grid_size

    parser = argparse.ArgumentParser()
    parser.add_argument('--gridsize', dest='grid_size',
                        default=default_grid_size,
                        type=float,
                        help='set the gridsize in millimetres')
    args = parser.parse_args()

    grid_size = args.grid_size


def print_grid_size_fitting_summary(x_grid_size, y_grid_size):
    sys.stderr.write(f'target grid size: {grid_size}\n')
    sys.stderr.write(f'    fitted x grid size: {x_grid_size}mm\n')
    sys.stderr.write(f'    fitted y grid size: {y_grid_size}mm\n')


def postscript_header(grid_size):
    postscript_header = f'''\
%!PS-Adobe-3.0
%%Creator: dotgrid.py
%%Title: A4 {grid_size}mm dotted grid double sided
%%EndComments
'''
    return postscript_header


def postscript_set_page_size(width, height):
    width_in_points = round(width / point)
    height_in_points = round(height / point)

    postscript_set_page_size = f'''\
<< /PageSize [{width_in_points} {height_in_points}] >> setpagedevice
'''
    return postscript_set_page_size


def print_postscript_dotgrid_page(x_number_of_dots, y_number_of_dots):
    print('0.8 setgray')

    for x in linspace(left_margin,
                      page_width - right_margin,
                      x_number_of_dots):
        for y in linspace(bottom_margin,
                          page_height - top_margin,
                          y_number_of_dots):
            x_in_points = x / point
            y_in_points = y / point
            print(postscript_draw_dot(x_in_points, y_in_points))

    print('showpage')


def postscript_draw_dot(x_in_points, y_in_points):
    rounded_x = round(x_in_points, 3)
    rounded_y = round(y_in_points, 3)
    postscript_draw_dot = f'''\
{rounded_x} {rounded_y} 0.75 0 360 arc closepath fill\
'''
    return postscript_draw_dot


def fit_grid_size_to_printable_length(length, margin1, margin2):
    printable_length = length - margin1 - margin2
    number_of_dots = printable_length / grid_size
    fitted_number_of_dots = round(number_of_dots)
    fitted_grid_size = printable_length / fitted_number_of_dots
    return (fitted_number_of_dots, fitted_grid_size)


if __name__ == "__main__":
    main()
