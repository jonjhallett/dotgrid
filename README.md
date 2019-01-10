# dotgrid

Generate PDFs for printing dotgrid paper in a variety of grid sizes. The PDF is intended to be printed doublesided on A4 paper.

To generate 5mm, 6mm, 7.5mm, 8mm and 10mm dotgrids, run
```
bash generate_dotgrid
```

To generate a PDF for an arbitrary grid size, use the `--gridsize` command line option for `dotgrid.py`, with a grid size in millimetres. For example, for a 12mm grid use
```
python3 dotgrid.py --gridsize=12 | ps2pdf - >dotgrid.pdf
```

The script will modify the grid size to ensure an exact number of grid squares are printed between the margins.
