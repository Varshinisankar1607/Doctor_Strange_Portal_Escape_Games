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

    # ---------------------------------------------------------------
    # NYC ROOFTOP PLATFORMS (Architectural Visuals)
    # ---------------------------------------------------------------

    def draw_platforms(
        self,
        surface: pygame.Surface
    ):
        """Draw realistic New York rooftop terrace stone/metallic platforms."""
        for wall in self.walls:
            if (
                wall.width == self.world_w
                or wall.height == self.world_h
            ):
                continue

            r = pygame.Rect(
                wall.x - self.camera.offset_x,
                wall.y - self.camera.offset_y,
                wall.width,
                wall.height
            )

            # 1. Main dark architectural slab (semi-translucent dark slate/granite)
            slab = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
            slab.fill((22, 20, 32, 235))

            # 2. Polished top walking stone cap (thickness 8px)
            cap_h = min(8, r.height)
            pygame.draw.rect(slab, (40, 44, 58, 255), (0, 0, r.width, cap_h))

            # Top crisp highlight rim (city light reflection)
            pygame.draw.line(slab, (95, 105, 130, 220), (0, 0), (r.width - 1, 0), 1)

            # Subtle warm city amber reflection line under the rim
            if cap_h > 2:
                pygame.draw.line(slab, (120, 100, 75, 120), (1, 1), (r.width - 2, 1), 1)

            # 3. Soft Sanctum / tech blue accent line along the ledge lip
            if cap_h >= 6:
                pygame.draw.line(slab, (35, 85, 160, 180), (2, cap_h - 1), (r.width - 3, cap_h - 1), 2)

            # 4. Vertical architectural panel seams and rivets
            seam_spacing = 70
            for sx in range(seam_spacing, r.width - 20, seam_spacing):
                pygame.draw.line(slab, (14, 12, 20, 200), (sx, cap_h), (sx, r.height - 2), 1)
                pygame.draw.line(slab, (50, 48, 65, 120), (sx + 1, cap_h), (sx + 1, r.height - 2), 1)
                # Small architectural bolt/bracket
                if r.height > 18:
                    pygame.draw.circle(slab, (60, 65, 80), (sx, cap_h + 6), 2)

            # 5. Side corner metal brackets
            pygame.draw.rect(slab, (35, 38, 50), (0, 0, 4, r.height))
            pygame.draw.rect(slab, (35, 38, 50), (r.width - 4, 0, 4, r.height))

            # 6. Bottom drop shadow
            pygame.draw.line(slab, (10, 8, 16, 255), (0, r.height - 1), (r.width - 1, r.height - 1), 2)

            surface.blit(slab, r.topleft)