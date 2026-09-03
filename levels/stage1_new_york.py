# levels/stage1_new_york.py

"""Stage 1 — New York City."""

import pygame

from levels.base_level import BaseLevel
from config.stages import STAGE_CONFIG
from core.asset_manager import assets


class Stage1NewYork(BaseLevel):

    def __init__(self, difficulty: str):

        super().__init__(1, difficulty)

        # -----------------------------------------------------------
        # NEW YORK BACKGROUND
        # -----------------------------------------------------------

        self.bg_image = assets.get_image(
            "backgrounds/stage1_bg.jpg",
            size=(1280, 720)
        )

        self.setup()

    # ---------------------------------------------------------------
    # SETUP
    # ---------------------------------------------------------------

    def setup(self):

        cfg = STAGE_CONFIG[1]

        ps = cfg["player_start"]

        ww = self.world_w
        wh = self.world_h

        # -----------------------------------------------------------
        # OUTER WALLS
        # -----------------------------------------------------------

        self.walls = [

            # Top boundary
            pygame.Rect(
                0,
                0,
                ww,
                40
            ),

            # Bottom boundary
            pygame.Rect(
                0,
                wh - 40,
                ww,
                40
            ),

            # Left boundary
            pygame.Rect(
                0,
                0,
                40,
                wh
            ),

            # Right boundary
            pygame.Rect(
                ww - 40,
                0,
                40,
                wh
            ),
        ]

        # -----------------------------------------------------------
        # NYC PLATFORM OBSTACLES
        #
        # Thin horizontal platforms like Stage 2.
        #
        # IMPORTANT:
        # These are actual collision rectangles, so the player
        # will collide with these platforms normally.
        # -----------------------------------------------------------

        platforms = [

            # =======================================================
            # TOP SECTION
            # =======================================================

            # Left upper platform
            (80, 180, 270, 42),

            # Middle upper platform
            (430, 180, 260, 42),

            # Right upper platform
            (780, 180, 250, 42),

            # Far right upper platform
            (1110, 180, 250, 42),

            # =======================================================
            # MIDDLE SECTION
            # =======================================================

            # Left-middle platform
            (180, 360, 250, 42),

            # Center platform
            (540, 360, 290, 42),

            # Right-middle platform
            (940, 360, 300, 42),

            # Far-right platform
            (1350, 360, 250, 42),

            # =======================================================
            # LOWER SECTION
            # =======================================================

            # Left lower platform
            (80, 550, 250, 42),

            # Center-left lower platform
            (400, 550, 260, 42),

            # Center-right lower platform
            (760, 550, 280, 42),

            # Right lower platform
            (1120, 550, 300, 42),

            # =======================================================
            # BOTTOM PLATFORM ROW
            # =======================================================

            (180, 700, 280, 42),

            (570, 700, 250, 42),

            (900, 700, 280, 42),

            (1280, 700, 300, 42),
        ]

        # -----------------------------------------------------------
        # CREATE COLLISION RECTANGLES
        # -----------------------------------------------------------

        for px, py, pw, ph in platforms:

            self.walls.append(
                pygame.Rect(
                    px,
                    py,
                    pw,
                    ph
                )
            )

        # -----------------------------------------------------------
        # PORTALS
        # -----------------------------------------------------------

        self.generate_portals(
            ps
        )

        # -----------------------------------------------------------
        # FRAGMENTS
        # -----------------------------------------------------------

        self.generate_fragments(
            cfg["fragment_count"]
        )

    # ---------------------------------------------------------------
    # BACKGROUND
    # ---------------------------------------------------------------

    def draw_background(
        self,
        surface: pygame.Surface
    ):

        surface.blit(
            self.bg_image,
            (0, 0)
        )