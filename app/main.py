#!/usr/bin/env python3

# BUILT-IN
import copy
import warnings
# INSTALLED
import tcod
# LOCAL
import color
from engine import Engine
import entity_factory
from procgen import generate_dungeon

def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        path="tilesheets/dejavu10x10_gs_tc.png",
        columns=32,
        rows=8,
        charmap=tcod.tileset.CHARMAP_TCOD,
    )

    player = copy.deepcopy(entity_factory.player)
    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine,
    )
    engine.update_fov()
    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!",
        color.welcome_text,
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Inner Space",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()

if __name__ == "__main__":
    with warnings.catch_warnings():
        WARNINGS_TO_IGNORE = [
            ".*tcod.*",
        ]
        for w in WARNINGS_TO_IGNORE:
            warnings.filterwarnings("ignore", w)
        main()

