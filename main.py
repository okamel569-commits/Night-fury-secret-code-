import pygame
import random

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
W, H = screen.get_size()
pygame.display.set_caption("NIGHT FURY - SECRET CODE")

clock = pygame.time.Clock()

BG = (12, 14, 26)
WHITE = (245, 245, 255)
PURPLE = (145, 80, 240)
BLUE = (55, 115, 220)
GREEN = (35, 180, 110)
RED = (215, 65, 75)
GRAY = (150, 155, 175)

font = pygame.font.Font(None, max(28, int(H * 0.035)))
small = pygame.font.Font(None, max(22, int(H * 0.027)))
big = pygame.font.Font(None, max(48, int(H * 0.065)))

state = "MENU"
difficulty = "EASY"
max_tries = 15
tries = 15
secret = ""
guess = ""
history = []
message = "Choose your difficulty"


def draw_text(value, f, color, x, y):
    image = f.render(str(value), True, color)
    rect = image.get_rect(center=(int(x), int(y)))
    screen.blit(image, rect)


def make_button(rect, label, color):
    pygame.draw.rect(screen, color, rect, border_radius=14)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=14)
    draw_text(label, font, WHITE, rect.centerx, rect.centery)


def start_game(level):
    global state, difficulty, max_tries, tries
    global secret, guess, history, message

    difficulty = level
    max_tries = {
        "EASY": 15,
        "MEDIUM": 10,
        "HARD": 6
    }[level]

    tries = max_tries
    secret = "".join(random.sample("0123456789", 4))
    guess = ""
    history = []
    message = "Enter 4 different digits"
    state = "GAME"


def draw_menu():
    screen.fill(BG)

    draw_text("NIGHT FURY", big, PURPLE, W // 2, H * 0.15)
    draw_text("SECRET CODE", font, WHITE, W // 2, H * 0.22)
    draw_text("SELECT DIFFICULTY", font, WHITE, W // 2, H * 0.36)

    width = int(W * 0.72)
    height = max(58, int(H * 0.085))
    x = (W - width) // 2
    gap = max(14, int(H * 0.02))

    buttons = []

    labels = [
        ("EASY", GREEN),
        ("MEDIUM", BLUE),
        ("HARD", RED)
    ]

    total_height = 3 * height + 2 * gap
    start_y = (H - total_height) // 2 + int(H * 0.08)

    for i, (label, color) in enumerate(labels):
        rect = pygame.Rect(
            x,
            start_y + i * (height + gap),
            width,
            height
        )
        make_button(rect, label, color)
        buttons.append((rect, label))

    return buttons


def draw_game():
    screen.fill(BG)

    # Keyboard dimensions are calculated first
    gap = max(7, int(W * 0.018))
    bw = (W - 4 * gap) // 3
    bh = max(48, min(int(H * 0.075), int(W * 0.19)))

    keyboard_height = 4 * bh + 5 * gap
    keyboard_top = H - keyboard_height

    # Header
    draw_text("NIGHT FURY", big, PURPLE, W // 2, H * 0.045)
    draw_text("SECRET CODE", small, WHITE, W // 2, H * 0.105)

    # Attempts
    draw_text(
        difficulty + " | Attempts: " + str(tries) + "/" + str(max_tries),
        font, WHITE, W // 2, keyboard_top * 0.20
    )

    # Number entry
    draw_text(
        "YOUR GUESS",
        small, GRAY, W // 2, keyboard_top * 0.29
    )

    shown = guess + "_" * (4 - len(guess))

    draw_text(
        shown,
        big, GREEN, W // 2, keyboard_top * 0.36
    )

    # Message
    draw_text(
        message,
        small, WHITE, W // 2, keyboard_top * 0.45
    )

    # Score and history are clearly below the number
    draw_text(
        "SCORE / HISTORY",
        small, PURPLE, W // 2, keyboard_top * 0.55
    )

    history_start = keyboard_top * 0.63
    history_gap = keyboard_top * 0.105

    for i, item in enumerate(history[-3:]):
        draw_text(
            item,
            small,
            WHITE,
            W // 2,
            history_start + i * history_gap
        )

    # Large touchscreen keyboard
    buttons = []

    for number in range(1, 10):
        row = (number - 1) // 3
        col = (number - 1) % 3

        rect = pygame.Rect(
            gap + col * (bw + gap),
            keyboard_top + gap + row * (bh + gap),
            bw,
            bh
        )

        make_button(rect, str(number), BLUE)
        buttons.append((rect, str(number)))

    bottom_y = keyboard_top + gap + 3 * (bh + gap)

    rect_zero = pygame.Rect(gap, bottom_y, bw, bh)
    rect_clear = pygame.Rect(2 * gap + bw, bottom_y, bw, bh)
    rect_enter = pygame.Rect(3 * gap + 2 * bw, bottom_y, bw, bh)

    make_button(rect_zero, "0", BLUE)
    make_button(rect_clear, "CLEAR", RED)
    make_button(rect_enter, "ENTER", GREEN)

    buttons.append((rect_zero, "0"))
    buttons.append((rect_clear, "CLEAR"))
    buttons.append((rect_enter, "ENTER"))

    return buttons


def draw_result():
    screen.fill(BG)

    if state == "WIN":
        title = "YOU WIN!"
        color = GREEN
    else:
        title = "GAME OVER"
        color = RED

    draw_text("NIGHT FURY", big, PURPLE, W // 2, H * 0.25)
    draw_text(title, big, color, W // 2, H * 0.48)
    draw_text("Secret code: " + secret, font, WHITE, W // 2, H * 0.56)

    width = int(W * 0.75)
    height = max(58, int(H * 0.09))
    x = (W - width) // 2

    again = pygame.Rect(x, int(H * 0.65), width, height)
    menu = pygame.Rect(
        x,
        int(H * 0.65) + height + 20,
        width,
        height
    )

    make_button(again, "PLAY AGAIN", GREEN)
    make_button(menu, "MAIN MENU", BLUE)

    return again, menu


def handle_game_click(pos, buttons):
    global guess, tries, state, message

    for rect, value in buttons:
        if not rect.collidepoint(pos):
            continue

        if value == "CLEAR":
            guess = ""
            message = "Enter 4 different digits"
            return

        if value == "ENTER":
            if len(guess) != 4:
                message = "Enter exactly 4 digits"
                return

            bulls = sum(
                guess[i] == secret[i] for i in range(4)
            )

            cows = sum(
                digit in secret for digit in guess
            ) - bulls

            history.append(
                guess + "  Bulls: " + str(bulls)
                + "  Cows: " + str(cows)
            )

            tries -= 1

            if bulls == 4:
                state = "WIN"

            elif tries <= 0:
                state = "LOSE"

            else:
                guess = ""
                message = "Try again!"

            return

        if len(guess) < 4 and value not in guess:
            guess += value
            message = "Enter 4 different digits"

        return


running = True

while running:

    if state == "MENU":
        menu_buttons = draw_menu()

    elif state == "GAME":
        game_buttons = draw_game()

    elif state in ("WIN", "LOSE"):
        result_buttons = draw_result()

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            pos = event.pos

            if state == "MENU":
                for rect, label in menu_buttons:
                    if rect.collidepoint(pos):
                        start_game(label)
                        break

            elif state == "GAME":
                handle_game_click(pos, game_buttons)

            elif state in ("WIN", "LOSE"):
                again, menu = result_buttons

                if again.collidepoint(pos):
                    start_game(difficulty)

                elif menu.collidepoint(pos):
                    state = "MENU"

    clock.tick(30)

pygame.quit()
