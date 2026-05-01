import random
import sys

import pygame


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
FPS = 10

BACKGROUND_COLOR = (15, 15, 15)
SNAKE_COLOR = (50, 200, 50)
FOOD_COLOR = (220, 60, 60)
TEXT_COLOR = (230, 230, 230)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def random_food_position(snake):
    """Return a random grid position that does not overlap snake."""
    cols = WINDOW_WIDTH // GRID_SIZE
    rows = WINDOW_HEIGHT // GRID_SIZE

    while True:
        position = (random.randint(0, cols - 1), random.randint(0, rows - 1))
        if position not in snake:
            return position


def reset_game():
    """Create and return a fresh game state."""
    center = (WINDOW_WIDTH // GRID_SIZE // 2, WINDOW_HEIGHT // GRID_SIZE // 2)
    snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
    direction = RIGHT
    food = random_food_position(snake)
    score = 0
    return snake, direction, food, score


def is_reverse(current_direction, new_direction):
    """Prevent direct reversal to avoid instant self-collision by input."""
    return (
        current_direction[0] + new_direction[0] == 0
        and current_direction[1] + new_direction[1] == 0
    )


def draw_cell(surface, color, grid_position):
    x = grid_position[0] * GRID_SIZE
    y = grid_position[1] * GRID_SIZE
    rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)
    large_font = pygame.font.SysFont(None, 42)

    snake, direction, food, score = reset_game()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if game_over:
                    if event.key == pygame.K_r:
                        snake, direction, food, score = reset_game()
                        game_over = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    continue

                if event.key in (pygame.K_UP, pygame.K_w):
                    new_direction = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    new_direction = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    new_direction = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    new_direction = RIGHT
                else:
                    new_direction = direction

                if not is_reverse(direction, new_direction):
                    direction = new_direction

        if not game_over:
            head_x, head_y = snake[0]
            next_head = (head_x + direction[0], head_y + direction[1])

            cols = WINDOW_WIDTH // GRID_SIZE
            rows = WINDOW_HEIGHT // GRID_SIZE

            # Collision with wall or snake body ends the run.
            if (
                next_head[0] < 0
                or next_head[0] >= cols
                or next_head[1] < 0
                or next_head[1] >= rows
                or next_head in snake
            ):
                game_over = True
            else:
                snake.insert(0, next_head)
                if next_head == food:
                    score += 1
                    food = random_food_position(snake)
                else:
                    snake.pop()

        screen.fill(BACKGROUND_COLOR)

        for segment in snake:
            draw_cell(screen, SNAKE_COLOR, segment)
        draw_cell(screen, FOOD_COLOR, food)

        score_surface = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_surface, (10, 10))

        if game_over:
            message = large_font.render("Game Over", True, TEXT_COLOR)
            sub_message = font.render("Press R to restart, Q to quit", True, TEXT_COLOR)
            message_rect = message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            sub_rect = sub_message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            screen.blit(message, message_rect)
            screen.blit(sub_message, sub_rect)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
