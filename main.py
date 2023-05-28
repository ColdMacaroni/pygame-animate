from typing import Iterable
from app import App
import pygame
import time

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

    onion_layers = 5
    onion_stack = []

    # If the animation is playing
    playing = False
    prev_time = time.time()

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
                    if e.button == 1:
                        app.start_drawing()
                    # Left click

                case pygame.MOUSEBUTTONUP:
                    # Left click
                    if e.button == 1:
                        app.stop_drawing()

                case pygame.MOUSEMOTION:
                    if app.frame.drawing and not playing:
                        app.draw(e.pos)
                        update_surface(surf, onion_stack, app.frame.surface, bg)

                case pygame.KEYUP:
                    match e.key:
                        case pygame.K_s:
                            app.stop_drawing()
                            app.save("out")
                        # TODO! Move all these onion updates to a function
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
                                onion_stack = app.get_onion_stack(onion_layers)
                                update_surface(surf, onion_stack, app.frame.surface, bg)

                        case pygame.K_c | pygame.K_DELETE:
                            app.stop_drawing()
                            app.frame.clear()
                            update_surface(surf, onion_stack, app.frame.surface, bg)

                        case pygame.K_p | pygame.K_SPACE:
                            app.stop_drawing()
                            playing = not playing

        if playing and prev_time + (1/animation_fps) <= time.time():
            app.next_frame()
            update_surface(surf, [], app.frame.surface, bg)

        screen.blit(surf, (0, 0))

        pygame.display.flip()
        clock.tick(update_fps)


if __name__ == "__main__":
    main()
