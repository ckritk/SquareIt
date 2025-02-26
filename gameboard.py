import pygame
import sys
from gameai import *

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 10
GRID_SPACING = SCREEN_WIDTH // (GRID_SIZE + 1)
POINT_RADIUS = 6
BACKGROUND_COLOR = (50, 50, 50)
GRID_COLOR = (200, 200, 200)
PLAYER1_COLOR = (255, 127, 0)  # for HUMAN (orange)
PLAYER2_COLOR = (0, 255, 255)    # for CPU (cyan)
LINE_WIDTH = 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Square It")

font = pygame.font.SysFont(None, 24)

dot_status = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = -1
square_vertices = []
animation_progress = 0
square_color = None

TOP_GAP = 70  
GRID_OFFSET = 20  

def blend_color(color, background, alpha):
    """ Manually blend a color with a background given an alpha. """
    return (
        int(color[0] * alpha + background[0] * (1 - alpha)),
        int(color[1] * alpha + background[1] * (1 - alpha)),
        int(color[2] * alpha + background[2] * (1 - alpha))
    )

def draw_legend(human_transparent=False, cpu_transparent=True):
    legend_y_pos = TOP_GAP // 2

    transparency_level = 0.3  
    bg_color = BACKGROUND_COLOR

    human_color = blend_color(PLAYER2_COLOR, bg_color, transparency_level) if human_transparent else PLAYER2_COLOR
    cpu_color = blend_color(PLAYER1_COLOR, bg_color, transparency_level) if cpu_transparent else PLAYER1_COLOR

    human_text = font.render("HUMAN", True, human_color)
    human_rect = human_text.get_rect(center=(SCREEN_WIDTH // 3, legend_y_pos))
    human_dot_pos = (human_rect.left - 10, human_rect.centery)

    screen.blit(human_text, human_rect)
    pygame.draw.circle(screen, human_color, human_dot_pos, POINT_RADIUS)

    cpu_text = font.render("CPU", True, cpu_color)
    cpu_rect = cpu_text.get_rect(center=(2 * SCREEN_WIDTH // 3, legend_y_pos))
    cpu_dot_pos = (cpu_rect.left - 10, cpu_rect.centery)

    screen.blit(cpu_text, cpu_rect)
    pygame.draw.circle(screen, cpu_color, cpu_dot_pos, POINT_RADIUS)




def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = (col + 1) * GRID_SPACING
            y = (row+1) * GRID_SPACING + GRID_OFFSET
            if row < GRID_SIZE - 1:
                pygame.draw.line(screen, GRID_COLOR, (x, y), (x, y + GRID_SPACING), 1)
            if col < GRID_SIZE - 1:
                pygame.draw.line(screen, GRID_COLOR, (x, y), (x + GRID_SPACING, y), 1)


def find_square_with_vertex(dot_status, vertex, player):
    global square_vertices, square_color
    rows = len(dot_status)
    cols = len(dot_status[0])

    def is_in_grid(x, y):
        return 0 <= x < rows and 0 <= y < cols and dot_status[x][y] == player

    x1, y1 = vertex

    for x2 in range(rows):
        for y2 in range(cols):
            if (x1, y1) == (x2, y2) or dot_status[x2][y2] != player:
                continue

            dx = x2 - x1
            dy = y2 - y1

            x3, y3 = x2 - dy, y2 + dx
            x4, y4 = x1 - dy, y1 + dx

            if is_in_grid(x3, y3) and is_in_grid(x4, y4):
                square_vertices = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                square_color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR
                return True

            x3, y3 = x2 + dy, y2 - dx
            x4, y4 = x1 + dy, y1 - dx

            if is_in_grid(x3, y3) and is_in_grid(x4, y4):
                square_vertices = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                square_color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR
                return True

    return False


def draw_dots():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = (col + 1) * GRID_SPACING
            y = (row + 1) * GRID_SPACING + GRID_OFFSET  # Add TOP_GAP to Y-coordinate
            if dot_status[row][col] == 1:
                pygame.draw.circle(screen, PLAYER1_COLOR, (x, y), POINT_RADIUS)
            elif dot_status[row][col] == -1:
                pygame.draw.circle(screen, PLAYER2_COLOR, (x, y), POINT_RADIUS)

def animate_square_edges():
    global animation_progress
    if square_vertices:
        points = [(col * GRID_SPACING + GRID_SPACING, row * GRID_SPACING + GRID_SPACING + GRID_OFFSET) for row, col in square_vertices]
        midpoints = [
            ((points[0][0] + points[1][0]) // 2, (points[0][1] + points[1][1]) // 2),
            ((points[1][0] + points[2][0]) // 2, (points[1][1] + points[2][1]) // 2),
            ((points[2][0] + points[3][0]) // 2, (points[2][1] + points[3][1]) // 2),
            ((points[3][0] + points[0][0]) // 2, (points[3][1] + points[0][1]) // 2)
        ]
        for i in range(4):
            start = midpoints[i]
            end1 = points[i]
            end2 = points[(i + 1) % 4]
            current_end1 = (
                int(start[0] + (end1[0] - start[0]) * animation_progress),
                int(start[1] + (end1[1] - start[1]) * animation_progress)
            )
            current_end2 = (
                int(start[0] + (end2[0] - start[0]) * animation_progress),
                int(start[1] + (end2[1] - start[1]) * animation_progress)
            )
            pygame.draw.line(screen, square_color, current_end1, current_end2, LINE_WIDTH)
        animation_progress += 0.001
        if animation_progress >= 1.0:
            animation_progress = 1.0

def get_clicked_dot(mouse_pos):
    mouse_x, mouse_y = mouse_pos
    adjusted_mouse_y = mouse_y - GRID_OFFSET  # Adjust the mouse y-coordinate to account for TOP_GAP

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = (col + 1) * GRID_SPACING
            y = (row + 1) * GRID_SPACING
            if (x - mouse_x) ** 2 + (y - adjusted_mouse_y) ** 2 <= POINT_RADIUS ** 2:
                return (row, col)
    return None

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not square_vertices:
            draw_legend(human_transparent=True, cpu_transparent=False)
            clicked_dot = get_clicked_dot(event.pos)
            if clicked_dot:
                row, col = clicked_dot
                if dot_status[row][col] == 0:
                    dot_status = make_move(dot_status, (row, col), False, True)
                    print(f"Player clicked dot at: {clicked_dot}")
                    draw_dots()
                    pygame.display.update()
                    if find_square_with_vertex(dot_status, clicked_dot, -1):
                        print("Player 1 wins!")
                        break

                    x = sq.find_3pt_square_zeros(dot_status, 1)
                    if len(x) == 0:
                        x = sq.find_3pt_square_zeros(dot_status, -1)
                        if len(x) == 0:
                            best_move = find_best_move(dot_status, DEPTH, True)
                        else:
                            print(x)
                            best_move = x[0]
                    else:
                        print(x)
                        best_move = x[0]
                    

                    if best_move:
                        dot_status = make_move(dot_status, best_move, True, True)
                        draw_dots()
                        pygame.display.update()
                        print(f"AI plays: {best_move}")
                        draw_legend(cpu_transparent=True)
                        if find_square_with_vertex(dot_status, best_move, 1):
                            print("AI wins!")

    screen.fill(BACKGROUND_COLOR)
    draw_legend()  
    draw_grid()
    draw_dots()
    if square_vertices:
        animate_square_edges()
    pygame.display.flip()
