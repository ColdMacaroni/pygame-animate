from typing import Iterable
from app import App
import pygame

# Size of the window
size = (600, 480)


def update_surface(
    surf: pygame.Surface,
    stack: Iterable[pygame.Surface],
    bg: None | pygame.Color,
):
    if bg is not None:
        surf.fill(bg)

    for s in stack:
        surf.blit(s, (0, 0))


def main():
    pygame.init()

    screen = pygame.display.set_mode(size, vsync=1)
    pygame.display.set_caption("ProtoAnima")

    clock = pygame.time.Clock()

    # The surface that'll be drawn on the screen
    surf = pygame.Surface(size).convert_alpha()

    # Hold all the frames
    app = App(size)

    # Background color of the thing
    bg = pygame.Color(0xFF, 0xFF, 0xFF)
    update_surface(surf, app.get_frame_stack(4), bg)

    # Determines whether the mouse is being dragged and thus is drawing
    dragging = False

    animation_fps = 24
    update_fps = animation_fps * 2.5

    running = True
    while running:
        # Handle events
        events = pygame.event.get()
        for e in events:
            match e.type:
                case pygame.QUIT:
                    running = False

                case pygame.MOUSEBUTTONDOWN:
                    # Left click
                    if e.button == 1:
                        dragging = True

                case pygame.MOUSEBUTTONUP:
                    # Left click
                    if e.button == 1:
                        dragging = False

                case pygame.MOUSEMOTION:
                    if dragging:
                        app.draw(e.pos)
                        update_surface(surf, app.get_frame_stack(4), bg)

        screen.blit(surf, (0, 0))

        pygame.display.flip()
        clock.tick(update_fps)


if __name__ == "__main__":
    main()
