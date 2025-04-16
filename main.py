import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Параметры камеры
d = 5  # Расстояние до экрана
scale = 100
angle_x, angle_y, angle_z = 0, 0, 0
scale_step = 1.1

# Параметры функции
a, b = 0.5, 0.5 
u_values = [i * 0.1 for i in range(0, int(4 * math.pi / 0.1) + 1)]
v_values = [i * 0.1 for i in range(-20, 21)]

def project(x, y, z):
    factor = d / (d + z)
    x_2d = int(WIDTH / 2 + x * factor * scale)
    y_2d = int(HEIGHT / 2 - y * factor * scale)
    return x_2d, y_2d

def rotate(x, y, z, angle_x, angle_y, angle_z):
    rad_x, rad_y, rad_z = math.radians(angle_x), math.radians(angle_y), math.radians(angle_z)
    cos_x, sin_x = math.cos(rad_x), math.sin(rad_x)
    cos_y, sin_y = math.cos(rad_y), math.sin(rad_y)
    cos_z, sin_z = math.cos(rad_z), math.sin(rad_z)

    # Вращение вокруг X
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    # Вращение вокруг Y
    x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y
    # Вращение вокруг Z
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

    return x, y, z

def func(u, v):
    x = a * u * math.cos(u)
    y = b * u * math.sin(u)
    z = v
    return x, y, z

grid = []
cells = []
steps = 4 
needs_update = True

running = True
mouse_dragging = False
prev_mouse_pos = (0, 0)

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                scale *= scale_step
                needs_update = True
            elif event.key == pygame.K_DOWN:
                scale /= scale_step
                needs_update = True
            elif event.key == pygame.K_RIGHT:
                a += 0.1
                needs_update = True
            elif event.key == pygame.K_LEFT:
                a -= 0.1
                needs_update = True
            elif event.key == pygame.K_q:
                angle_z += 5
                needs_update = True
            elif event.key == pygame.K_e:
                angle_z -= 5
                needs_update = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_dragging = True
                prev_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_dragging:
                dx, dy = event.pos[0] - prev_mouse_pos[0], event.pos[1] - prev_mouse_pos[1]
                angle_x += dy * 0.5
                angle_y += dx * 0.5
                prev_mouse_pos = event.pos
                needs_update = True

    if needs_update:
        grid = []
        for u in u_values:
            row = []
            for v in v_values:
                x, y, z = func(u, v)
                x, y, z = rotate(x, y, z, angle_x, angle_y, angle_z)
                row.append((x, y, z))
            grid.append(row)

        cells = []
        for i in range(len(grid) - 1):
            for j in range(len(grid[i]) - 1):
                p1 = grid[i][j]
                p2 = grid[i][j + 1]
                p3 = grid[i + 1][j + 1]
                p4 = grid[i + 1][j]
                avg_z = (p1[2] + p2[2] + p3[2] + p4[2]) / 4
                cells.append((avg_z, (p1, p2, p3, p4)))

        cells.sort(reverse=True)
        needs_update = False

    # Рисуем заливку
    for avg_z, (p1, p2, p3, p4) in cells:
        brightness = max(50, min(255, int(255 - (avg_z * 60))))
        color = (0, brightness, 0)

        for k in range(steps + 1):
            t = k / steps

            # Горизонтальная линия
            lx = p1[0] * (1 - t) + p4[0] * t
            ly = p1[1] * (1 - t) + p4[1] * t
            lz = p1[2] * (1 - t) + p4[2] * t

            rx = p2[0] * (1 - t) + p3[0] * t
            ry = p2[1] * (1 - t) + p3[1] * t
            rz = p2[2] * (1 - t) + p3[2] * t

            pygame.draw.line(screen, color, project(lx, ly, lz), project(rx, ry, rz))

            # Вертикальная линия
            tx = p1[0] * (1 - t) + p2[0] * t
            ty = p1[1] * (1 - t) + p2[1] * t
            tz = p1[2] * (1 - t) + p2[2] * t

            bx = p4[0] * (1 - t) + p3[0] * t
            by = p4[1] * (1 - t) + p3[1] * t
            bz = p4[2] * (1 - t) + p3[2] * t

            pygame.draw.line(screen, color, project(tx, ty, tz), project(bx, by, bz))


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
