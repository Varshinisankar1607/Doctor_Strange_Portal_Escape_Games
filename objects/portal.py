# objects/portal.py
"""
CINEMATIC MYSTICAL PORTAL
Doctor Strange: Portal Escape

Full replacement portal renderer.

Gameplay/collision API is kept compatible with the existing project.
The collision rectangle remains invisible.

Visual style:
- Tall vertical portal
- Multiple magical rings
- Swirling energy
- Glowing runes
- Bright sparks
- Animated inner vortex
- Soft outer glow
- Stage-specific colors
"""

import pygame
import math
import random


# ================================================================
# GAMEPLAY SIZE
# ================================================================

PORTAL_W = 80
PORTAL_H = 110

INTERACT_DIST = 90


# ================================================================
# PORTAL
# ================================================================

class Portal:

    # ------------------------------------------------------------
    # STAGE COLORS
    # ------------------------------------------------------------

    COLORS_BY_STAGE = {
        1: (255, 145, 20),      # Orange / Gold
        2: (40, 190, 255),      # Cyan / Blue
        3: (185, 60, 255),      # Purple
        4: (130, 220, 255),     # Ice Blue
        5: (255, 55, 15),       # Hell Red
    }

    def __init__(
        self,
        x,
        y,
        stage,
        is_correct,
        label="",
        portal_id=0
    ):

        # IMPORTANT:
        # This rectangle is for GAMEPLAY only.
        # It is NOT drawn on screen.

        self.rect = pygame.Rect(
            x,
            y,
            PORTAL_W,
            PORTAL_H
        )

        self.stage = stage
        self.is_correct = is_correct
        self.label = label
        self.portal_id = portal_id

        self.activated = False

        # --------------------------------------------------------
        # Animation
        # --------------------------------------------------------

        self.rotation = random.uniform(
            0,
            math.tau
        )

        self.rotation2 = random.uniform(
            0,
            math.tau
        )

        self.rotation3 = random.uniform(
            0,
            math.tau
        )

        self.pulse = random.uniform(
            0,
            math.tau
        )

        self.swirl_time = random.uniform(
            0,
            math.tau
        )

        # --------------------------------------------------------
        # Particles
        # --------------------------------------------------------

        self.particles = []

        self.spawn_timer = 0.0

        # --------------------------------------------------------
        # Color
        # --------------------------------------------------------

        self.color = self.COLORS_BY_STAGE.get(
            stage,
            (255, 145, 20)
        )


    # ============================================================
    # UPDATE
    # ============================================================

    def update(self, dt):

        # --------------------------------------------------------
        # ROTATING MAGIC
        # --------------------------------------------------------

        self.rotation += dt * 1.7
        self.rotation2 -= dt * 1.15
        self.rotation3 += dt * 2.1

        # --------------------------------------------------------
        # PULSE
        # --------------------------------------------------------

        self.pulse += dt * 3.2

        # --------------------------------------------------------
        # SWIRL
        # --------------------------------------------------------

        self.swirl_time += dt * 4.0

        # --------------------------------------------------------
        # PARTICLE SPAWN
        # --------------------------------------------------------

        self.spawn_timer += dt

        if self.spawn_timer >= 0.035:

            self.spawn_timer = 0

            self._spawn_particle()

        # --------------------------------------------------------
        # UPDATE PARTICLES
        # --------------------------------------------------------

        new_particles = []

        for p in self.particles:

            # x
            # y
            # vx
            # vy
            # life
            # max_life
            # size

            p[4] -= dt

            if p[4] > 0:

                p[0] += p[2] * dt
                p[1] += p[3] * dt

                # Magical floating motion
                p[3] -= 2.0 * dt

                new_particles.append(p)

        self.particles = new_particles

        # Keep particle count under control

        if len(self.particles) > 75:

            self.particles = self.particles[-75:]


    # ============================================================
    # PARTICLES
    # ============================================================

    def _spawn_particle(self):

        cx = self.rect.centerx
        cy = self.rect.centery

        angle = random.uniform(
            0,
            math.tau
        )

        # Tall portal shape

        rx = random.uniform(
            38,
            54
        )

        ry = random.uniform(
            58,
            82
        )

        x = (
            cx
            + math.cos(angle) * rx
        )

        y = (
            cy
            + math.sin(angle) * ry
        )

        # Particles slowly rise

        vx = random.uniform(
            -12,
            12
        )

        vy = random.uniform(
            -35,
            -5
        )

        life = random.uniform(
            0.35,
            0.9
        )

        size = random.choice(
            [1, 1, 2, 2, 3]
        )

        self.particles.append(
            [
                x,
                y,
                vx,
                vy,
                life,
                life,
                size
            ]
        )


    # ============================================================
    # PLAYER DISTANCE
    # ============================================================

    def is_player_nearby(
        self,
        player_rect
    ):

        dx = (
            player_rect.centerx
            - self.rect.centerx
        )

        dy = (
            player_rect.centery
            - self.rect.centery
        )

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        return distance < INTERACT_DIST


    # ============================================================
    # COLOR HELPERS
    # ============================================================

    def _mix_color(
        self,
        color,
        amount
    ):

        return (
            min(
                255,
                int(color[0] + amount)
            ),

            min(
                255,
                int(color[1] + amount)
            ),

            min(
                255,
                int(color[2] + amount)
            )
        )


    # ============================================================
    # DRAW SOFT GLOW
    # ============================================================

    def _draw_glow(
        self,
        surface,
        cx,
        cy
    ):

        size = 190

        glow = pygame.Surface(
            (
                size,
                size
            ),
            pygame.SRCALPHA
        )

        gcx = size // 2
        gcy = size // 2

        pulse = (
            math.sin(self.pulse)
            + 1
        ) * 0.5

        # Large soft glow

        for scale, alpha in [
            (1.00, 18),
            (0.86, 25),
            (0.72, 35),
            (0.60, 48),
        ]:

            w = int(
                90 * scale
                + pulse * 6
            )

            h = int(
                145 * scale
                + pulse * 8
            )

            pygame.draw.ellipse(
                glow,
                (
                    self.color[0],
                    self.color[1],
                    self.color[2],
                    alpha
                ),
                (
                    gcx - w // 2,
                    gcy - h // 2,
                    w,
                    h
                ),
                5
            )

        surface.blit(
            glow,
            (
                cx - size // 2,
                cy - size // 2
            ),
            special_flags=pygame.BLEND_RGBA_ADD
        )


    # ============================================================
    # DRAW DARK PORTAL CENTER
    # ============================================================

    def _draw_center(
        self,
        surface,
        cx,
        cy
    ):

        layer_size = 150

        layer = pygame.Surface(
            (
                layer_size,
                layer_size
            ),
            pygame.SRCALPHA
        )

        lc = layer_size // 2

        # Outer energy

        pygame.draw.ellipse(
            layer,
            (
                self.color[0],
                self.color[1],
                self.color[2],
                100
            ),
            (
                lc - 48,
                lc - 70,
                96,
                140
            )
        )

        # Dark interior

        pygame.draw.ellipse(
            layer,
            (
                3,
                2,
                12,
                240
            ),
            (
                lc - 39,
                lc - 61,
                78,
                122
            )
        )

        # Inner color

        pygame.draw.ellipse(
            layer,
            (
                self.color[0],
                self.color[1],
                self.color[2],
                32
            ),
            (
                lc - 32,
                lc - 52,
                64,
                104
            )
        )

        surface.blit(
            layer,
            (
                cx - layer_size // 2,
                cy - layer_size // 2
            ),
            special_flags=pygame.BLEND_RGBA_ADD
        )


    # ============================================================
    # DRAW MAGICAL RING
    # ============================================================

    def _draw_ring(
        self,
        surface,
        cx,
        cy,
        width,
        height,
        angle,
        alpha,
        thickness
    ):

        size = 190

        ring = pygame.Surface(
            (
                size,
                size
            ),
            pygame.SRCALPHA
        )

        rcx = size // 2
        rcy = size // 2

        # Main ring

        pygame.draw.ellipse(
            ring,
            (
                self.color[0],
                self.color[1],
                self.color[2],
                alpha
            ),
            (
                rcx - width // 2,
                rcy - height // 2,
                width,
                height
            ),
            thickness
        )

        # Bright inner line

        pygame.draw.ellipse(
            ring,
            (
                255,
                225,
                150,
                min(
                    255,
                    alpha + 20
                )
            ),
            (
                rcx - (width - 7) // 2,
                rcy - (height - 7) // 2,
                width - 7,
                height - 7
            ),
            1
        )

        rotated = pygame.transform.rotate(
            ring,
            math.degrees(angle)
        )

        surface.blit(
            rotated,
            (
                cx - rotated.get_width() // 2,
                cy - rotated.get_height() // 2
            ),
            special_flags=pygame.BLEND_RGBA_ADD
        )


    # ============================================================
    # DRAW MAGIC RUNES
    # ============================================================

    def _draw_runes(
        self,
        surface,
        cx,
        cy
    ):

        rune_surface = pygame.Surface(
            (
                190,
                190
            ),
            pygame.SRCALPHA
        )

        rcx = 95
        rcy = 95

        # --------------------------------------------------------
        # Outer rune positions
        # --------------------------------------------------------

        for i in range(12):

            angle = (
                math.tau
                * i
                / 12
            ) + self.rotation3

            radius_x = 48
            radius_y = 68

            x = (
                rcx
                + math.cos(angle)
                * radius_x
            )

            y = (
                rcy
                + math.sin(angle)
                * radius_y
            )

            rune_size = 6

            # Diamond

            points = [
                (
                    int(x),
                    int(y - rune_size)
                ),

                (
                    int(x + rune_size),
                    int(y)
                ),

                (
                    int(x),
                    int(y + rune_size)
                ),

                (
                    int(x - rune_size),
                    int(y)
                )
            ]

            pygame.draw.polygon(
                rune_surface,
                (
                    255,
                    225,
                    150,
                    210
                ),
                points,
                2
            )

            # Tiny center

            pygame.draw.circle(
                rune_surface,
                (
                    255,
                    250,
                    210,
                    230
                ),
                (
                    int(x),
                    int(y)
                ),
                2
            )

        surface.blit(
            rune_surface,
            (
                cx - 95,
                cy - 95
            ),
            special_flags=pygame.BLEND_RGBA_ADD
        )


    # ============================================================
    # DRAW SWIRLING ENERGY
    # ============================================================

    def _draw_swirl(
        self,
        surface,
        cx,
        cy
    ):

        swirl = pygame.Surface(
            (
                130,
                160
            ),
            pygame.SRCALPHA
        )

        sx = 65
        sy = 80

        # --------------------------------------------------------
        # Four independent energy trails
        # --------------------------------------------------------

        for trail in range(5):

            points = []

            phase = (
                self.swirl_time
                + trail * 1.25
            )

            for i in range(55):

                t = i / 54.0

                angle = (
                    phase
                    + t * math.tau * 1.4
                )

                radius = (
                    4
                    + t * 36
                )

                x = (
                    sx
                    + math.cos(angle)
                    * radius
                    * 0.75
                )

                y = (
                    sy
                    + math.sin(angle)
                    * radius
                    * 1.45
                )

                points.append(
                    (
                        int(x),
                        int(y)
                    )
                )

            if len(points) > 1:

                alpha = (
                    145
                    - trail * 20
                )

                pygame.draw.lines(
                    swirl,
                    (
                        self.color[0],
                        self.color[1],
                        self.color[2],
                        alpha
                    ),
                    False,
                    points,
                    2
                )

        surface.blit(
            swirl,
            (
                cx - 65,
                cy - 80
            ),
            special_flags=pygame.BLEND_RGBA_ADD
        )


    # ============================================================
    # DRAW CENTER CORE
    # ============================================================

    def _draw_core(
        self,
        surface,
        cx,
        cy
    ):

        core = pygame.Surface(
            (
                70,
                90
            ),
            pygame.SRCALPHA
        )

        ccx = 35
        ccy = 45

        pulse = (
            1
            + math.sin(
                self.pulse * 1.4
            ) * 0.12
        )

        w = int(
            12 * pulse
        )

        h = int(
            25 * pulse
        )

        # Glow

        pygame.draw.ellipse(
            core,
            (
                self.color[0],
                self.color[1],
                self.color[2],
                90
            ),
            (
                ccx - w * 2,
                ccy - h * 2,
                w * 4,
                h * 4
            )
        )

        # White-hot center

        pygame.draw.ellipse(
            core,
            (
                255,
                240,
                190,
                220
            ),
            (
                ccx - w,
                ccy - h,
                w * 2,
                h * 2
            )
        )

        surface.blit(
            core,
            (
                cx - 35,
                cy - 45
            ),
            special_flags=pygame.BLEND_RGBA_ADD
        )


    # ============================================================
    # DRAW PARTICLES
    # ============================================================

    def _draw_particles(
        self,
        surface,
        camera
    ):

        for p in self.particles:

            x = (
                int(p[0])
                - int(camera.offset_x)
            )

            y = (
                int(p[1])
                - int(camera.offset_y)
            )

            life_ratio = (
                p[4]
                / max(
                    p[5],
                    0.001
                )
            )

            alpha = int(
                255
                * life_ratio
            )

            size = p[6]

            particle = pygame.Surface(
                (
                    14,
                    14
                ),
                pygame.SRCALPHA
            )

            # Soft glow

            pygame.draw.circle(
                particle,
                (
                    self.color[0],
                    self.color[1],
                    self.color[2],
                    alpha // 3
                ),
                (
                    7,
                    7
                ),
                6
            )

            # Bright spark

            pygame.draw.circle(
                particle,
                (
                    255,
                    240,
                    190,
                    alpha
                ),
                (
                    7,
                    7
                ),
                max(
                    1,
                    size
                )
            )

            surface.blit(
                particle,
                (
                    x - 7,
                    y - 7
                ),
                special_flags=pygame.BLEND_RGBA_ADD
            )


    # ============================================================
    # MAIN DRAW
    # ============================================================

    def draw(
        self,
        surface,
        camera,
        font=None
    ):

        # --------------------------------------------------------
        # SCREEN POSITION
        # --------------------------------------------------------

        cx = (
            self.rect.centerx
            - int(camera.offset_x)
        )

        cy = (
            self.rect.centery
            - int(camera.offset_y)
        )

        # --------------------------------------------------------
        # ANIMATED SIZE
        # --------------------------------------------------------

        pulse = math.sin(
            self.pulse
        )

        width = int(
            78
            + pulse * 2
        )

        height = int(
            128
            + pulse * 4
        )

        # ========================================================
        # GLOW
        # ========================================================

        self._draw_glow(
            surface,
            cx,
            cy
        )

        # ========================================================
        # DARK CENTER
        # ========================================================

        self._draw_center(
            surface,
            cx,
            cy
        )

        # ========================================================
        # OUTER RING
        # ========================================================

        self._draw_ring(
            surface,
            cx,
            cy,
            width + 12,
            height + 12,
            self.rotation,
            245,
            4
        )

        # ========================================================
        # SECOND RING
        # ========================================================

        self._draw_ring(
            surface,
            cx,
            cy,
            width + 2,
            height + 2,
            self.rotation2,
            210,
            2
        )

        # ========================================================
        # THIRD RING
        # ========================================================

        self._draw_ring(
            surface,
            cx,
            cy,
            width - 9,
            height - 10,
            self.rotation3,
            180,
            2
        )

        # ========================================================
        # INNER SWIRL
        # ========================================================

        self._draw_swirl(
            surface,
            cx,
            cy
        )

        # ========================================================
        # RUNES
        # ========================================================

        self._draw_runes(
            surface,
            cx,
            cy
        )

        # ========================================================
        # CENTER CORE
        # ========================================================

        self._draw_core(
            surface,
            cx,
            cy
        )

        # ========================================================
        # FOUR ENERGY NODES
        # ========================================================

        for i in range(4):

            angle = (
                self.rotation
                + i * math.pi / 2
            )

            x = (
                cx
                + math.cos(angle)
                * width
                * 0.46
            )

            y = (
                cy
                + math.sin(angle)
                * height
                * 0.46
            )

            pygame.draw.circle(
                surface,
                (
                    255,
                    245,
                    200
                ),
                (
                    int(x),
                    int(y)
                ),
                4
            )

            pygame.draw.circle(
                surface,
                self.color,
                (
                    int(x),
                    int(y)
                ),
                8,
                2
            )

        # ========================================================
        # PARTICLES
        # ========================================================

        self._draw_particles(
            surface,
            camera
        )

        # ========================================================
        # LABEL
        # ========================================================

        if self.label and font:

            text = font.render(
                self.label,
                True,
                (
                    255,
                    225,
                    140
                )
            )

            shadow = font.render(
                self.label,
                True,
                (
                    10,
                    5,
                    15
                )
            )

            label_y = (
                cy
                + height // 2
                + 10
            )

            surface.blit(
                shadow,
                (
                    cx
                    - shadow.get_width() // 2
                    + 2,
                    label_y + 2
                )
            )

            surface.blit(
                text,
                (
                    cx
                    - text.get_width() // 2,
                    label_y
                )
            )


    # ============================================================
    # INTERACTION PROMPT
    # ============================================================

    def draw_interact_prompt(
        self,
        surface,
        camera,
        font
    ):

        if not font:
            return

        cx = (
            self.rect.centerx
            - int(camera.offset_x)
        )

        cy = (
            self.rect.centery
            - int(camera.offset_y)
        )

        text = "[E] ENTER PORTAL"

        rendered = font.render(
            text,
            True,
            (
                255,
                225,
                120
            )
        )

        box_w = (
            rendered.get_width()
            + 24
        )

        box_h = (
            rendered.get_height()
            + 12
        )

        box = pygame.Surface(
            (
                box_w,
                box_h
            ),
            pygame.SRCALPHA
        )

        # Dark transparent background

        box.fill(
            (
                5,
                2,
                18,
                190
            )
        )

        # Magical border

        pygame.draw.rect(
            box,
            (
                self.color[0],
                self.color[1],
                self.color[2],
                230
            ),
            (
                0,
                0,
                box_w,
                box_h
            ),
            2,
            border_radius=6
        )

        bx = (
            cx
            - box_w // 2
        )

        by = (
            cy
            - 90
        )

        surface.blit(
            box,
            (
                bx,
                by
            )
        )

        surface.blit(
            rendered,
            (
                cx
                - rendered.get_width() // 2,
                by + 6
            )
        )