from tkinter import *
import random

# Constants
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPEED = 150
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#1D4BF0"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#38DD9A"
SCORE_FILE ="score.txt"


try:
    with open(SCORE_FILE,"r") as file:
        topscore = int(file.read())
except FileNotFoundError:
    topscore=0

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake"
            )
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food"
        )

def next_turn(snake, food):
    global direction,score,topscore

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE


    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    # Checkif eaten
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        if score>topscore:
            topscore=score
            with open(SCORE_FILE,"w") as file:
                file.write(str(score))

        label.config(text="Score: {} | Top Score:{}".format(score,topscore))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction
    elif new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Check if the snake hits the walls
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Check if the snake collides with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2,
        font=("consolas", 40),
        text="GAME OVER",
        fill="red",
        tags="gameover",

    )
    score = 0  # Reset the score
    label.config(text=f"Score: {score} | Top Score: {topscore}")

# Main game window
window = Tk()
window.title("Snake Game  :-)")
window.resizable(False, False)

topscore=0#top score initialize
score = 0  # Initialize score to 0
direction = "down"

label = Label(window, text="Score: {} | Top score:{}".format(score,topscore), font=("consolas", 30))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
