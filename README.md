# Pygame animation program

Requires pygame. Add your desired animation framerate as a command line argument

| Key | Action |
| --- | ------ |
| n   | New frame |
| d   | delete frame |
| ,   | previous frame |
| .   | next frame |
| c   | clear frame |
| space or p | play/pause animation |
| s | save frames to out folder |
| + or = | increase brush size |
| - | decrease brush size |

You can then convert those to an mp4 or whatever with `ffmpeg -framerate 8 -pattern_type glob -i 'out/*.png' -c:v libx264 -pix_fmt yuv420p out.mp4`
