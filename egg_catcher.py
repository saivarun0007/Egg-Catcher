import tkinter as tk
import random
from PIL import Image, ImageTk

# Initialize the main window
root = tk.Tk()
root.title("Egg Catcher Game")

# Canvas dimensions
canvas_width = 400
canvas_height = 600
c = tk.Canvas(root, width=canvas_width, height=canvas_height)
c.pack()

# Load background images
background_images = [
    ImageTk.PhotoImage(Image.open("background1.jpg").resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)),
    ImageTk.PhotoImage(Image.open("background2.jpg").resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)),
    ImageTk.PhotoImage(Image.open("background3.jpg").resize((canvas_width, canvas_height), Image.Resampling.LANCZOS))
]

current_background = c.create_image(0, 0, anchor='nw', image=background_images[0])

# Create U-shaped pan (catcher)
pan_width = 60
pan_height = 40
pan_color = "blue"

left_oval = c.create_oval(canvas_width // 2 - pan_width,
                          canvas_height - pan_height - 20,
                          canvas_width // 2 - pan_width + 20,
                          canvas_height - 20,
                          fill=pan_color)

right_oval = c.create_oval(canvas_width // 2 + pan_width - 20,
                           canvas_height - pan_height - 20,
                           canvas_width // 2 + pan_width,
                           canvas_height - 20,
                           fill=pan_color)

bottom_rectangle = c.create_rectangle(canvas_width // 2 - pan_width + 10,
                                      canvas_height - pan_height - 10,
                                      canvas_width // 2 + pan_width - 10,
                                      canvas_height - 20,
                                      fill=pan_color)

catcher = [left_oval, right_oval, bottom_rectangle]

# Game variables
score = 0
chances = 3
egg_speed = 5
egg_interval = 2000
difficulty_factor = 0.95
eggs = []
level = 1
level_scores = [100, 150, 200]
paused = False

# Display score and chances
score_text = c.create_text(10, 10, anchor='nw', font=('Arial', 16, 'bold'), fill='black', text='Score: 0')
chances_text = c.create_text(canvas_width - 10, 10, anchor='ne', font=('Arial', 16, 'bold'), fill='black', text='Chances: 3')


def update_background():
    """Updates the background image based on the current level."""
    c.itemconfig(current_background, image=background_images[level - 1])


def create_egg():
    """Creates a new falling egg with a random color."""
    if not paused:
        x = random.randint(10, canvas_width - 10)
        y = 0
        egg_color = random.choice(["red", "yellow", "green", "blue", "purple"])
        egg = c.create_oval(x - 15, y, x + 15, y + 30, fill=egg_color, width=0)
        eggs.append(egg)
    root.after(egg_interval, create_egg)


def move_eggs():
    """Moves the eggs down the screen."""
    global chances, score, egg_speed
    if not paused:
        for egg in list(eggs):
            c.move(egg, 0, egg_speed)
            egg_coords = c.coords(egg)

            if egg_coords[3] > canvas_height:  # Egg fell off the screen
                c.delete(egg)
                eggs.remove(egg)
                chances -= 1
                c.itemconfigure(chances_text, text=f'Chances: {chances}')
                if chances == 0:
                    game_over()

            elif check_collision(egg_coords):
                c.delete(egg)
                eggs.remove(egg)
                increase_score(10)

    root.after(100, move_eggs)


def check_collision(egg_coords):
    """Checks if an egg collides with the U-shaped pan."""
    (lx1, ly1, lx2, ly2) = c.coords(catcher[0])  # Left oval
    (rx1, ry1, rx2, ry2) = c.coords(catcher[1])  # Right oval
    (bx1, by1, bx2, by2) = c.coords(catcher[2])  # Bottom rectangle

    return (
        (lx1 <= egg_coords[2] <= lx2 and ly1 <= egg_coords[3] <= ly2) or
        (rx1 <= egg_coords[0] <= rx2 and ry1 <= egg_coords[3] <= ry2) or
        (bx1 <= egg_coords[2] and bx2 >= egg_coords[0] and by1 <= egg_coords[3])
    )


def increase_score(points):
    """Increases the score and checks for level promotion."""
    global score, egg_interval, level
    score += points
    c.itemconfigure(score_text, text=f'Score: {score}')
    if score >= level_scores[level - 1]:
        promote_level()


def promote_level():
    """Promotes the player to the next level."""
    global level, egg_speed, egg_interval, paused
    if level < 3:
        paused = True
        level += 1
        egg_speed += 2
        egg_interval = max(500, int(egg_interval * difficulty_factor))
        update_background()
        show_message(f"Level {level} Unlocked!")
        root.after(3000, resume_game)
    else:
        game_won()


def show_message(message):
    """Displays a temporary message on the screen."""
    message_id = c.create_text(canvas_width // 2, canvas_height // 2, text=message, font=("Arial", 24, "bold"), fill="white")
    root.after(2000, lambda: c.delete(message_id))


def resume_game():
    """Resumes the game after showing a level-up message."""
    global paused
    paused = False


def move_left(event):
    """Moves the U-shaped pan to the left."""
    (lx1, ly1, lx2, ly2) = c.coords(catcher[0])
    if lx1 > 0:
        for part in catcher:
            c.move(part, -20, 0)


def move_right(event):
    """Moves the U-shaped pan to the right."""
    (rx1, ry1, rx2, ry2) = c.coords(catcher[1])
    if rx2 < canvas_width:
        for part in catcher:
            c.move(part, 20, 0)


def game_won():
    """Displays a game won message."""
    show_message(f"Congratulations! You completed all levels with a score of {score}!")
    root.after(3000, restart_game)


def game_over():
    """Displays game over popup and restarts."""
    show_message("Game Over")
    root.after(3000, restart_game)


def restart_game():
    """Resets the game to the initial state."""
    global score, chances, eggs, egg_speed, egg_interval, level, paused
    score = 0
    chances = 3
    egg_speed = 5
    egg_interval = 2000
    level = 1
    paused = False
    eggs.clear()
    update_background()
    c.itemconfigure(score_text, text='Score: 0')
    c.itemconfigure(chances_text, text='Chances: 3')


# Bind keys to U-shaped pan movement
c.bind('<Left>', move_left)
c.bind('<Right>', move_right)
c.focus_set()

# Start the game
root.after(1000, create_egg)
root.after(1000, move_eggs)
root.mainloop()
