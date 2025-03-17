# Egg Catcher Game

## Description

This project is an *Egg Catcher Game* built using *Python* and *Tkinter* for the graphical user interface (GUI). The player controls a U-shaped pan to catch falling eggs, earn points, and progress through levels.

## Features

- *User-friendly GUI* using Tkinter.

- *U-shaped pan* to catch falling eggs.

- *Multiple levels* with increasing difficulty.

- *Score tracking* and chances system.

- *Game over and level progression messages.*

- *Different background images* for each level.


## Technologies Used

- *Python*

- *Tkinter* for GUI

- *Pillow (PIL)* for handling images

- *Random* for generating random egg positions


## Installation

### Prerequisites

- Install Python 

- Install required dependencies:
  sh
  pip install pillow
  

## Setup

1. *Ensure You Have Background Images:*
   - The game requires three background images: background1.jpg, background2.jpg, background3.jpg.

   - Place these images in the same directory as the script.


2. *Run the Python Script:*
   sh
   python egg_catcher.py
   

## Gameplay

- Move the *U-shaped pan* using the *Left Arrow* and *Right Arrow* keys.

- Catch the falling eggs to earn *10 points per egg*.

- Lose a chance when an egg falls off the screen.

- Progress to the *next level* at *100, 150, and 200 points*.

- Game over when chances reach *zero*.


## Troubleshooting

- Ensure the background images (background1.jpg, background2.jpg, background3.jpg) are present in the correct directory.

- If images do not load, check the file paths in the script.

- If PIL (Pillow) is not installed, install it using pip install pillow.


## Author

Developed by *CHANDRUPATLA SAI VARUN*


## License

This project is licensed under the *MIT License*.
