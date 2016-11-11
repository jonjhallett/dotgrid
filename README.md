# dotgrid

Generate PDFs for printing A4 dotgrid paper in a variety of grid sizes.

To generate 5mm, 7.5mm, 8mm and 10mm dotgrids, run
```
bash generate_dotgrid
```

To generate a PDF for an arbitrary grid size, run
```
python3 dotgrid.py --gridsize=<grid size in mm> | ps2pdf - >dotgrid.pdf
```

The python script, `dotgrid.py`, outputs PostScript with a PageSize set for A4.
