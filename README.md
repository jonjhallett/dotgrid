# dotgrid

Generate PDFs for printing A4 dotgrid paper in a variety of grid sizes.

To generate 5mm, 7.5mm, 8mm and 10mm dotgrids, run
```bash
bash generate_dotgrid
```

To generate a PDF for an arbitrary grid size, run
```bash
python3 dotgrid.py --gridsize=<grid size in mm> | ps2pdf - >dotgrid.pdf
```
