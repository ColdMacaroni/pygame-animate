from typing import Iterable
from app import App
import pygame

# Size of the window
size = (600, 480)


def update_surface(
    surf: pygame.Surface,
    stack: Iterable[pygame.Surface],
    last: pygame.Surface,
    bg: None | pygame.Color,
):
    if bg is not None:
        surf.fill(bg)

    for s in stack:
        surf.blit(s, (0, 0))

    # The last frame, above all
    surf.blit(last, (0,0))


def main():
    pygame.init()

    screen = pygame.display.set_mode(size, vsync=1)
    pygame.display.set_caption("ProtoAnima")

    clock = pygame.time.Clock()

    # The surface that'll be drawn on the screen
    surf = pygame.Surface(size)

    # Hold all the frames
    app = App(size)

    # Background color of the thing
    bg = pygame.Color(0xFF, 0xFF, 0xFF)
    update_surface(surf, [], app.frame.surface, bg)

    onion_layers = 3
    onion_stack = []

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
                        update_surface(surf, onion_stack, app.frame.surface, bg)

                case pygame.KEYUP:
                    match e.key:
                        case pygame.K_PERIOD:
                            app.next_frame()
                            onion_stack = app.get_onion_stack(onion_layers)
                            update_surface(surf, onion_stack, app.frame.surface, bg)

                        case pygame.K_COMMA:
                            app.prev_frame()
                            onion_stack = app.get_onion_stack(onion_layers)
                            update_surface(surf, onion_stack, app.frame.surface, bg)

                        case pygame.K_n:
                            app.new_frame()
                            onion_stack = app.get_onion_stack(onion_layers)
                            update_surface(surf, onion_stack, app.frame.surface, bg)

                        case pygame.K_d:
                            if len(app.frames) > 1:
                                app.del_frame()

        screen.blit(surf, (0, 0))

        pygame.display.flip()
        clock.tick(update_fps)


if __name__ == "__main__":
    main()
