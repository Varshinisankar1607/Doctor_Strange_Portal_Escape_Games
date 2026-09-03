# ============================================================
# enemies/enemy_manager.py
# ============================================================

import pygame
import random

from enemies.enemy_types import (
    PatrolEnemy,
    ChaserEnemy,
    AttackerEnemy
)

from config.difficulty import DIFFICULTIES, STAGE_SCALE
from config.scoring import SCORING


class EnemyManager:

    def __init__(
        self,
        stage: int,
        difficulty: str,
        spawn_zones: list,
        player_start,
        world_rect: pygame.Rect
    ):

        self.stage = stage
        self.difficulty = difficulty
        self.spawn_zones = spawn_zones
        self.player_start = player_start
        self.world_rect = world_rect

        self.enemies = []

        self._kill_count = 0
        self._kill_cap = SCORING["enemy_kill_cap"]
        self._enemies_created = 0

        diff = DIFFICULTIES[difficulty]
        scale = STAGE_SCALE[stage]

        self._count_mult = (
            diff["enemy_count_mult"] * scale
        )

        self._speed_mult = (
            diff["enemy_speed_mult"] * scale
        )

        self._damage_mult = (
            diff["damage_mult"]
        )

        # Prevent one fire attack from hitting
        # the same enemy every single frame.
        self._attack_hit_enemies = set()

    # ========================================================
    # SAFE SPAWN
    # ========================================================

    def _safe_spawn_pos(self, size=(52, 64)):

        for _ in range(30):

            zone = random.choice(
                self.spawn_zones
            )

            x = random.randint(
                zone[0],
                zone[0] + zone[2] - size[0]
            )

            y = random.randint(
                zone[1],
                zone[1] + zone[3] - size[1]
            )

            px, py = self.player_start

            if (
                abs(x - px) > 200
                or abs(y - py) > 200
            ):
                return x, y

        return (
            self.spawn_zones[0][0],
            self.spawn_zones[0][1]
        )

    # ========================================================
    # SPAWN WAVE
    # ========================================================

    def spawn_wave(self, base_count: int):

        count = max(
            1,
            int(
                base_count * self._count_mult
            )
        )

        types = [
            PatrolEnemy,
            ChaserEnemy,
            AttackerEnemy
        ]

        weights = {
            1: [0.5, 0.3, 0.2],
            2: [0.35, 0.4, 0.25],
            3: [0.25, 0.4, 0.35],
            4: [0.2, 0.4, 0.4],
            5: [0.1, 0.45, 0.45]
        }.get(
            self.stage,
            [0.33, 0.33, 0.34]
        )

        from enemies.enemy import (
            ENEMY_HP_BASE,
            ENEMY_SPEED_BASE,
            ENEMY_DMG_BASE
        )

        for _ in range(count):

            enemy_class = random.choices(
                types,
                weights=weights
            )[0]

            x, y = self._safe_spawn_pos()

            enemy = enemy_class(
                x,
                y,
                hp=int(
                    ENEMY_HP_BASE
                    * self._count_mult
                    * 0.7
                ),
                speed=int(
                    ENEMY_SPEED_BASE
                    * self._speed_mult
                ),
                damage=int(
                    ENEMY_DMG_BASE
                    * self._damage_mult
                )
            )

            self.enemies.append(enemy)

        self._enemies_created += count

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        dt: float,
        player,
        walls: list
    ) -> int:

        score_delta = 0

        # ----------------------------------------------------
        # CURRENT FIRE HITBOX
        # ----------------------------------------------------

        hitbox = player.attack.get_hitbox(
            player.rect
        )

        # ----------------------------------------------------
        # If there is NO fire currently active,
        # reset hit tracking.
        # ----------------------------------------------------

        if hitbox is None:

            self._attack_hit_enemies.clear()

        # ====================================================
        # ENEMY LOOP
        # ====================================================

        for enemy in self.enemies:

            # ------------------------------------------------
            # DEAD ENEMY
            # ------------------------------------------------

            if not enemy.alive:

                enemy.update(
                    dt,
                    walls
                )

                continue

            # ------------------------------------------------
            # ENEMY AI
            # ------------------------------------------------

            hit_player = enemy.think(
                player.rect,
                dt
            )

            # ------------------------------------------------
            # ENEMY MOVEMENT
            # ------------------------------------------------

            enemy.update(
                dt,
                walls
            )

            # ------------------------------------------------
            # ENEMY ATTACK -> PLAYER
            # ------------------------------------------------

            if hit_player:

                damaged = player.take_damage(
                    enemy.damage
                )

                if damaged:

                    score_delta += (
                        SCORING[
                            "hazard_hit_penalty"
                        ]
                    )

            # =================================================
            # FIRE -> ENEMY
            # =================================================

            current_hitbox = (
                player.attack.get_hitbox(
                    player.rect
                )
            )

            if (
                current_hitbox is not None
                and enemy.alive
                and enemy not in self._attack_hit_enemies
                and current_hitbox.colliderect(
                    enemy.rect
                )
            ):

                from player.player_attack import (
                    ATTACK_DAMAGE
                )

                # ------------------------------------------------
                # DAMAGE
                # ------------------------------------------------

                just_died = enemy.take_damage(
                    ATTACK_DAMAGE
                )

                # Remember this enemy for THIS fire attack.
                self._attack_hit_enemies.add(
                    enemy
                )

                # ------------------------------------------------
                # KNOCKBACK
                # ------------------------------------------------

                if not just_died:

                    enemy.knockback(
                        player.attack.angle,
                        distance=70.0
                    )

                # ------------------------------------------------
                # SCORE
                # ------------------------------------------------

                if just_died:

                    if (
                        self._kill_count
                        < self._kill_cap
                    ):

                        self._kill_count += 1

                        score_delta += (
                            SCORING[
                                "enemy_kill_bonus"
                            ]
                        )

        # ====================================================
        # REMOVE DEAD ENEMIES
        # ====================================================

        self.enemies = [
            enemy
            for enemy in self.enemies
            if not (
                not enemy.alive
                and enemy._death_timer > 1.0
            )
        ]

        return score_delta

    # ========================================================
    # DRAW
    # ========================================================

    def draw(
        self,
        surface,
        camera
    ):

        for enemy in self.enemies:

            enemy.draw(
                surface,
                camera
            )

    # ========================================================
    # ALL DEAD
    # ========================================================

    def all_dead(self) -> bool:

        return all(
            not enemy.alive
            for enemy in self.enemies
        )

    # ========================================================
    # LIVING COUNT
    # ========================================================

    def living_count(self) -> int:

        return sum(
            1
            for enemy in self.enemies
            if enemy.alive
        )

    # ========================================================
    # CLEANUP
    # ========================================================

    def cleanup(self):

        self.enemies.clear()

        self._attack_hit_enemies.clear()