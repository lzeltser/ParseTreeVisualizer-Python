# Parse Tree Visualizer

Parse Tree Visualizer is an application written in Python and PyQt6
that can display a parse tree for any program written in the
calculator language, a simple Turing complete language created by Dr.
Michael L. Scott in his textbook *Programming Language Pragmatics*.
The program can create a parse tree using LL(1) recursive descent and
table-driven algorithms as well the SLR algorithm.

The program was my capstone project for my computer science degree at
UMass Lowell.

## How to Run
1) Run 
```git clone https://github.com/lzeltser/ParseTreeVisualizer-Python```
 in your desired directory.
2) Install requirements by running ```pip install -r requirements.txt```.
3) Navigate to the Source folder and run ```python Main.py```.

## Requirements
Parse Tree Visualizer has been developed using Python 3.13.1 and only
tested on this version and a Windows 10 machine.

## Known bugs
* The parse tree is not placed on the grid properly when drawn

## Future plans
This project is a work in progress. The following are features I
intend to add:
* Create three parser generators, allowing users to input a grammar for
a programming language and a tree will be built from it
* Add functionality to the menu bar
* Add tooltips
* Allow the tree to be exported as an image file
* Add settings related to displaying the tree
* Add settings for font size
* Add a way to zoom in an out from the tree

## Contact
For any questions about the project, you can contact me at
leonzeltser at gmail dot com.

## Credits
* Author - Leon Zeltser
* Mentor - Dr. Charles Tom Wilkes
* Committee Member - Dr. Matteo Cimini

Parse Tree Visualizer is a port of a Java applet made by Dr. Zerksis
D. Umrigar.

## License
Parse Tree Visualizer is open source and licensed under the GNU Public
License version 3.

Copyright (C) 2024-2025 Leon Zeltser
