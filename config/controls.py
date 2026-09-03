import pygame


# ============================================================
# KEYBOARD CONTROLS
# ============================================================

MOVE_UP = [
    pygame.K_w,
    pygame.K_UP
]

MOVE_DOWN = [
    pygame.K_s,
    pygame.K_DOWN
]

MOVE_LEFT = [
    pygame.K_a,
    pygame.K_LEFT
]

MOVE_RIGHT = [
    pygame.K_d,
    pygame.K_RIGHT
]

ATTACK = [
    pygame.K_SPACE
]

DODGE = [
    pygame.K_LSHIFT,
    pygame.K_RSHIFT
]

INTERACT = [
    pygame.K_e
]

PAUSE = [
    pygame.K_ESCAPE
]

FULLSCREEN = [
    pygame.K_F11
]

CONFIRM = [
    pygame.K_RETURN,
    pygame.K_KP_ENTER
]


# ============================================================
# CONTROLLER BUTTONS
# ============================================================

# Standard Xbox / PlayStation SDL layout
#
# 0 = A / Cross
# 1 = B / Circle
# 2 = X / Square
# 3 = Y / Triangle
# 7 = Start
#
# Movement = Left Stick

CONTROLLER_INTERACT = 0
CONTROLLER_DODGE = 1
CONTROLLER_ATTACK = 2
CONTROLLER_PAUSE = 7

CONTROLLER_AXIS_X = 0
CONTROLLER_AXIS_Y = 1

CONTROLLER_DEADZONE = 0.20


# ============================================================
# INPUT MANAGER
# ============================================================

class InputManager:

    def __init__(self):

        self.joystick = None
        self.controller_connected = False

        self.current_attack = False
        self.current_dodge = False
        self.current_interact = False
        self.current_pause = False

        self.previous_attack = False
        self.previous_dodge = False
        self.previous_interact = False
        self.previous_pause = False

        self.last_input_device = "keyboard"

        self._setup_controller()


    # ========================================================
    # CONTROLLER SETUP
    # ========================================================

    def _setup_controller(self):

        try:

            pygame.joystick.init()

            if pygame.joystick.get_count() > 0:

                self.joystick = pygame.joystick.Joystick(0)

                if not self.joystick.get_init():
                    self.joystick.init()

                self.controller_connected = True

                print(
                    "[INPUT] Controller connected:",
                    self.joystick.get_name()
                )

        except Exception as e:

            self.joystick = None
            self.controller_connected = False

            print(
                "[INPUT] Controller unavailable:",
                e
            )


    # ========================================================
    # CHECK CONTROLLER
    # ========================================================

    def _check_controller(self):

        try:

            pygame.joystick.init()

            count = pygame.joystick.get_count()

            if count <= 0:

                self.joystick = None
                self.controller_connected = False

                return

            if self.joystick is None:

                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()

            self.controller_connected = True

        except Exception:

            self.joystick = None
            self.controller_connected = False


    # ========================================================
    # GET BUTTON
    # ========================================================

    def _button(self, button):

        if not self.controller_connected:
            return False

        if self.joystick is None:
            return False

        try:

            if button >= self.joystick.get_numbuttons():
                return False

            return bool(
                self.joystick.get_button(button)
            )

        except Exception:

            return False


    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, keys):

        self._check_controller()

        # Save previous state
        self.previous_attack = self.current_attack
        self.previous_dodge = self.current_dodge
        self.previous_interact = self.current_interact
        self.previous_pause = self.current_pause

        # ----------------------------------------------------
        # KEYBOARD
        # ----------------------------------------------------

        keyboard_attack = any(
            keys[k]
            for k in ATTACK
        )

        keyboard_dodge = any(
            keys[k]
            for k in DODGE
        )

        keyboard_interact = any(
            keys[k]
            for k in INTERACT
        )

        keyboard_pause = any(
            keys[k]
            for k in PAUSE
        )

        # ----------------------------------------------------
        # CONTROLLER
        # ----------------------------------------------------

        controller_attack = self._button(
            CONTROLLER_ATTACK
        )

        controller_dodge = self._button(
            CONTROLLER_DODGE
        )

        controller_interact = self._button(
            CONTROLLER_INTERACT
        )

        controller_pause = self._button(
            CONTROLLER_PAUSE
        )

        # ----------------------------------------------------
        # COMBINE
        # ----------------------------------------------------

        self.current_attack = (
            keyboard_attack
            or controller_attack
        )

        self.current_dodge = (
            keyboard_dodge
            or controller_dodge
        )

        self.current_interact = (
            keyboard_interact
            or controller_interact
        )

        self.current_pause = (
            keyboard_pause
            or controller_pause
        )

        # ----------------------------------------------------
        # DEVICE DETECTION
        # ----------------------------------------------------

        if (
            controller_attack
            or controller_dodge
            or controller_interact
            or controller_pause
        ):

            self.last_input_device = "controller"

        elif (
            keyboard_attack
            or keyboard_dodge
            or keyboard_interact
            or keyboard_pause
        ):

            self.last_input_device = "keyboard"


    # ========================================================
    # MOVEMENT
    # ========================================================

    def get_movement(self, keys):

        x = 0
        y = 0

        # Keyboard
        if any(keys[k] for k in MOVE_LEFT):
            x -= 1

        if any(keys[k] for k in MOVE_RIGHT):
            x += 1

        if any(keys[k] for k in MOVE_UP):
            y -= 1

        if any(keys[k] for k in MOVE_DOWN):
            y += 1

        keyboard_movement = pygame.Vector2(
            x,
            y
        )

        # Controller
        controller_movement = pygame.Vector2(
            0,
            0
        )

        if (
            self.controller_connected
            and self.joystick is not None
        ):

            try:

                if self.joystick.get_numaxes() >= 2:

                    controller_movement.x = (
                        self.joystick.get_axis(
                            CONTROLLER_AXIS_X
                        )
                    )

                    controller_movement.y = (
                        self.joystick.get_axis(
                            CONTROLLER_AXIS_Y
                        )
                    )

                    # Deadzone
                    if abs(controller_movement.x) < CONTROLLER_DEADZONE:
                        controller_movement.x = 0

                    if abs(controller_movement.y) < CONTROLLER_DEADZONE:
                        controller_movement.y = 0

            except Exception:

                controller_movement.update(
                    0,
                    0
                )

        # Controller has priority if stick is moving
        if controller_movement.length_squared() > 0:

            self.last_input_device = "controller"

            if controller_movement.length_squared() > 1:

                controller_movement.scale_to_length(1)

            return controller_movement

        # Keyboard
        if keyboard_movement.length_squared() > 0:

            self.last_input_device = "keyboard"

            if keyboard_movement.length_squared() > 1:

                keyboard_movement.scale_to_length(1)

            return keyboard_movement

        return pygame.Vector2(
            0,
            0
        )


    # ========================================================
    # PRESSED
    # ========================================================

    def attack_pressed(self):

        return (
            self.current_attack
            and not self.previous_attack
        )


    def dodge_pressed(self):

        return (
            self.current_dodge
            and not self.previous_dodge
        )


    def interact_pressed(self):

        return (
            self.current_interact
            and not self.previous_interact
        )


    def pause_pressed(self):

        return (
            self.current_pause
            and not self.previous_pause
        )


    # ========================================================
    # HELD
    # ========================================================

    def attack_held(self):

        return self.current_attack


    def dodge_held(self):

        return self.current_dodge


    # ========================================================
    # PROMPTS
    # ========================================================

    def get_attack_prompt(self):

        if self.last_input_device == "controller":
            return "X / □  Attack"

        return "SPACE  Attack"


    def get_dodge_prompt(self):

        if self.last_input_device == "controller":
            return "B / ○  Dodge"

        return "SHIFT  Dodge"


    def get_interact_prompt(self):

        if self.last_input_device == "controller":
            return "A / ✕  Interact"

        return "E  Interact"


    def get_pause_prompt(self):

        if self.last_input_device == "controller":
            return "START  Pause"

        return "ESC  Pause"


# ============================================================
# GLOBAL INPUT INSTANCE
# ============================================================

INPUT = InputManager()