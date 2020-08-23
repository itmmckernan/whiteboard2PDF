# whiteboard2PDF
A simple program written in python in order to convert the exported SVG file from Microsoft Whiteboard to a PDF.

# Usage
1. Export an SVG from MS Whiteboard
2. Drop it onto the whiteboard2svg.py. It can take multiple.
3. Give it a second and the PDF file will magically appear in the directory of the python file.

# Installation
1. Python 3. Tested on 3.8 64 bit but others will work.
2. Libraries:
    Needs cariosvg, Pillow/PIL, and numpy
  
 # todo
 1. Compile python file and dependancies into single .exe file
 2. Keep everything vectorized (dont rasterize pen strokes)
 3. Command line options (quality, etc)
 4. Add option to move strokes off pages into their own pdf pages (currently they are just cut off)
 5. Speed it up
 6. de-spagettify everything
