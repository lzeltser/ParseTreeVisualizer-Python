# Parse Tree Visualizer

Parse Tree Visualizer is an application written in Python and PyQt6
that can display a parse tree for any program written in the
calculator language, a simple Turing complete language created by Dr.
Michael L. Scott in his textbook *Programming Language Pragmatics*.
The program can create a parse tree using LL(1) recursive descent and
table-driven algorithms as well the SLR algorithm.

The program was made as a part of my capstone project for my computer
science degree at UMass Lowell.

## How to Run
1) Run 
```git clone https://github.com/lzeltser/ParseTreeVisualizer-Python```
in your desired directory.
2) Install requirements by running ```pip install -r requirements.txt```
in the root folder. You may want to create a virtual environment first.
3) Navigate to the Source folder and run ```python Main.py```.

## Requirements
Parse Tree Visualizer has been developed using Python 3.13.1 and only
tested on this version and on a Windows 10 machine.

## Known bugs

## Future plans
This project is a work in progress. The following are features I
intend to add:
* Clean up the code
* Add functionality to the menu bar
* Add tooltips
* Allow the tree to be exported as an image file
* Add settings related to displaying the tree
* Add settings for font size
* Add a way to zoom in an out from the tree
* Add more languages for the recursive descent code (in no particular
order, Ada, C#, D, Go, Java, JavaScript, Haskell, OCaml, Ruby, Rust)
and make them set by config files rather than hard coded
* Add more grammars (B-Minor and PL/0 are currently a work-in-progress)

## Contact
For any questions about the project, you can email me at
leonzeltser at gmail dot com.

## Credits
* Author - Leon Zeltser
* Mentor - Dr. Charles Thomas Wilkes
* Committee Member - Dr. Matteo Cimini

Parse Tree Visualizer is a port of a Java applet made by Dr. Zerksis
D. Umrigar and ported to later versions of Java by David Bacon and
Victoria Munroe mentored by Dr. Charles Thomas Wilkes.

## License
Parse Tree Visualizer is open source and is licensed under the GNU
General Public License version 3.

Copyright (C) 2024-2025 Leon Zeltser
