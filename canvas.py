from typing import Self, Sequence
import pygame
from enum import Enum, auto
from pygame import Color, Surface


class BrushSize(Enum):
    SMALL = auto()
    MEDIUM = auto()
    BIG = auto()

    def size(self) -> int:
        """Returns the radius of the brush"""
        match self:
            case self.SMALL:
                return 1

            case self.MEDIUM:
                return 2

            case self.BIG:
                return 4

    @property
    def order(self) -> Sequence[Self]:
        """Brushes ordered from smalles to biggest"""
        return (self.SMALL, self.MEDIUM, self.BIG)

    def next(self):
        """Gets the next bigger size"""
        idx = self.order.index(self)
        
        if idx < len(self.order) - 1:
            idx += 1

        return self.order[idx]

    def prev(self):
        """Gets the next smaller size"""
        idx = self.order.index(self)
        
        if idx > 0:
            idx -= 1

        return self.order[idx]


class Canvas:
    def __init__(
        self, size: tuple[int, int], colorkey: Color = Color(0xFF, 0xFF, 0xFF)
    ) -> None:
        self.width, self.height = size
        self.colorkey = colorkey

        # For connecting each point drawn
        self.prev_spot = None
        self.drawing = False
        self.brush_size = None

        self.surface = Surface(size)
        self.surface.set_colorkey(colorkey)
        self.surface.fill(colorkey)

    def draw(
        self,
        pos,
        color: Color = Color(0x00, 0x00, 0x00),
    ):
        """Draws a circle at the given position, with all the stuff"""
        assert (
            self.drawing and self.brush_size is not None
        ), "Attempted to draw without starting drawing"

        if self.prev_spot is not None:
            pygame.draw.line(
                self.surface,
                color,
                self.prev_spot,
                pos,
                self.brush_size.size() * 2,
            )

        self.prev_spot = pos

    def start_drawing(self, brush_size: BrushSize):
        """Start connecting between the dots"""
        self.prev_spot = None
        self.drawing = True
        self.brush_size = brush_size

    def stop_drawing(self):
        """Stop connecting between the dots"""
        self.prev_spot = None
        self.drawing = False
        self.brush_size = None

    def clear(self):
        """Clears the surface"""
        self.surface.fill(self.colorkey)

    def save(self, fn: str):
        """Save the surface to the given file"""
        pygame.image.save(self.surface, fn)

    def get_onion(self, color: Color, trans: int = 255) -> Surface:
        """Returns a surface to be blitted as an onion layer. Unsure of the actual term"""
        surf = self.surface.copy()

        pygame.transform.threshold(
            surf, self.surface, search_color=self.colorkey, set_color=color
        )

        surf.set_alpha(trans)
        return surf
