import pygame
import os

from config.controls import INPUT
from player.player_animation import build_animations
from player.player_attack import MysticFlame
from core.collision import collide_rects
from effects.particles import ParticleSystem


# ============================================================
# PLAYER SETTINGS
# ============================================================

PLAYER_SPEED = 220
PLAYER_HP = 100
IFRAMES = 0.6
DAMAGE_PER_HIT = 5


# ============================================================
# DODGE SETTINGS
# ============================================================

DODGE_SPEED = 650
DODGE_DURATION = 0.18
DODGE_COOLDOWN = 0.75


# ============================================================
# PLAYER
# ============================================================

class Player:

    def __init__(self, x, y):

        # Keep original player size
        self.SIZE = (64, 80)

        self.rect = pygame.Rect(
            x,
            y,
            self.SIZE[0],
            self.SIZE[1]
        )

        self.vel = pygame.Vector2(0, 0)

        # Health
        self.hp = PLAYER_HP
        self.max_hp = PLAYER_HP
        self.alive = True

        # Damage protection
        self.iframes = 0.0

        # Animation
        self._anims = build_animations(self.SIZE)
        self._state = "idle"
        self._frame = 0.0
        self._frame_spd = 6.0

        # Direction
        self._facing = "right"

        # Custom player image
        self.custom_player = None
        self.load_custom_player()

        # Attack
        self.attack = MysticFlame()

        # Particles
        self._particles = ParticleSystem()

        # Damage flash
        self._flash = 0.0

        # Existing game variable
        self.fragments_collected = 0

        # Dodge
        self.dodge_timer = 0.0
        self.dodge_cooldown = 0.0
        self.dodge_direction = pygame.Vector2(0, 0)
        self.dodge_invulnerable = False
        self.dodge_was_held = False


    # ========================================================
    # CUSTOM PLAYER IMAGE
    # ========================================================

    def load_custom_player(self):

        player_folder = os.path.dirname(
            os.path.abspath(__file__)
        )

        project_folder = os.path.dirname(
            player_folder
        )

        possible_folders = [
            os.path.join(project_folder, "assests", "player"),
            os.path.join(project_folder, "assets", "player"),
        ]

        possible_images = [
            "doctor_strange_player.png",
            "doctor_strange_player_120x145.jpg",
            "doctor_strange_player.jpg",
            "mystical_sorcerer_player.png",
            "mystical_sorcerer_player.jpg",
            "doctor_strange_player.jpeg",
            "mystical_sorcerer_player.jpeg",
        ]

        image_path = None

        for folder in possible_folders:
            if not os.path.isdir(folder):
                continue
            for filename in possible_images:
                path = os.path.join(folder, filename)
                if os.path.isfile(path):
                    image_path = path
                    print(
                        "[PLAYER] Found custom image:",
                        filename,
                        "in",
                        folder
                    )
                    break
            if image_path is not None:
                break

        if image_path is None:

            print(
                "[PLAYER] No custom player image found."
            )

            print(
                "[PLAYER] Using original player animation."
            )

            return

        try:

            image = pygame.image.load(
                image_path
            ).convert_alpha()

        except Exception as error:

            print(
                "[PLAYER] Could not load image:",
                error
            )

            return

        image = image.copy()

        # If image does not already have an alpha channel with transparency, key out light background
        has_transparency = any(
            image.get_at((x, y))[3] < 255
            for x in (0, image.get_width() - 1)
            for y in (0, image.get_height() - 1)
        )

        if not has_transparency:
            width = image.get_width()
            height = image.get_height()

            for px in range(width):
                for py in range(height):
                    r, g, b, a = image.get_at((px, py))
                    if r > 220 and g > 220 and b > 220:
                        image.set_at((px, py), (r, g, b, 0))

        # Keep original visual size (120, 145)
        if image.get_size() != (120, 145):
            image = pygame.transform.smoothscale(
                image,
                (120, 145)
            )

        self.custom_player = image

        print(
            "[PLAYER] Custom player loaded successfully."
        )


    # ========================================================
    # DODGE
    # ========================================================

    def start_dodge(self, dx, dy):

        if not self.alive:
            return False

        if self.dodge_timer > 0:
            return False

        if self.dodge_cooldown > 0:
            return False

        direction = pygame.Vector2(
            dx,
            dy
        )

        # If player isn't moving,
        # dodge in facing direction.
        if direction.length_squared() == 0:

            if self._facing == "right":

                direction = pygame.Vector2(1, 0)

            elif self._facing == "left":

                direction = pygame.Vector2(-1, 0)

            elif self._facing == "up":

                direction = pygame.Vector2(0, -1)

            else:

                direction = pygame.Vector2(0, 1)

        else:

            direction = direction.normalize()

        self.dodge_direction = direction

        self.dodge_timer = DODGE_DURATION

        self.dodge_cooldown = DODGE_COOLDOWN

        self.dodge_invulnerable = True

        self.vel.update(0, 0)

        # Dodge particles
        self._particles.emit(
            self.rect.centerx,
            self.rect.centery,
            18,
            (180, 80, 255),
            (2, 7),
            (0.15, 0.35),
            (2, 6)
        )

        return True


    # ========================================================
    # INPUT
    # ========================================================

    def handle_input(self, keys, dt=None):

        # Update keyboard + controller
        INPUT.update(keys)

        # ----------------------------------------------------
        # MOVEMENT
        # ----------------------------------------------------

        movement = INPUT.get_movement(keys)

        dx = movement.x
        dy = movement.y

        # ----------------------------------------------------
        # DODGE
        # ----------------------------------------------------

        dodge_pressed = INPUT.dodge_pressed()

        dodge_held = INPUT.dodge_held()

        if (
            dodge_pressed
            and not self.dodge_was_held
        ):

            self.start_dodge(
                dx,
                dy
            )

        self.dodge_was_held = dodge_held

        # ----------------------------------------------------
        # NORMAL MOVEMENT
        # ----------------------------------------------------

        if self.dodge_timer <= 0:

            self.vel.x = dx * PLAYER_SPEED
            self.vel.y = dy * PLAYER_SPEED

        else:

            self.vel.update(0, 0)

        # ----------------------------------------------------
        # FACING
        # ----------------------------------------------------

        if dx > 0:

            self._facing = "right"

        elif dx < 0:

            self._facing = "left"

        elif dy < 0:

            self._facing = "up"

        elif dy > 0:

            self._facing = "down"

        # ----------------------------------------------------
        # ATTACK
        # ----------------------------------------------------

        attack_pressed = INPUT.attack_pressed()

        self.attack.try_attack(
            self.rect,
            self._facing,
            keys,
            attack_input=attack_pressed
        )

        # ----------------------------------------------------
        # PLAYER STATE
        # ----------------------------------------------------

        if not self.alive:

            self._state = "death"

        elif self.dodge_timer > 0:

            self._state = "walk"

        elif self._flash > 0:

            self._state = "damage"

        elif self.attack.active:

            self._state = "attack"

        elif (
            dx != 0
            or dy != 0
        ):

            self._state = "walk"

        else:

            self._state = "idle"


    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        dt,
        walls,
        world_rect
    ):

        # ----------------------------------------------------
        # TIMERS
        # ----------------------------------------------------

        if self.iframes > 0:

            self.iframes -= dt

            if self.iframes < 0:
                self.iframes = 0

        if self._flash > 0:

            self._flash -= dt

            if self._flash < 0:
                self._flash = 0

        if self.dodge_cooldown > 0:

            self.dodge_cooldown -= dt

            if self.dodge_cooldown < 0:
                self.dodge_cooldown = 0

        # ----------------------------------------------------
        # DODGE MOVEMENT
        # ----------------------------------------------------

        if self.dodge_timer > 0:

            self.dodge_timer -= dt

            self.vel = (
                self.dodge_direction
                * DODGE_SPEED
            )

            # X collision
            self.rect.x += int(
                self.vel.x * dt
            )

            correction = collide_rects(
                self.rect,
                walls
            )

            self.rect.x += int(
                correction.x
            )

            # Y collision
            self.rect.y += int(
                self.vel.y * dt
            )

            correction = collide_rects(
                self.rect,
                walls
            )

            self.rect.y += int(
                correction.y
            )

            # World boundaries
            self.rect.clamp_ip(
                world_rect
            )

            # Dodge trail
            self._particles.emit(
                self.rect.centerx,
                self.rect.centery,
                1,
                (180, 80, 255),
                (2, 5),
                (0.10, 0.25),
                (2, 5)
            )

            # Finish dodge
            if self.dodge_timer <= 0:

                self.dodge_timer = 0

                self.dodge_invulnerable = False

                self.vel.update(0, 0)

        # ----------------------------------------------------
        # NORMAL MOVEMENT
        # ----------------------------------------------------

        else:

            # X movement
            self.rect.x += int(
                self.vel.x * dt
            )

            correction = collide_rects(
                self.rect,
                walls
            )

            self.rect.x += int(
                correction.x
            )

            # Y movement
            self.rect.y += int(
                self.vel.y * dt
            )

            correction = collide_rects(
                self.rect,
                walls
            )

            self.rect.y += int(
                correction.y
            )

            # World boundaries
            self.rect.clamp_ip(
                world_rect
            )

        # ----------------------------------------------------
        # ATTACK
        # ----------------------------------------------------

        self.attack.update(
            dt,
            self.rect
        )

        # ----------------------------------------------------
        # PARTICLES
        # ----------------------------------------------------

        self._particles.update(dt)

        # ----------------------------------------------------
        # ANIMATION
        # ----------------------------------------------------

        if self._state in self._anims:

            frames = self._anims[
                self._state
            ]

            if frames:

                self._frame = (
                    self._frame
                    + self._frame_spd * dt
                ) % len(frames)


    # ========================================================
    # TAKE DAMAGE
    # ========================================================

    def take_damage(self, amount):

        # Dodge = invulnerable
        if self.dodge_invulnerable:

            return False

        # Existing i-frames
        if self.iframes > 0:

            return False

        if not self.alive:

            return False

        self.hp = max(
            0,
            self.hp - amount
        )

        self.iframes = IFRAMES

        self._flash = 0.25

        # Damage particles
        self._particles.emit(
            self.rect.centerx,
            self.rect.centery,
            12,
            (255, 80, 80),
            (2, 5),
            (0.20, 0.50),
            (2, 5)
        )

        # Death
        if self.hp <= 0:

            self.hp = 0

            self.alive = False

            self.vel.update(
                0,
                0
            )

        return True


    # ========================================================
    # HEAL
    # ========================================================

    def heal(self, amount):

        self.hp = min(
            self.max_hp,
            self.hp + amount
        )


    # ========================================================
    # DRAW
    # ========================================================

    def draw(
        self,
        surface,
        camera
    ):

        # ----------------------------------------------------
        # INVINCIBILITY BLINK
        # ----------------------------------------------------

        visible = True

        if self.iframes > 0:

            visible = (
                int(
                    self.iframes * 10
                ) % 2 == 0
            )

        if self.dodge_invulnerable:

            visible = True

        if not visible:

            return

        # ----------------------------------------------------
        # CUSTOM PLAYER
        # ----------------------------------------------------

        if self.custom_player is not None:

            sprite = self.custom_player

            # Face left
            if self._facing == "left":

                sprite = pygame.transform.flip(
                    sprite,
                    True,
                    False
                )

            # Damage flash
            if self._flash > 0:

                sprite = sprite.copy()

                flash = pygame.Surface(
                    sprite.get_size(),
                    pygame.SRCALPHA
                )

                flash.fill(
                    (255, 60, 60, 80)
                )

                sprite.blit(
                    flash,
                    (0, 0),
                    special_flags=pygame.BLEND_RGBA_ADD
                )

            # Dodge glow
            if self.dodge_invulnerable:

                sprite = sprite.copy()

                glow = pygame.Surface(
                    sprite.get_size(),
                    pygame.SRCALPHA
                )

                glow.fill(
                    (180, 80, 255, 35)
                )

                sprite.blit(
                    glow,
                    (0, 0),
                    special_flags=pygame.BLEND_RGBA_ADD
                )

            screen_rect = camera.apply(
                self.rect
            )

            draw_x = (
                screen_rect.centerx
                - sprite.get_width() // 2
            )

            draw_y = (
                screen_rect.centery
                - sprite.get_height() // 2
            )

            surface.blit(
                sprite,
                (draw_x, draw_y)
            )

        # ----------------------------------------------------
        # ORIGINAL PLAYER ANIMATION
        # ----------------------------------------------------

        else:

            if self._state in self._anims:

                frames = self._anims[
                    self._state
                ]

                if frames:

                    index = (
                        int(self._frame)
                        % len(frames)
                    )

                    sprite = frames[
                        index
                    ]

                    screen_rect = camera.apply(
                        self.rect
                    )

                    surface.blit(
                        sprite,
                        screen_rect.topleft
                    )

        # ----------------------------------------------------
        # ATTACK PARTICLES
        # ----------------------------------------------------

        self.attack.draw(
            surface,
            camera
        )

        # ----------------------------------------------------
        # PLAYER PARTICLES
        # ----------------------------------------------------

        self._particles.draw(
            surface,
            camera
        )


    # ========================================================
    # CENTER
    # ========================================================

    @property
    def center(self):

        return self.rect.center