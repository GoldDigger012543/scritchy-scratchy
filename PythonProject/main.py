import pygame
import sys
from random import randint

pygame.init()

# Настройки окна
WIDTH = 1100
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lottery Game")

clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

GRAY = (120, 120, 120)
DARK_GRAY = (45, 45, 45)

GREEN = (60, 200, 100)
BLUE = (60, 130, 255)
GOLD = (255, 190, 40)

TICKET_COLOR = (245, 220, 150)

# Фон
background = pygame.image.load(
    "background.png"
).convert()

background = pygame.transform.scale(
    background,
    (WIDTH, HEIGHT)
)

# Спрайты
coin_image = pygame.image.load(
    "coin.png"
).convert_alpha()

money_image = pygame.image.load(
    "money.png"
).convert_alpha()

bag_image = pygame.image.load(
    "bagofgold.png"
).convert_alpha()

# Шрифты
font_small = pygame.font.Font(None, 26)
font = pygame.font.Font(None, 32)
font_big = pygame.font.Font(None, 48)
font_huge = pygame.font.Font(None, 70)

# Начальные значения игрока
level = 0
xp = 0
money = 0


# Система опыта
def xp_for_next_level():
    return int(100 * (1.3 ** level))


def add_xp(amount):
    global xp
    global level

    xp += amount

    while xp >= xp_for_next_level():
        xp -= xp_for_next_level()
        level += 1


# Класс тикета
class Widget(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        required_level
    ):

        super().__init__()

        self.width = width
        self.height = height
        self.text = text
        self.required_level = required_level

        self.image = pygame.Surface(
            (width, height)
        )

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.update_image()


    def update_image(self):

        if level >= self.required_level:

            self.image.fill(
                (35, 35, 35)
            )

            pygame.draw.rect(
                self.image,
                BLUE,
                self.image.get_rect(),
                3
            )

            text_image = font.render(
                self.text,
                True,
                WHITE
            )

        else:

            self.image.fill(
                (25, 25, 25)
            )

            pygame.draw.rect(
                self.image,
                DARK_GRAY,
                self.image.get_rect(),
                3
            )

            text_image = font.render(
                f"{self.text} | LVL {self.required_level}",
                True,
                GRAY
            )

        text_rect = text_image.get_rect(
            center=self.image.get_rect().center
        )

        self.image.blit(
            text_image,
            text_rect
        )


# Создание тикетов
widgets = pygame.sprite.Group()

ticket1 = Widget(
    220,
    100,
    250,
    70,
    "Ticket 1",
    0
)

ticket2 = Widget(
    220,
    190,
    250,
    70,
    "Ticket 2",
    5
)

widgets.add(ticket1)
widgets.add(ticket2)

# Состояние билета
ticket_open = False
current_ticket = None

# Слоты
slots = [
    None,
    None,
    None
]

opened_slots = [
    False,
    False,
    False
]

# Награда
win_money = 0
win_xp = 0

result_checked = False


# Случайное выпадение символа
def roll_symbol(ticket):

    number = randint(1, 100)

    if ticket == ticket1:

        if number <= 70:
            return "coin"

        elif number <= 95:
            return "money"

        else:
            return "bag"

    elif ticket == ticket2:

        if number <= 40:
            return "coin"

        elif number <= 85:
            return "money"

        else:
            return "bag"


# Получение изображения символа
def get_symbol_image(symbol):

    if symbol == "coin":
        return coin_image

    elif symbol == "money":
        return money_image

    elif symbol == "bag":
        return bag_image

    return None


# Проверка комбинации и определение награды
def calculate_reward():

    if slots[0] == slots[1] == slots[2]:

        if slots[0] == "coin":
            return 30, 100

        elif slots[0] == "money":
            return 150, 150

        elif slots[0] == "bag":
            return 750, 300

    if slots[0] == slots[1]:

        if slots[0] == "coin":
            return 10, 25

        elif slots[0] == "money":
            return 50, 50

        elif slots[0] == "bag":
            return 250, 100

    if slots[1] == slots[2]:

        if slots[1] == "coin":
            return 10, 25

        elif slots[1] == "money":
            return 50, 50

        elif slots[1] == "bag":
            return 250, 100

    return 0, 10


# Открытие билета
def open_ticket(ticket):

    global ticket_open
    global current_ticket
    global slots
    global opened_slots
    global win_money
    global win_xp
    global result_checked

    if level < ticket.required_level:
        return

    current_ticket = ticket

    slots = [
        None,
        None,
        None
    ]

    opened_slots = [
        False,
        False,
        False
    ]

    win_money = 0
    win_xp = 0

    result_checked = False

    ticket_open = True


# Открытие отдельного слота
def open_slot(slot_number):

    global slots
    global opened_slots
    global win_money
    global win_xp
    global money
    global result_checked

    if opened_slots[slot_number]:
        return

    slots[slot_number] = roll_symbol(current_ticket)

    opened_slots[slot_number] = True

    if all(opened_slots):

        win_money, win_xp = calculate_reward()

        money += win_money

        add_xp(win_xp)

        result_checked = True


# Отрисовка закрытого слота
def draw_closed_slot(rect):

    pygame.draw.rect(
        screen,
        DARK_GRAY,
        rect,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        BLACK,
        rect,
        4,
        border_radius=10
    )

    question = font_huge.render(
        "?",
        True,
        WHITE
    )

    question_rect = question.get_rect(
        center=rect.center
    )

    screen.blit(
        question,
        question_rect
    )


# Отрисовка открытого слота
def draw_open_slot(rect, symbol):

    pygame.draw.rect(
        screen,
        WHITE,
        rect,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        BLACK,
        rect,
        4,
        border_radius=10
    )

    image = get_symbol_image(symbol)

    if image is not None:

        image_rect = image.get_rect(
            center=rect.center
        )

        screen.blit(
            image,
            image_rect
        )


# Отрисовка билета
def draw_lottery_ticket():

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 180)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    ticket_rect = pygame.Rect(
        300,
        70,
        650,
        500
    )

    pygame.draw.rect(
        screen,
        TICKET_COLOR,
        ticket_rect,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        GOLD,
        ticket_rect,
        5,
        border_radius=20
    )

    title = font_huge.render(
        "LOTTERY",
        True,
        BLACK
    )

    title_rect = title.get_rect(
        center=(WIDTH // 2, 130)
    )

    screen.blit(
        title,
        title_rect
    )

    ticket_name = font.render(
        current_ticket.text,
        True,
        BLACK
    )

    screen.blit(
        ticket_name,
        (340, 175)
    )

    slot_size = 120
    slot_y = 230

    slot_x_positions = [
        365,
        490,
        615
    ]

    for i in range(3):

        rect = pygame.Rect(
            slot_x_positions[i],
            slot_y,
            slot_size,
            slot_size
        )

        if not opened_slots[i]:
            draw_closed_slot(rect)

        else:
            draw_open_slot(
                rect,
                slots[i]
            )

    if not result_checked:

        hint = font.render(
            "Нажмите на каждый слот",
            True,
            BLACK
        )

        hint_rect = hint.get_rect(
            center=(WIDTH // 2, 390)
        )

        screen.blit(
            hint,
            hint_rect
        )

    if result_checked:

        if win_money > 0:

            reward_text = font_big.render(
                f"+{win_money} MONEY",
                True,
                GREEN
            )

        else:

            reward_text = font_big.render(
                "NO MATCH",
                True,
                GRAY
            )

        reward_rect = reward_text.get_rect(
            center=(WIDTH // 2, 395)
        )

        screen.blit(
            reward_text,
            reward_rect
        )

        xp_text = font.render(
            f"+{win_xp} XP",
            True,
            BLUE
        )

        xp_rect = xp_text.get_rect(
            center=(WIDTH // 2, 440)
        )

        screen.blit(
            xp_text,
            xp_rect
        )

    close_text = font_small.render(
        "ESC - закрыть билет",
        True,
        BLACK
    )

    close_rect = close_text.get_rect(
        center=(WIDTH // 2, 520)
    )

    screen.blit(
        close_text,
        close_rect
    )


# Панель игрока
def draw_level_panel():

    panel = pygame.Rect(
        10,
        10,
        180,
        630
    )

    pygame.draw.rect(
        screen,
        (30, 30, 30),
        panel,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        BLUE,
        panel,
        2,
        border_radius=10
    )

    level_text = font_big.render(
        f"LEVEL {level}",
        True,
        WHITE
    )

    screen.blit(
        level_text,
        (30, 35)
    )

    money_text = font_big.render(
        f"$ {money}",
        True,
        GOLD
    )

    screen.blit(
        money_text,
        (30, 90)
    )

    required_xp = xp_for_next_level()

    xp_text = font.render(
        f"XP: {xp}/{required_xp}",
        True,
        WHITE
    )

    screen.blit(
        xp_text,
        (30, 150)
    )

    bar_x = 30
    bar_y = 190

    bar_width = 140
    bar_height = 20

    pygame.draw.rect(
        screen,
        DARK_GRAY,
        (
            bar_x,
            bar_y,
            bar_width,
            bar_height
        )
    )

    progress = xp / required_xp

    pygame.draw.rect(
        screen,
        GREEN,
        (
            bar_x,
            bar_y,
            int(bar_width * progress),
            bar_height
        )
    )

    tickets_text = font.render(
        "Tickets:",
        True,
        WHITE
    )

    screen.blit(
        tickets_text,
        (30, 250)
    )

    if level >= 0:

        color = GREEN
        text = "Ticket 1"

    else:

        color = GRAY
        text = "Ticket 1"

    ticket_text = font_small.render(
        text,
        True,
        color
    )

    screen.blit(
        ticket_text,
        (30, 290)
    )

    if level >= 5:

        color = GREEN
        text = "Ticket 2"

    else:

        color = GRAY
        text = "Ticket 2 | LVL 5"

    ticket_text = font_small.render(
        text,
        True,
        color
    )

    screen.blit(
        ticket_text,
        (30, 330)
    )


# Главный игровой цикл
running = True

while running:

    # Обработка событий
    for event in pygame.event.get():

        # Закрытие игры
        if event.type == pygame.QUIT:

            running = False

        # Управление мышью
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = event.pos

            # Если билет не открыт
            if not ticket_open:

                for widget in widgets:

                    if widget.rect.collidepoint(
                        mouse_pos
                    ):

                        open_ticket(widget)

            # Если билет открыт
            else:

                slot_rects = [

                    pygame.Rect(
                        365,
                        230,
                        120,
                        120
                    ),

                    pygame.Rect(
                        490,
                        230,
                        120,
                        120
                    ),

                    pygame.Rect(
                        615,
                        230,
                        120,
                        120
                    )

                ]

                # Проверка нажатия на слоты
                for i in range(3):

                    if slot_rects[i].collidepoint(
                        mouse_pos
                    ):

                        open_slot(i)

        # Управление клавиатурой
        if event.type == pygame.KEYDOWN:

            # Закрытие билета клавишей ESC
            if event.key == pygame.K_ESCAPE:

                ticket_open = False

    # Обновление тикетов
    for widget in widgets:

        widget.update_image()

    # Отрисовка экрана
    screen.blit(
        background,
        (0, 0)
    )

    draw_level_panel()

    widgets.draw(screen)

    if ticket_open:

        draw_lottery_ticket()

    pygame.display.flip()

    clock.tick(60)

# Завершение игры
pygame.quit()

sys.exit()