from pygame import Color, Surface
from canvas import *
import os
from sys import stderr


class App:
    """Holds the frames and stuff"""

    def __init__(
        self,
        size: tuple[int, int],
        start_brush: BrushSize = BrushSize.MEDIUM,
        brush_color: Color = Color(0x00, 0x00, 0x00),
    ):
        self.size = size
        self.brush = start_brush
        self.brush_color = brush_color

        # Start with an empty frame, avoids issues
        self.frames = [Canvas(size)]
        self.frame_idx = 0

    @property
    def frame(self):
        """Gets the current frame"""
        return self.frames[self.frame_idx]

    def new_frame(self):
        """Inserts a new frame after the one we're viewing"""
        self.stop_drawing()
        self.frames.insert(self.frame_idx + 1, Canvas(self.size))
        self.frame_idx += 1

    def del_frame(self):
        """Deletes the currently viewed frame"""
        self.stop_drawing()

        self.frames.pop(self.frame_idx)

        self.frame_idx = max(0, self.frame_idx - 1)

    def next_frame(self):
        """Switches to the next frame, loops around"""
        self.stop_drawing()

        self.frame_idx += 1
        self.frame_idx %= len(self.frames)

    def prev_frame(self):
        """Switches to the previous frame, loops around"""
        self.stop_drawing()

        self.frame_idx -= 1
        self.frame_idx %= len(self.frames)

    def draw(self, pos: tuple[int, int]):
        self.frame.draw(pos, self.brush_color)

    def start_drawing(self):
        self.frame.start_drawing(self.brush)

    def stop_drawing(self):
        self.frame.stop_drawing()

    def get_onion_stack(self, layers: int) -> list[Surface]:
        """Returns onion layers.
        layers refers to how many forward, how many backward."""

        stack = []
        prev_onion = Color(0x67, 0x13, 0x15)
        next_onion = Color(0x13, 0x50, 0x1F)

        # Inner function because i don't want to repeat myself
        def onion_append(idx: int, color: Color):
            """Adds the frame at that index to the stack, calculating alpha"""
            # Increase opacity as we get closer to the current layer,
            # but don't go full 0 or 255
            alpha = 200 - 180 * (abs(self.frame_idx - idx)) / layers

            stack.append(self.frames[idx].get_onion(color, round(alpha)))

        # Get previous frames, avoid going into negatives.
        for i in range(max(0, self.frame_idx - layers), self.frame_idx):
            onion_append(i, prev_onion)

        # Get next frames, avoid going out of range
        for i in range(
            self.frame_idx + 1,
            min(len(self.frames), self.frame_idx + layers + 1),
        ):
            onion_append(i, next_onion)

        return stack

    def save(self, folder: str) -> None:
        if not os.path.exists(folder):
            os.mkdir(folder)

        for i in range(len(self.frames)):
            # TODO! Find a more extensible way of numbering the images
            self.frames[i].save(os.path.join(folder, f"frame-{i:03}.png"))
