# enemies/enemy.py

"""Base enemy class with procedural visuals and combat support."""

import pygame
import math

from effects.particles import ParticleSystem


# ============================================================
# ENEMY SETTINGS
# ============================================================

ENEMY_HP_BASE = 60
ENEMY_SPEED_BASE = 90
ENEMY_DMG_BASE = 5
ENEMY_ATTACK_CD = 1.0


# ============================================================
# ENEMY VISUALS
# ============================================================

def _draw_enemy_frame(
    kind: str,
    frame: int,
    size=(52, 64)
):

    w, h = size

    surf = pygame.Surface(
        size,
        pygame.SRCALPHA
    )

    # Walking animation
    leg_off = int(
        math.sin(frame * 1.4) * 4
    )

    arm_swing = int(
        math.sin(frame * 1.4) * 5
    )

    # Colors
    body_col = {
        "patrol": (60, 30, 90),
        "chaser": (80, 20, 20),
        "attacker": (40, 60, 20)
    }.get(
        kind,
        (60, 30, 90)
    )

    armor_col = {
        "patrol": (130, 80, 180),
        "chaser": (180, 50, 50),
        "attacker": (80, 150, 40)
    }.get(
        kind,
        (130, 80, 180)
    )

    eye_col = (
        255,
        50,
        0
    )

    # ========================================================
    # LEGS
    # ========================================================

    pygame.draw.rect(
        surf,
        body_col,
        (
            w // 2 - 10,
            h // 2 + 10,
            8,
            16 + leg_off
        ),
        border_radius=3
    )

    pygame.draw.rect(
        surf,
        body_col,
        (
            w // 2 + 2,
            h // 2 + 10,
            8,
            16 - leg_off
        ),
        border_radius=3
    )

    # ========================================================
    # TORSO
    # ========================================================

    pygame.draw.rect(
        surf,
        body_col,
        (
            w // 2 - 13,
            h // 2 - 10,
            26,
            22
        ),
        border_radius=4
    )

    pygame.draw.polygon(
        surf,
        armor_col,
        [
            (w // 2 - 13, h // 2 - 10),
            (w // 2 + 13, h // 2 - 10),
            (w // 2 + 10, h // 2 + 5),
            (w // 2 - 10, h // 2 + 5)
        ]
    )

    # ========================================================
    # ARMS
    # ========================================================

    pygame.draw.line(
        surf,
        body_col,
        (
            w // 2 - 13,
            h // 2 - 4
        ),
        (
            w // 2 - 22,
            h // 2 + 10 + arm_swing
        ),
        5
    )

    pygame.draw.line(
        surf,
        body_col,
        (
            w // 2 + 13,
            h // 2 - 4
        ),
        (
            w // 2 + 22,
            h // 2 + 10 - arm_swing
        ),
        5
    )

    # Fists
    pygame.draw.circle(
        surf,
        armor_col,
        (
            w // 2 - 22,
            h // 2 + 14 + arm_swing
        ),
        5
    )

    pygame.draw.circle(
        surf,
        armor_col,
        (
            w // 2 + 22,
            h // 2 + 14 - arm_swing
        ),
        5
    )

    # ========================================================
    # HEAD
    # ========================================================

    head_y = h // 2 - 26

    pygame.draw.ellipse(
        surf,
        body_col,
        (
            w // 2 - 10,
            head_y,
            20,
            20
        )
    )

    # Helmet
    pygame.draw.arc(
        surf,
        armor_col,
        (
            w // 2 - 11,
            head_y - 2,
            22,
            14
        ),
        0,
        math.pi,
        5
    )

    # Eyes
    pygame.draw.circle(
        surf,
        eye_col,
        (
            w // 2 - 4,
            head_y + 10
        ),
        3
    )

    pygame.draw.circle(
        surf,
        eye_col,
        (
            w // 2 + 4,
            head_y + 10
        ),
        3
    )

    return surf


# ============================================================
# ANIMATIONS
# ============================================================

def build_enemy_animations(
    kind: str,
    size=(52, 64)
):

    states = {
        "walk": 8,
        "attack": 6,
        "death": 6,
        "idle": 6
    }

    animations = {}

    for state, frame_count in states.items():

        animations[state] = [
            _draw_enemy_frame(
                kind,
                frame,
                size
            )
            for frame in range(frame_count)
        ]

    return animations


# ============================================================
# ENEMY
# ============================================================

class Enemy:

    def __init__(
        self,
        x,
        y,
        kind="patrol",
        hp=None,
        speed=None,
        damage=None
    ):

        self.kind = kind

        self.rect = pygame.Rect(
            x,
            y,
            52,
            64
        )

        self.hp = (
            hp
            if hp is not None
            else ENEMY_HP_BASE
        )

        self.max_hp = self.hp

        self.speed = (
            speed
            if speed is not None
            else ENEMY_SPEED_BASE
        )

        self.damage = (
            damage
            if damage is not None
            else ENEMY_DMG_BASE
        )

        self.alive = True

        # ====================================================
        # ANIMATION
        # ====================================================

        self._anims = build_enemy_animations(
            kind,
            (52, 64)
        )

        self._state = "idle"

        self._frame = 0.0

        self._frame_speed = 8.0

        # ====================================================
        # COMBAT
        # ====================================================

        self._attack_cd = 0.0

        self._flash = 0.0

        self._flash_col = (
            255,
            255,
            255
        )

        # ====================================================
        # DEATH
        # ====================================================

        self._death_timer = 0.0

        # ====================================================
        # PARTICLES
        # ====================================================

        self.particles = ParticleSystem()

        # ====================================================
        # MOVEMENT
        # ====================================================

        self.vel = pygame.Vector2(
            0,
            0
        )

    # ========================================================
    # TAKE DAMAGE
    # ========================================================

    def take_damage(
        self,
        amount: int
    ):

        if not self.alive:

            return False

        amount = max(
            0,
            int(amount)
        )

        self.hp -= amount

        self._flash = 0.2

        # Hit particles
        self.particles.emit(
            self.rect.centerx,
            self.rect.centery,
            8,
            (
                255,
                150,
                0
            ),
            (2, 5),
            (0.1, 0.3)
        )

        # ====================================================
        # DEATH
        # ====================================================

        if self.hp <= 0:

            self.hp = 0

            self.alive = False

            self._state = "death"

            self._frame = 0.0

            self._death_timer = 0.0

            # Death particles
            self.particles.emit(
                self.rect.centerx,
                self.rect.centery,
                20,
                (
                    200,
                    80,
                    20
                ),
                (2, 6),
                (0.3, 0.7)
            )

            return True

        return False

    # ========================================================
    # KNOCKBACK
    # ========================================================

    def knockback(
        self,
        angle: float,
        distance: float = 70.0
    ):

        if not self.alive:

            return

        dx = (
            math.cos(angle)
            * distance
        )

        dy = (
            math.sin(angle)
            * distance
        )

        self.rect.x += int(dx)

        self.rect.y += int(dy)

        self.vel.update(
            0,
            0
        )

    # ========================================================
    # ATTACK COOLDOWN
    # ========================================================

    def can_attack(self):

        return self._attack_cd <= 0

    def reset_attack_cd(self):

        self._attack_cd = (
            ENEMY_ATTACK_CD
        )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        dt,
        walls=None
    ):

        # Attack cooldown
        if self._attack_cd > 0:

            self._attack_cd -= dt

            if self._attack_cd < 0:

                self._attack_cd = 0

        # Hit flash
        if self._flash > 0:

            self._flash -= dt

            if self._flash < 0:

                self._flash = 0

        # ====================================================
        # DEAD
        # ====================================================

        if not self.alive:

            self._death_timer += dt

            self._frame = min(
                self._frame
                + self._frame_speed * dt,
                len(
                    self._anims["death"]
                ) - 1
            )

            self.particles.update(
                dt
            )

            return

        # ====================================================
        # MOVEMENT
        # ====================================================

        if self.vel.length() > 0:

            self.rect.x += int(
                self.vel.x * dt
            )

            if walls:

                from core.collision import collide_rects

                mtv = collide_rects(
                    self.rect,
                    walls
                )

                self.rect.x += int(
                    mtv.x
                )

            self.rect.y += int(
                self.vel.y * dt
            )

            if walls:

                from core.collision import collide_rects

                mtv = collide_rects(
                    self.rect,
                    walls
                )

                self.rect.y += int(
                    mtv.y
                )

            self._state = "walk"

        else:

            self._state = "idle"

        # ====================================================
        # ANIMATION
        # ====================================================

        current_animation = self._anims[
            self._state
        ]

        self._frame = (
            self._frame
            + self._frame_speed * dt
        ) % len(current_animation)

        # ====================================================
        # PARTICLES
        # ====================================================

        self.particles.update(
            dt
        )

    # ========================================================
    # DRAW
    # ========================================================

    def draw(
        self,
        surface,
        camera
    ):

        # Fully finished death
        if (
            not self.alive
            and self._death_timer > 0.6
        ):

            self.particles.draw(
                surface,
                camera
            )

            return

        # Camera-compatible positioning
        r = camera.apply(
            self.rect
        )

        animation = self._anims[
            self._state
        ]

        frame_idx = min(
            int(self._frame),
            len(animation) - 1
        )

        sprite = animation[
            frame_idx
        ]

        # ====================================================
        # DAMAGE FLASH
        # ====================================================

        if self._flash > 0:

            flash = pygame.Surface(
                sprite.get_size(),
                pygame.SRCALPHA
            )

            flash.fill(
                (
                    255,
                    255,
                    255,
                    180
                )
            )

            sprite = sprite.copy()

            sprite.blit(
                flash,
                (0, 0)
            )

        surface.blit(
            sprite,
            r.topleft
        )

        # ====================================================
        # HEALTH BAR
        # ====================================================

        if self.alive:

            bar_width = 44
            bar_height = 5

            bar_x = (
                r.centerx
                - bar_width // 2
            )

            bar_y = (
                r.top
                - 10
            )

            pygame.draw.rect(
                surface,
                (
                    60,
                    10,
                    10
                ),
                (
                    bar_x,
                    bar_y,
                    bar_width,
                    bar_height
                ),
                border_radius=2
            )

            if self.max_hp > 0:

                fill_width = int(
                    bar_width
                    * self.hp
                    / self.max_hp
                )

            else:

                fill_width = 0

            pygame.draw.rect(
                surface,
                (
                    200,
                    40,
                    40
                ),
                (
                    bar_x,
                    bar_y,
                    fill_width,
                    bar_height
                ),
                border_radius=2
            )

        # ====================================================
        # PARTICLES
        # ====================================================

        self.particles.draw(
            surface,
            camera
        )