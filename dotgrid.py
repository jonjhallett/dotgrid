#!/usr/bin/python3

import sys
import argparse

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
    x_grid_size = fit_grid_size_to_printable_length(page_width,
                                                    left_margin,
                                                    right_margin)
    y_grid_size = fit_grid_size_to_printable_length(page_height,
                                                    bottom_margin,
                                                    top_margin)
    print_grid_size_fitting_summary(x_grid_size, y_grid_size)
    print(postscript_header(grid_size))
    print(postscript_set_page_size(page_width, page_height))
    for page_number in [1, 2]:
        print_postscript_dotgrid_page(x_grid_size, y_grid_size)


def set_grid_size_from_argument_or_default():
    global grid_size

    parser = argparse.ArgumentParser()
    parser.add_argument("--gridsize", dest="grid_size",
                        default=default_grid_size,
                        type=float)
    args = parser.parse_args()

    grid_size = args.grid_size


def print_grid_size_fitting_summary(x_grid_size, y_grid_size):
    print_to_stderr(f'target grid size: {grid_size}')
    print_to_stderr(f'    fitted x grid size: {x_grid_size}mm')
    print_to_stderr(f'    fitted y grid size: {y_grid_size}mm')


def postscript_header(grid_size):
    postscript_header = f"""\
%!PS-Adobe-3.0
%%Creator: dotgrid.py
%%Title: A4 {grid_size}mm dotted grid double sided
%%EndComments
"""
    return postscript_header


def postscript_set_page_size(width, height):
    width_in_points = int(round(width / point))
    height_in_points = int(round(height / point))

    postscript_set_page_size = f"""\
<< /PageSize [{width_in_points} {height_in_points}] >> setpagedevice
"""
    return postscript_set_page_size


def print_postscript_dotgrid_page(x_grid_size, y_grid_size):
    print("0.8 setgray")

    for x in frange(left_margin,
                    page_width - right_margin + 1,
                    x_grid_size):
        for y in frange(bottom_margin,
                        page_height - top_margin + 1,
                        y_grid_size):
            x_in_points = truncate_to_3_decimal_points(x / point)
            y_in_points = truncate_to_3_decimal_points(y / point)
            print(postscript_draw_dot(x_in_points, y_in_points))

    print("showpage")


def postscript_draw_dot(x_in_points, y_in_points):
    postscript_draw_dot = f"""\
{x_in_points} {y_in_points} 0.75 0 360 arc closepath fill\
"""
    return postscript_draw_dot


def fit_grid_size_to_printable_length(length, margin1, margin2):
    printable_length = length - margin1 - margin2
    number_of_dots = printable_length / grid_size
    fitted_number_of_dots = round(number_of_dots)
    fitted_grid_size = printable_length / fitted_number_of_dots
    return fitted_grid_size


def truncate_to_3_decimal_points(f):
    f_truncated_to_3_decimal_places = f"{f:.3f}"
    return f_truncated_to_3_decimal_places


def frange(start, finish, increment):
    x = start
    while x < finish:
        yield x
        x += increment


def print_to_stderr(*args, **opts):
    opts['file'] = sys.stderr
    print(*args, **opts)


main()
