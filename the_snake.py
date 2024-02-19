from random import randint

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_START = 20


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Это базовый класс, от него наследуются другие объекты."""

    def __init__(self, bg_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = bg_color

    def draw(self):
        """Метод определяет, как будет отрисовываться объект."""
        pass

    def draw_1(self, surface, position):
        """Метод определяет, как будет отрисовываться объект."""
        rect = pygame.Rect(
            position,
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для яблока"""

    def __init__(self, bg_color=APPLE_COLOR):
        super().__init__(bg_color)
        self.randomize_position()

    def randomize_position(self):
        """Задает случайную координату"""
        while True:
            x_position = randint(SCREEN_START, SCREEN_WIDTH - GRID_SIZE)
            y_position = randint(SCREEN_START, SCREEN_HEIGHT - GRID_SIZE)
            if x_position % 20 == 0 and y_position % 20 == 0:
                self.position = (x_position, y_position)
                break

    def draw(self, surface):
        """Метод определяет, как будет отрисовываться объект."""
        self.draw_1(surface, self.position)


class Snake(GameObject):
    """Класс для змеи."""

    def __init__(self, bg_color=SNAKE_COLOR):
        super().__init__(bg_color)
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_1, head_2 = self.get_head_position()
        direction_1, direction_2 = self.direction
        title_1 = (head_1 + direction_1 * GRID_SIZE) % SCREEN_WIDTH
        title_2 = (head_2 + direction_2 * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (title_1, title_2))

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Метод определяет, как будет отрисовываться объект."""
        for position in self.positions[:-1]:
            self.draw_1(surface, position)
        self.draw_1(surface, self.positions[0])
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT


def handle_keys(game_object):
    """Обрабатывает события клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл"""
    apple = Apple()
    snake = Snake()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw(screen)
        snake.draw(screen)

        if snake.positions == apple.position:
            apple.randomize_position()

        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.length += 1

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
