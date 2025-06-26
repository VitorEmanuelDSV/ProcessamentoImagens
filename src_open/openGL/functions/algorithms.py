from .primitives import draw_pixel

def draw_line(x0, y0, x1, y1, color=(1.0, 1.0, 1.0)):
    x0 = int(round(x0))
    y0 = int(round(y0))
    x1 = int(round(x1))
    y1 = int(round(y1))
    """Algoritmo de Bresenham para desenhar linha."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        draw_pixel(x0, y0, color)

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_line_3d(x0, y0, z0, x1, y1, z1, color=(1.0, 1.0, 1.0)):
    """Algoritmo de Bresenham adaptado para 3D."""

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    dz = abs(z1 - z0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    sz = 1 if z0 < z1 else -1

    if dx >= dy and dx >= dz:  # x dominante
        err_y = dx / 2
        err_z = dx / 2
        while x0 != x1:
            draw_pixel(x0, y0, z0, color)
            err_y -= dy
            err_z -= dz
            if err_y < 0:
                y0 += sy
                err_y += dx
            if err_z < 0:
                z0 += sz
                err_z += dx
            x0 += sx
    elif dy >= dx and dy >= dz:  # y dominante
        err_x = dy / 2
        err_z = dy / 2
        while y0 != y1:
            draw_pixel(x0, y0, z0, color)
            err_x -= dx
            err_z -= dz
            if err_x < 0:
                x0 += sx
                err_x += dy
            if err_z < 0:
                z0 += sz
                err_z += dy
            y0 += sy
    else:  # z dominante
        err_x = dz / 2
        err_y = dz / 2
        while z0 != z1:
            draw_pixel(x0, y0, z0, color)
            err_x -= dx
            err_y -= dy
            if err_x < 0:
                x0 += sx
                err_x += dz
            if err_y < 0:
                y0 += sy
                err_y += dz
            z0 += sz

    draw_pixel(x1, y1, z1, color)  # desenhar o último pixel
