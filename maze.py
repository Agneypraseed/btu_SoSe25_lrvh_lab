import pygame

GRID_SIZE = 8
TILE_SIZE = 60
WIDTH, HEIGHT = GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE + 90
MAZE = [
    [0, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 2],
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 50, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
FPS = 30

agent_pos = [0, 0]
score = 0


def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE,
                               TILE_SIZE, TILE_SIZE)
            # Fill cell background
            if MAZE[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)  # Wall
            elif MAZE[y][x] == 2:
                pygame.draw.rect(screen, GREEN, rect)  # Goal
            else:
                pygame.draw.rect(screen, WHITE, rect)  # Path

            # Draw grid lines on all cells
            pygame.draw.rect(screen, GRAY, rect, 2)

    agent_rect = pygame.Rect(
        agent_pos[0] * TILE_SIZE + 10, agent_pos[1] * TILE_SIZE + 10, TILE_SIZE - 20, TILE_SIZE - 20)
    pygame.draw.rect(screen, BLUE, agent_rect)  # Agent

    score_text = font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect()
    score_rect.center = (WIDTH // 2, HEIGHT - 45)  # Position in the extra space below maze
    screen.blit(score_text, score_rect)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            dx, dy = 0, 0
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_UP:
                dy = -1
            elif event.key == pygame.K_DOWN:
                dy = 1    

            if dx != 0 or dy != 0:
                new_x = agent_pos[0] + dx
                new_y = agent_pos[1] + dy

                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    if MAZE[new_y][new_x] != 1:
                        agent_pos[0] = new_x
                        agent_pos[1] = new_y

                        if MAZE[new_y][new_x] == 2:
                            score += 1
                            print(f"Score: {score}")
                            # Reset agent position to start
                            agent_pos = [0, 0]

    screen.fill(WHITE)
    draw_grid()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
