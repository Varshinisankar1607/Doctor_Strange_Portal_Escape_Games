# ============================================================
# player/player_attack.py
# MYSTIC FLAME ATTACK - VISUAL UPGRADE
# ============================================================

import pygame
import math
import random

from effects.particles import ParticleSystem


# ============================================================
# ATTACK SETTINGS
# ============================================================

ATTACK_COOLDOWN = 0.40
ATTACK_DURATION = 0.28

ATTACK_DAMAGE = 30

ATTACK_RANGE = 120
ATTACK_WIDTH = 90


# ============================================================
# MYSTIC FLAME
# ============================================================

class MysticFlame:

    def __init__(self):

        self.cooling = 0.0
        self.active = False
        self.timer = 0.0

        self.particles = ParticleSystem()

        self.angle = 0.0

        self.attack_was_held = False

        # ----------------------------------------------------
        # Visual animation
        # ----------------------------------------------------

        self.visual_time = 0.0

        self.flame_seed = random.random()

    # ========================================================
    # ATTACK
    # ========================================================

    def try_attack(
        self,
        player_rect,
        facing,
        keys=None,
        attack_input=None
    ):

        # ----------------------------------------------------
        # BACKWARD COMPATIBILITY
        # ----------------------------------------------------

        if attack_input is None:

            attack_input = False

            if keys is not None:

                try:

                    from config.controls import ATTACK

                    attack_input = any(
                        keys[k]
                        for k in ATTACK
                    )

                except Exception:

                    attack_input = False

        # ----------------------------------------------------
        # BUTTON RELEASE
        # ----------------------------------------------------

        if not attack_input:

            self.attack_was_held = False

            return False

        # ----------------------------------------------------
        # PREVENT REPEATED FIRE WHILE HELD
        # ----------------------------------------------------

        if self.attack_was_held:

            return False

        self.attack_was_held = True

        # ----------------------------------------------------
        # COOLDOWN
        # ----------------------------------------------------

        if self.cooling > 0:

            return False

        # ----------------------------------------------------
        # DIRECTION
        # ----------------------------------------------------

        angles = {

            "right": 0.0,

            "left": math.pi,

            "up": -math.pi / 2,

            "down": math.pi / 2
        }

        self.angle = angles.get(
            facing,
            0.0
        )

        # ----------------------------------------------------
        # START ATTACK
        # ----------------------------------------------------

        self.active = True

        self.timer = ATTACK_DURATION

        self.cooling = ATTACK_COOLDOWN

        self.visual_time = 0.0

        self.flame_seed = random.random()

        # ----------------------------------------------------
        # PLAYER CENTER
        # ----------------------------------------------------

        cx = player_rect.centerx
        cy = player_rect.centery

        # ----------------------------------------------------
        # BIG INITIAL BURST
        # ----------------------------------------------------

        for _ in range(35):

            spread = random.uniform(
                -0.48,
                0.48
            )

            particle_angle = (
                self.angle
                + spread
            )

            distance = random.uniform(
                12,
                48
            )

            px = (
                cx
                + math.cos(particle_angle)
                * distance
            )

            py = (
                cy
                + math.sin(particle_angle)
                * distance
            )

            colour = random.choice(
                [
                    (255, 70, 0),
                    (255, 110, 0),
                    (255, 170, 0),
                    (255, 220, 40),
                    (255, 245, 140)
                ]
            )

            self.particles.emit(
                px,
                py,
                1,
                colour,
                (3, 9),
                (0.15, 0.35),
                (2, 7)
            )

        return True

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        dt,
        player_rect
    ):

        # ----------------------------------------------------
        # COOLDOWN
        # ----------------------------------------------------

        if self.cooling > 0:

            self.cooling -= dt

            if self.cooling < 0:

                self.cooling = 0.0

        # ----------------------------------------------------
        # FLAME ACTIVE
        # ----------------------------------------------------

        if self.active:

            self.timer -= dt

            self.visual_time += dt

            cx = player_rect.centerx
            cy = player_rect.centery

            # ------------------------------------------------
            # CONTINUOUS FIRE PARTICLES
            # ------------------------------------------------

            for _ in range(12):

                distance = random.uniform(
                    25,
                    ATTACK_RANGE
                )

                # Wider near the end
                spread_amount = (
                    0.10
                    + (distance / ATTACK_RANGE)
                    * 0.25
                )

                spread = random.uniform(
                    -spread_amount,
                    spread_amount
                )

                particle_angle = (
                    self.angle
                    + spread
                )

                px = (
                    cx
                    + math.cos(particle_angle)
                    * distance
                )

                py = (
                    cy
                    + math.sin(particle_angle)
                    * distance
                )

                colour = random.choice(
                    [
                        (255, 80, 0),
                        (255, 120, 0),
                        (255, 170, 0),
                        (255, 210, 30),
                        (255, 240, 120)
                    ]
                )

                self.particles.emit(
                    px,
                    py,
                    1,
                    colour,
                    (2, 8),
                    (0.08, 0.25),
                    (2, 7)
                )

            # ------------------------------------------------
            # ATTACK END
            # ------------------------------------------------

            if self.timer <= 0:

                self.timer = 0.0

                self.active = False

        # ----------------------------------------------------
        # PARTICLES
        # ----------------------------------------------------

        self.particles.update(dt)

    # ========================================================
    # CANCEL
    # ========================================================

    def cancel(self):

        self.active = False

        self.timer = 0.0

        self.attack_was_held = True

    # ========================================================
    # HITBOX
    # ========================================================

    def get_hitbox(
        self,
        player_rect
    ):

        if not self.active:

            return None

        cx = player_rect.centerx
        cy = player_rect.centery

        start_distance = 25

        start_x = (
            cx
            + math.cos(self.angle)
            * start_distance
        )

        start_y = (
            cy
            + math.sin(self.angle)
            * start_distance
        )

        # ----------------------------------------------------
        # HORIZONTAL
        # ----------------------------------------------------

        if abs(
            math.cos(self.angle)
        ) > 0.5:

            length = ATTACK_RANGE
            width = ATTACK_WIDTH

            if math.cos(self.angle) > 0:

                left = int(start_x)

            else:

                left = int(
                    start_x - length
                )

            top = int(
                start_y - width / 2
            )

            return pygame.Rect(
                left,
                top,
                length,
                width
            )

        # ----------------------------------------------------
        # VERTICAL
        # ----------------------------------------------------

        length = ATTACK_RANGE
        width = ATTACK_WIDTH

        if math.sin(self.angle) > 0:

            top = int(start_y)

        else:

            top = int(
                start_y - length
            )

        left = int(
            start_x - width / 2
        )

        return pygame.Rect(
            left,
            top,
            width,
            length
        )

    # ========================================================
    # DRAW BIG FLAME
    # ========================================================

    def draw(
        self,
        surface,
        camera
    ):

        # Always draw particles
        self.particles.draw(
            surface,
            camera
        )

        if not self.active:

            return

        # ----------------------------------------------------
        # IMPORTANT
        # World -> screen
        # ----------------------------------------------------

        # We don't have player_rect here, so the particle
        # system handles the small sparks. The large flame
        # is drawn using the particles' visible region below.
        #
        # To keep the existing API unchanged, this method
        # uses the particle list for the animated effect.
        # ----------------------------------------------------

        # Large glow particles
        for _ in range(7):

            # Generate screen-space glow around the active
            # flame area using camera center.
            #
            # Find approximate center from camera position.
            sx = (
                surface.get_width() // 2
            )

            sy = (
                surface.get_height() // 2
            )

            # Random glow around center
            gx = sx + random.randint(
                -35,
                35
            )

            gy = sy + random.randint(
                -25,
                25
            )

            radius = random.randint(
                4,
                11
            )

            glow = pygame.Surface(
                (
                    radius * 4,
                    radius * 4
                ),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                glow,
                (255, 120, 0, 40),
                (
                    radius * 2,
                    radius * 2
                ),
                radius * 2
            )

            surface.blit(
                glow,
                (
                    gx - radius * 2,
                    gy - radius * 2
                )
            )

    # ========================================================
    # COOLDOWN %
    # ========================================================

    @property
    def cooldown_pct(self):

        if ATTACK_COOLDOWN <= 0:

            return 0.0

        return max(
            0.0,
            min(
                1.0,
                self.cooling
                / ATTACK_COOLDOWN
            )
        )