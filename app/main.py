#!/usr/bin/env python3

# BUILT-INS
import warnings
# PIP INSTALLED
import tcod
# LOCALS
from actions import EscapeAction, MovementAction
from input_handlers import EventHandler

def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(
        path="tilesheets/dejavu10x10_gs_tc.png",
        columns=32,
        rows=8,
        charmap=tcod.tileset.CHARMAP_TCOD,
    )

    event_handler = EventHandler()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Inner Space",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=player_x, y=player_y, string="@")

            context.present(root_console)

            root_console.clear()

            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                elif isinstance(action, EscapeAction):
                    raise SystemExit()

if __name__ == "__main__":
    with warnings.catch_warnings():
        WARNINGS_TO_IGNORE = [
            ".*tcod.*",
        ]
        for w in WARNINGS_TO_IGNORE:
            warnings.filterwarnings("ignore", w)
        main()
