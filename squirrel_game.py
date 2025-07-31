import tkinter as tk
import random

# Game constants
WIDTH = 800
HEIGHT = 400
GROUND_Y = HEIGHT - 50
PLAYER_SIZE = 30
GRAVITY = 0.6
JUMP_STRENGTH = -12
SPEED = 5

class SquirrelGame:
    def __init__(self, root):
        self.root = root
        root.title("Squirrel Side Scroller")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()

        # Score display
        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="black",
                                                  font=("Arial", 16), text=f"Score: {self.score}")

        # Create ground
        self.canvas.create_rectangle(0, GROUND_Y, WIDTH, HEIGHT, fill="forestgreen", outline="")

        # Player setup
        self.player_x = 100
        self.player_y = GROUND_Y - PLAYER_SIZE
        self.player_vy = 0
        self.player = self.canvas.create_rectangle(
            self.player_x, self.player_y,
            self.player_x + PLAYER_SIZE, self.player_y + PLAYER_SIZE,
            fill="saddlebrown")

        # Lists for acorns and rocks
        self.acorns = []
        self.rocks = []

        # Event bindings
        root.bind("<space>", self.jump)

        # Start game loop
        self.spawn_counter = 0
        self.game_over = False
        self.update()

    def jump(self, event=None):
        if self.player_y >= GROUND_Y - PLAYER_SIZE - 1:  # on ground
            self.player_vy = JUMP_STRENGTH

    def spawn_objects(self):
        # Spawn acorn or rock randomly
        obj_type = random.choice(["acorn", "rock"])
        y = GROUND_Y - PLAYER_SIZE if obj_type == "rock" else random.randint(GROUND_Y - 120, GROUND_Y - PLAYER_SIZE*2)
        if obj_type == "acorn":
            obj = self.canvas.create_oval(WIDTH, y, WIDTH + 20, y + 20, fill="orange", outline="")
            self.acorns.append(obj)
        else:
            obj = self.canvas.create_rectangle(WIDTH, y, WIDTH + 30, y + 30, fill="gray", outline="")
            self.rocks.append(obj)

    def move_objects(self, objects):
        for obj in list(objects):
            self.canvas.move(obj, -SPEED, 0)
            x1, y1, x2, y2 = self.canvas.coords(obj)
            if x2 < 0:
                self.canvas.delete(obj)
                objects.remove(obj)

    def check_collisions(self):
        player_coords = self.canvas.coords(self.player)
        # Check acorn collection
        for acorn in list(self.acorns):
            if self.overlap(player_coords, self.canvas.coords(acorn)):
                self.canvas.delete(acorn)
                self.acorns.remove(acorn)
                self.score += 1
                self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")
        # Check rock collision
        for rock in list(self.rocks):
            if self.overlap(player_coords, self.canvas.coords(rock)):
                self.game_over = True
                self.canvas.itemconfigure(self.score_text, text=f"Game Over! Final Score: {self.score}")

    @staticmethod
    def overlap(box1, box2):
        x11, y11, x12, y12 = box1
        x21, y21, x22, y22 = box2
        return not (x12 < x21 or x22 < x11 or y12 < y21 or y22 < y11)

    def update_player(self):
        # Apply gravity
        self.player_vy += GRAVITY
        self.player_y += self.player_vy
        if self.player_y > GROUND_Y - PLAYER_SIZE:
            self.player_y = GROUND_Y - PLAYER_SIZE
            self.player_vy = 0
        self.canvas.coords(self.player,
                           self.player_x, self.player_y,
                           self.player_x + PLAYER_SIZE, self.player_y + PLAYER_SIZE)

    def update(self):
        if not self.game_over:
            self.spawn_counter += 1
            if self.spawn_counter % 50 == 0:
                self.spawn_objects()
            self.move_objects(self.acorns)
            self.move_objects(self.rocks)
            self.check_collisions()
            self.update_player()
            self.root.after(20, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = SquirrelGame(root)
    root.mainloop()
