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
        return self.order[(self.order.index(self) + 1) % len(self.order)]

    def prev(self):
        """Gets the next smaller size"""
        return self.order[(self.order.index(self) - 1) % len(self.order)]


class Canvas:
    def __init__(
        self, size: tuple[int, int], colorkey: Color = Color(0xFF, 0xFF, 0xFF)
    ) -> None:
        self.width, self.height = size
        self.colorkey = colorkey

        self.surface = Surface(size)
        self.surface.set_colorkey(colorkey)
        self.surface.fill(colorkey)

    def draw(
        self,
        pos,
        brush_size: BrushSize,
        color: Color = Color(0x00, 0x00, 0x00),
    ):
        """Draws a circle at the given position, with all the stuff"""
        pygame.draw.circle(self.surface, color, pos, brush_size.size())

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
