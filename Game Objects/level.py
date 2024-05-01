# levels.py
from main import generate_bricks
class Level:
    def __init__(self, bricks, ball_speed):
        self.bricks = bricks
        self.ball_speed = ball_speed

# Define level data
def generate_levels(width, Display_Space):
      # Import generate_bricks from main.py
    levels_data = [
        Level(generate_bricks(width, Display_Space, 4, 10), 5),  # Level 1
        Level(generate_bricks(width, Display_Space, 5, 12), 6),  # Level 2
        # Add more levels as needed
    ]
    return levels_data
