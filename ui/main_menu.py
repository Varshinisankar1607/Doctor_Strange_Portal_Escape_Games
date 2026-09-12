# ui/main_menu.py
"""
Doctor Strange: Portal Escape
Cinematic Animated Main Menu

FULL REPLACEMENT FILE

Features:
- Elegant cinematic serif typography
- Curved/fantasy-style appearance
- Animated title breathing
- Animated golden shimmer
- Soft magical glow
- Deep cinematic shadow
- Floating particles
- Dimensional cracks
- PLAY / HOW TO PLAY / EXIT
- Mouse controls
- Keyboard controls
"""

import pygame
import math
import random
import os

from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from core.asset_manager import assets


class MainMenu:

    # =============================================================
    # COLORS
    # =============================================================

    GOLD = (255, 180, 0)
    GOLD_BRIGHT = (255, 220, 95)
    GOLD_LIGHT = (255, 235, 165)

    WHITE = (255, 255, 255)
    WHITE_SOFT = (245, 240, 255)

    PURPLE = (125, 55, 220)
    PURPLE_BRIGHT = (205, 120, 255)

    BLACK = (5, 2, 12)

    # =============================================================
    # INITIALIZATION
    # =============================================================

    def __init__(self, font_large, font_med, font_small):

        # Keep compatibility with existing Game class
        self.fl = font_large
        self.fm = font_med
        self.fs = font_small

        self._t = 0.0

        # =========================================================
        # BACKGROUND
        # =========================================================

        self.home_bg = assets.get_image(
            "backgrounds/homepage_multiverse.jpg",
            size=(SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        # =========================================================
        # CINEMATIC FONTS
        # =========================================================

        self.title_font = self._load_cinematic_font(
            max(66, int(SCREEN_WIDTH * 0.062))
        )

        self.title_font_2 = self._load_cinematic_font(
            max(62, int(SCREEN_WIDTH * 0.057))
        )

        self.subtitle_font = self._load_cinematic_font(
            max(21, int(SCREEN_WIDTH * 0.0175))
        )

        self.button_font = self._load_cinematic_font(
            max(29, int(SCREEN_WIDTH * 0.025))
        )

        # =========================================================
        # FLOATING PARTICLES
        # =========================================================

        self._particles = []

        for _ in range(120):

            self._particles.append({
                "x": random.uniform(
                    0,
                    SCREEN_WIDTH
                ),

                "y": random.uniform(
                    0,
                    SCREEN_HEIGHT
                ),

                "vx": random.uniform(
                    -0.35,
                    0.35
                ),

                "vy": random.uniform(
                    -1.5,
                    -0.3
                ),

                "speed": random.uniform(
                    0.8,
                    1.8
                ),

                "size": random.randint(
                    1,
                    3
                ),

                "phase": random.uniform(
                    0,
                    math.pi * 2
                )
            })

        # =========================================================
        # DIMENSIONAL CRACKS
        # =========================================================

        self._cracks = []

        for _ in range(7):

            self._cracks.append({
                "x": random.randint(
                    70,
                    SCREEN_WIDTH - 70
                ),

                "y": random.randint(
                    100,
                    SCREEN_HEIGHT - 150
                ),

                "angle": random.uniform(
                    0,
                    math.pi * 2
                ),

                "length": random.randint(
                    35,
                    90
                )
            })

        # =========================================================
        # BUTTONS
        # =========================================================

        self.selected = 0

        self._buttons = [
            "PLAY",
            "HOW TO PLAY",
            "EXIT"
        ]

        self.hovered = -1
        self.clicked = None

    # =============================================================
    # LOAD CINEMATIC FONT
    # =============================================================

    def _load_cinematic_font(self, size):

        """
        Loads an elegant serif font available on Windows.

        Priority:
        1. Baskerville
        2. Garamond
        3. Constantia
        4. Georgia
        5. Cambria
        6. Times New Roman

        If none are available, Georgia is used as fallback.
        """

        candidates = [

            # -----------------------------------------------------
            # BASKERVILLE
            # -----------------------------------------------------

            r"C:\Windows\Fonts\BASKVILL.TTF",

            # -----------------------------------------------------
            # GARAMOND
            # -----------------------------------------------------

            r"C:\Windows\Fonts\GARA.TTF",

            # -----------------------------------------------------
            # CONSTANTIA
            # -----------------------------------------------------

            r"C:\Windows\Fonts\constan.ttf",

            # -----------------------------------------------------
            # GEORGIA
            # -----------------------------------------------------

            r"C:\Windows\Fonts\georgia.ttf",

            # -----------------------------------------------------
            # CAMBRIA
            # -----------------------------------------------------

            r"C:\Windows\Fonts\cambria.ttf",

            # -----------------------------------------------------
            # TIMES NEW ROMAN
            # -----------------------------------------------------

            r"C:\Windows\Fonts\times.ttf",
        ]

        for font_path in candidates:

            try:

                if os.path.exists(font_path):

                    return pygame.font.Font(
                        font_path,
                        size
                    )

            except Exception:

                pass

        # ---------------------------------------------------------
        # FALLBACK
        # ---------------------------------------------------------

        return pygame.font.SysFont(
            "georgia",
            size,
            bold=True
        )

    # =============================================================
    # FIT FONT TO SCREEN
    # =============================================================

    def _fit_font(
        self,
        font,
        text,
        max_width
    ):

        """
        Automatically reduces the font size if the title
        becomes too wide for the screen.
        """

        size = font.get_height()

        while size > 20:

            test_font = self._load_cinematic_font(
                size
            )

            width = test_font.size(
                text
            )[0]

            if width <= max_width:

                return test_font

            size -= 2

        return font

    # =============================================================
    # EVENT HANDLING
    # =============================================================

    def handle_event(
        self,
        event,
        mouse_pos
    ):

        # ---------------------------------------------------------
        # MOUSE MOVE
        # ---------------------------------------------------------

        if event.type == pygame.MOUSEMOTION:

            self.hovered = -1

            for i, (
                rx,
                ry,
                rw,
                rh
            ) in enumerate(
                self._button_rects()
            ):

                if (
                    rx <= mouse_pos[0] <= rx + rw
                    and
                    ry <= mouse_pos[1] <= ry + rh
                ):

                    self.hovered = i

        # ---------------------------------------------------------
        # MOUSE CLICK
        # ---------------------------------------------------------

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and
            event.button == 1
        ):

            if (
                0 <= self.hovered
                < len(self._buttons)
            ):

                self.clicked = (
                    self._buttons[
                        self.hovered
                    ]
                )

                return self.clicked

        # ---------------------------------------------------------
        # KEYBOARD
        # ---------------------------------------------------------

        elif event.type == pygame.KEYDOWN:

            # UP
            if event.key in (
                pygame.K_UP,
                pygame.K_w
            ):

                self.selected = (
                    self.selected - 1
                ) % len(self._buttons)

            # DOWN
            elif event.key in (
                pygame.K_DOWN,
                pygame.K_s
            ):

                self.selected = (
                    self.selected + 1
                ) % len(self._buttons)

            # ENTER
            elif event.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER
            ):

                self.clicked = (
                    self._buttons[
                        self.selected
                    ]
                )

                return self.clicked

        return None

    # =============================================================
    # BUTTON RECTANGLES
    # =============================================================

    def _button_rects(self):

        bw = min(
            390,
            int(SCREEN_WIDTH * 0.29)
        )

        bh = 64

        cx = (
            SCREEN_WIDTH // 2
            - bw // 2
        )

        base_y = int(
            SCREEN_HEIGHT * 0.715
        )

        return [
            (
                cx,
                base_y + i * 78,
                bw,
                bh
            )

            for i in range(
                len(self._buttons)
            )
        ]

    # =============================================================
    # UPDATE
    # =============================================================

    def update(
        self,
        dt: float
    ):

        self._t += dt

        # ---------------------------------------------------------
        # PARTICLES
        # ---------------------------------------------------------

        for p in self._particles:

            p["x"] += (
                p["vx"]
                * dt
                * 30
            )

            p["y"] += (
                p["vy"]
                * p["speed"]
                * dt
                * 30
            )

            # Wrap top
            if p["y"] < -10:

                p["y"] = (
                    SCREEN_HEIGHT + 10
                )

                p["x"] = random.uniform(
                    0,
                    SCREEN_WIDTH
                )

            # Wrap left
            if p["x"] < -10:

                p["x"] = (
                    SCREEN_WIDTH + 10
                )

            # Wrap right
            elif p["x"] > SCREEN_WIDTH + 10:

                p["x"] = -10

    # =============================================================
    # DRAW PARTICLE
    # =============================================================

    def _draw_particle(
        self,
        surface,
        x,
        y,
        size,
        alpha
    ):

        particle = pygame.Surface(
            (
                size * 4 + 4,
                size * 4 + 4
            ),
            pygame.SRCALPHA
        )

        center = (
            size * 2 + 2,
            size * 2 + 2
        )

        # ---------------------------------------------------------
        # SOFT PURPLE GLOW
        # ---------------------------------------------------------

        pygame.draw.circle(
            particle,
            (
                190,
                160,
                255,
                max(
                    20,
                    int(alpha * 0.35)
                )
            ),
            center,
            size * 2
        )

        # ---------------------------------------------------------
        # BRIGHT CENTER
        # ---------------------------------------------------------

        pygame.draw.circle(
            particle,
            (
                235,
                220,
                255,
                max(
                    40,
                    int(alpha)
                )
            ),
            center,
            max(
                1,
                size
            )
        )

        surface.blit(
            particle,
            (
                int(
                    x - center[0]
                ),
                int(
                    y - center[1]
                )
            )
        )

    # =============================================================
    # DRAW DIMENSIONAL CRACKS
    # =============================================================

    def _draw_cracks(
        self,
        surface
    ):

        t = self._t

        for crack in self._cracks:

            cx = crack["x"]
            cy = crack["y"]

            base_angle = (
                crack["angle"]
            )

            length = (
                crack["length"]
            )

            pulse = (
                math.sin(
                    t * 1.5
                    + cx * 0.01
                )
                * 0.12
            )

            for segment in range(3):

                angle = (
                    base_angle
                    + segment * 0.45
                    + pulse
                )

                seg_length = (
                    length
                    * (segment + 1)
                    / 3
                )

                x2 = (
                    cx
                    + math.cos(angle)
                    * seg_length
                )

                y2 = (
                    cy
                    + math.sin(angle)
                    * seg_length
                )

                pygame.draw.line(
                    surface,
                    (
                        100,
                        45,
                        210
                    ),
                    (
                        int(cx),
                        int(cy)
                    ),
                    (
                        int(x2),
                        int(y2)
                    ),
                    2
                )

    # =============================================================
    # CINEMATIC TEXT
    # =============================================================

    def _draw_glow_text(
        self,
        surface,
        font,
        text,
        center_x,
        center_y,
        fill,
        outline,
        outline_width=3,
        glow_strength=45,
        pulse=True
    ):

        # ---------------------------------------------------------
        # TITLE BREATHING ANIMATION
        # ---------------------------------------------------------

        if pulse:

            breathe = (
                math.sin(
                    self._t * 1.8
                )
                * 1.2
            )

            center_y += breathe

        # ---------------------------------------------------------
        # MAIN TEXT
        # ---------------------------------------------------------

        text_surface = font.render(
            text,
            True,
            fill
        )

        rect = text_surface.get_rect(
            center=(
                int(center_x),
                int(center_y)
            )
        )

        # ---------------------------------------------------------
        # SOFT MAGIC GLOW
        # ---------------------------------------------------------

        glow_size = (
            text_surface.get_width()
            + 70,

            text_surface.get_height()
            + 70
        )

        glow_surface = pygame.Surface(
            glow_size,
            pygame.SRCALPHA
        )

        glow_text = font.render(
            text,
            True,
            fill
        )

        pulse_alpha = int(
            glow_strength
            + math.sin(
                self._t * 2.2
            ) * 12
        )

        pulse_alpha = max(
            10,
            min(
                90,
                pulse_alpha
            )
        )

        glow_text.set_alpha(
            pulse_alpha
        )

        gx = (
            glow_size[0] // 2
            - glow_text.get_width() // 2
        )

        gy = (
            glow_size[1] // 2
            - glow_text.get_height() // 2
        )

        # Multiple glow passes
        for ox, oy in (
            (-5, 0),
            (5, 0),
            (0, -5),
            (0, 5),
            (0, 0),
        ):

            glow_surface.blit(
                glow_text,
                (
                    gx + ox,
                    gy + oy
                )
            )

        surface.blit(
            glow_surface,
            (
                rect.x
                - (
                    glow_size[0]
                    - rect.width
                ) // 2,

                rect.y
                - (
                    glow_size[1]
                    - rect.height
                ) // 2
            )
        )

        # ---------------------------------------------------------
        # DEEP SHADOW
        # ---------------------------------------------------------

        shadow = font.render(
            text,
            True,
            (
                12,
                3,
                22
            )
        )

        shadow_rect = shadow.get_rect(
            center=(
                rect.centerx + 4,
                rect.centery + 6
            )
        )

        surface.blit(
            shadow,
            shadow_rect
        )

        # ---------------------------------------------------------
        # DARK OUTLINE
        # ---------------------------------------------------------

        outline_surface = font.render(
            text,
            True,
            outline
        )

        for dx in range(
            -outline_width,
            outline_width + 1
        ):

            for dy in range(
                -outline_width,
                outline_width + 1
            ):

                if (
                    dx == 0
                    and
                    dy == 0
                ):
                    continue

                surface.blit(
                    outline_surface,
                    (
                        rect.x + dx,
                        rect.y + dy
                    )
                )

        # ---------------------------------------------------------
        # MAIN TEXT
        # ---------------------------------------------------------

        surface.blit(
            text_surface,
            rect
        )

        return rect

    # =============================================================
    # DRAW TITLE
    # =============================================================

    def _draw_title(
        self,
        surface
    ):

        sw = SCREEN_WIDTH
        sh = SCREEN_HEIGHT

        # =========================================================
        # DOCTOR STRANGE
        # =========================================================

        title1 = "DOCTOR STRANGE:"

        title1_font = self._fit_font(
            self.title_font,
            title1,
            int(sw * 0.82)
        )

        title1_y = int(
            sh * 0.105
        )

        self._draw_glow_text(
            surface,
            title1_font,
            title1,
            sw // 2,
            title1_y,
            self.GOLD_BRIGHT,
            (
                55,
                16,
                5
            ),
            outline_width=5,
            glow_strength=50,
            pulse=True
        )

        # =========================================================
        # PORTAL ESCAPE
        # =========================================================

        title2 = "PORTAL ESCAPE"

        title2_font = self._fit_font(
            self.title_font_2,
            title2,
            int(sw * 0.70)
        )

        title2_y = int(
            sh * 0.205
        )

        self._draw_glow_text(
            surface,
            title2_font,
            title2,
            sw // 2,
            title2_y,
            self.WHITE,
            (
                35,
                12,
                75
            ),
            outline_width=5,
            glow_strength=42,
            pulse=True
        )

        # =========================================================
        # ANIMATED GOLDEN SHIMMER
        # =========================================================

        shimmer_y = int(
            sh * 0.255
        )

        shimmer_width = int(
            sw * 0.32
        )

        travel = (
            math.sin(
                self._t * 1.2
            )
            * 0.5
            + 0.5
        )

        shimmer_x = int(
            sw // 2
            - shimmer_width // 2
            + (
                travel - 0.5
            )
            * shimmer_width
            * 0.7
        )

        shimmer = pygame.Surface(
            (
                shimmer_width,
                2
            ),
            pygame.SRCALPHA
        )

        for x in range(
            shimmer_width
        ):

            distance = abs(
                x
                - shimmer_width // 2
            )

            alpha = max(
                0,
                110
                - int(
                    distance * 3
                )
            )

            pygame.draw.line(
                shimmer,
                (
                    255,
                    220,
                    110,
                    alpha
                ),
                (
                    x,
                    0
                ),
                (
                    x,
                    1
                )
            )

        surface.blit(
            shimmer,
            (
                shimmer_x,
                shimmer_y
            )
        )

        # =========================================================
        # SUBTITLE
        # =========================================================

        subtitle_text = (
            "FIND THE RIGHT PORTAL BEFORE "
            "THE MULTIVERSE COLLAPSES"
        )

        subtitle_font = self._fit_font(
            self.subtitle_font,
            subtitle_text,
            int(sw * 0.72)
        )

        subtitle_y = int(
            sh * 0.295
        )

        self._draw_glow_text(
            surface,
            subtitle_font,
            subtitle_text,
            sw // 2,
            subtitle_y,
            self.GOLD_LIGHT,
            (
                30,
                10,
                40
            ),
            outline_width=2,
            glow_strength=18,
            pulse=False
        )

    # =============================================================
    # DRAW BUTTONS
    # =============================================================

    def _draw_buttons(
        self,
        surface
    ):

        highlight = (
            self.hovered
            if self.hovered >= 0
            else self.selected
        )

        for i, (
            rx,
            ry,
            rw,
            rh
        ) in enumerate(
            self._button_rects()
        ):

            is_selected = (
                i == highlight
            )

            panel = pygame.Surface(
                (
                    rw,
                    rh
                ),
                pygame.SRCALPHA
            )

            # -----------------------------------------------------
            # PANEL
            # -----------------------------------------------------

            if is_selected:

                panel.fill(
                    (
                        80,
                        35,
                        8,
                        145
                    )
                )

            else:

                panel.fill(
                    (
                        8,
                        5,
                        28,
                        195
                    )
                )

            # -----------------------------------------------------
            # SELECTED BORDER
            # -----------------------------------------------------

            if is_selected:

                border_alpha = int(
                    190
                    + math.sin(
                        self._t * 4
                    ) * 50
                )

                pygame.draw.rect(
                    panel,
                    (
                        255,
                        215,
                        80,
                        border_alpha
                    ),
                    (
                        0,
                        0,
                        rw,
                        rh
                    ),
                    3,
                    border_radius=10
                )

                pygame.draw.rect(
                    panel,
                    (
                        255,
                        145,
                        20,
                        125
                    ),
                    (
                        5,
                        5,
                        rw - 10,
                        rh - 10
                    ),
                    1,
                    border_radius=8
                )

            # -----------------------------------------------------
            # NORMAL BORDER
            # -----------------------------------------------------

            else:

                pygame.draw.rect(
                    panel,
                    (
                        105,
                        60,
                        190,
                        190
                    ),
                    (
                        0,
                        0,
                        rw,
                        rh
                    ),
                    2,
                    border_radius=10
                )

            surface.blit(
                panel,
                (
                    rx,
                    ry
                )
            )

            # -----------------------------------------------------
            # BUTTON TEXT
            # -----------------------------------------------------

            text_color = (
                self.GOLD_BRIGHT
                if is_selected
                else self.WHITE_SOFT
            )

            text = self._buttons[i]

            font = self.button_font

            # Smaller font for HOW TO PLAY
            if text == "HOW TO PLAY":

                font = self._load_cinematic_font(
                    max(
                        25,
                        int(
                            font.get_height()
                            * 0.86
                        )
                    )
                )

            txt = font.render(
                text,
                True,
                text_color
            )

            # -----------------------------------------------------
            # SELECTED SCALE
            # -----------------------------------------------------

            if is_selected:

                scale = 1.045

                txt = pygame.transform.smoothscale(
                    txt,
                    (
                        int(
                            txt.get_width()
                            * scale
                        ),

                        int(
                            txt.get_height()
                            * scale
                        )
                    )
                )

            # -----------------------------------------------------
            # TEXT SHADOW
            # -----------------------------------------------------

            shadow_txt = font.render(
                text,
                True,
                (
                    12,
                    3,
                    22
                )
            )

            if is_selected:

                shadow_txt = (
                    pygame.transform.smoothscale(
                        shadow_txt,
                        txt.get_size()
                    )
                )

            surface.blit(
                shadow_txt,
                (
                    rx
                    + rw // 2
                    - shadow_txt.get_width() // 2
                    + 2,

                    ry
                    + rh // 2
                    - shadow_txt.get_height() // 2
                    + 3
                )
            )

            # -----------------------------------------------------
            # MAIN BUTTON TEXT
            # -----------------------------------------------------

            surface.blit(
                txt,
                (
                    rx
                    + rw // 2
                    - txt.get_width() // 2,

                    ry
                    + rh // 2
                    - txt.get_height() // 2
                )
            )

    # =============================================================
    # DRAW
    # =============================================================

    def draw(
        self,
        surface: pygame.Surface
    ):

        t = self._t

        sw = SCREEN_WIDTH
        sh = SCREEN_HEIGHT

        # =========================================================
        # BACKGROUND
        # =========================================================

        surface.blit(
            self.home_bg,
            (
                0,
                0
            )
        )

        # =========================================================
        # DARK CINEMATIC OVERLAY
        # =========================================================

        overlay = pygame.Surface(
            (
                sw,
                sh
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (
                5,
                2,
                20,
                48
            )
        )

        surface.blit(
            overlay,
            (
                0,
                0
            )
        )

        # =========================================================
        # LOWER DARK GRADIENT
        # =========================================================

        gradient = pygame.Surface(
            (
                sw,
                sh
            ),
            pygame.SRCALPHA
        )

        for y in range(
            sh // 2,
            sh
        ):

            alpha = int(
                15
                + (
                    (
                        y
                        - sh / 2
                    )
                    /
                    (sh / 2)
                )
                * 115
            )

            pygame.draw.line(
                gradient,
                (
                    0,
                    0,
                    10,
                    alpha
                ),
                (
                    0,
                    y
                ),
                (
                    sw,
                    y
                )
            )

        surface.blit(
            gradient,
            (
                0,
                0
            )
        )

        # =========================================================
        # DIMENSIONAL CRACKS
        # =========================================================

        self._draw_cracks(
            surface
        )

        # =========================================================
        # FLOATING PARTICLES
        # =========================================================

        for p in self._particles:

            alpha = int(
                110
                + 70
                * math.sin(
                    t * 2
                    + p["phase"]
                )
            )

            self._draw_particle(
                surface,
                p["x"],
                p["y"],
                p["size"],
                alpha
            )

        # =========================================================
        # TITLE
        # =========================================================

        self._draw_title(
            surface
        )

        # =========================================================
        # BUTTONS
        # =========================================================

        self._draw_buttons(
            surface
        )