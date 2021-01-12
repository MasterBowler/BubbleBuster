from constants import *
from level import Level
from player import Player
from bubble import Bubble
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Bubble Buster")

#https://www.pygame.org/docs/tut/ChimpLineByLine.html
def load_image(name, colorkey=None):
    fullname = os.path.join('art', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

bubbles = []
for c in COLORS:
    bubbles.append(load_image(c + '.png'))

level = Level()
level.random_level()
player = Player()
bubble_to_shoot = Bubble(SCREEN_WIDTH / 2 - BUBBLE_WIDTH / 2, SCREEN_HEIGHT - BUBBLE_WIDTH, 500, 90, 1, False)

def get_bubble_coordinate(row, column):
    bubble_x = level.x + column * level.bubble_width
    if (row + level.row_offset) % 2:
        bubble_x += level.bubble_width/2
    bubble_y = level.y + row * level.row_height
    return bubble_x, bubble_y

def draw_bubble(bubble_color, x, y):
    if bubble_color >= 0 and bubble_color < len(bubbles):
        window.blit(bubbles[bubble_color],(x,y))
    return

def render_grid(rows, columns):
    for i in range(rows):
        for j in range(columns):
            bubble = level.grid[i][j]
            coordinates = get_bubble_coordinate(i, j)
            draw_bubble(bubble.bubble_color, coordinates[0], coordinates[1])

def get_grid_position(x, y):
    grid_y = math.floor((y - level.y) / level.row_height)
    x_offset = 0
    if (grid_y + level.row_offset) % 2:
        x_offset = level.bubble_width / 2
    grid_x = math.floor(((x - x_offset) - level.x)/ level.bubble_width)
    return grid_x, grid_y

def update_mouse_angle():
    position_x, position_y = pygame.mouse.get_pos()
    mouse_angle = math.degrees(math.atan2((player.y + level.bubble_height / 2) - position_y,
                                                position_x - (player.x + level.bubble_width / 2)))
    if mouse_angle < 0:
        mouse_angle = 180 + (180 + mouse_angle)
    player.angle = mouse_angle
    lower_bound = 8
    upper_bound = 172
    if mouse_angle > 90 and mouse_angle < 270:
        if mouse_angle > upper_bound:
            mouse_angle = upper_bound
    elif mouse_angle < lower_bound or mouse_angle >= 270:
        mouse_angle = lower_bound

def render_mouse_angle():
    center_x = player.x + level.bubble_width / 2
    center_y = player.y + level.bubble_height / 2
    end_x = center_x + 1.5 * level.bubble_width * math.cos(math.radians(player.angle))
    end_y = center_y - 1.5 * level.bubble_height * math.sin(math.radians(player.angle))
    pygame.draw.line(window, (180,160,140), (center_x,center_y), (end_x,end_y), 6)


def place_bubble():
    center_x = bubble_to_shoot.x + level.bubble_width / 2
    center_y = bubble_to_shoot.y + level.bubble_height / 2
    grid_pos = get_grid_position(center_x, center_y)
    level.grid[grid_pos[1]][grid_pos[0]].bubble_color = bubble_to_shoot.bubble_color
    bubble_to_shoot.reinitialize()
    return

def collision_detection(x1, y1, r1, x2, y2, r2):
    dx = x1 - x2
    dy = y1 - y2
    distance = math.sqrt(dx * dx + dy * dy)
    if distance < r1 + r2:
        return True
    return False

def mooving_bubble(delta_time):
    bubble_to_shoot.x += delta_time * bubble_to_shoot.speed * math.cos(math.radians(bubble_to_shoot.angle))
    bubble_to_shoot.y += delta_time * bubble_to_shoot.speed * -1 * math.sin(math.radians(bubble_to_shoot.angle))

    if bubble_to_shoot.x <= level.x:
        bubble_to_shoot.angle = 180 - bubble_to_shoot.angle
        bubble_to_shoot.x = level.x
    elif bubble_to_shoot.x + level.bubble_width >= level.x + level.width:
        bubble_to_shoot.angle = 180 - bubble_to_shoot.angle
        bubble_to_shoot.x = level.x + level.width - level.bubble_width

    if bubble_to_shoot.y <= level.y:
        bubble_to_shoot.y = level.y
        place_bubble()
        return

    for i in range(level.rows):
        for j in range(level.columns):
            bubble = level.grid[i][j]
            if bubble.bubble_color < 0:
               continue

            coordinates_x, coordinates_y = get_bubble_coordinate(i,j)
            if collision_detection (bubble_to_shoot.x + level.bubble_width / 2,
                                    bubble_to_shoot.y + level.bubble_height / 2,
                                    level.radius,
                                    coordinates_x + level.bubble_width / 2,
                                    coordinates_y + level.bubble_height / 2,
                                    level.radius):
                bubble_to_shoot.moving = False
                place_bubble()
                return

def main():

    clock = pygame.time.Clock()
    run = True
    while run:
        milliseconds = clock.tick(60)
        delta_time = milliseconds / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bubble_to_shoot.moving = True
                update_mouse_angle()
                bubble_to_shoot.angle = player.angle

        window.fill((255,255,255))
        render_grid(level.rows,level.columns)
        update_mouse_angle()
        render_mouse_angle()
        if bubble_to_shoot.moving:
            mooving_bubble(delta_time)
        draw_bubble(bubble_to_shoot.bubble_color, bubble_to_shoot.x, bubble_to_shoot.y)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
