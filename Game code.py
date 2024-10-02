import pygame, sys, random

def draw_bg():
    screen.blit(bg_surface,(bg_x_pos,0))
    screen.blit(bg_surface,(bg_x_pos + 1100,0))

def draw_ship():
    screen.blit(ship_surface, ship_rect)

def ship_animation():
    new_ship = ship_frames[ship_index]
    new_ship_rect = new_ship.get_rect(center = (100,ship_rect.centery))
    return new_ship, new_ship_rect

def ship_movement():
    global ship_rect
    ship_rect.y += ship_speed
    if ship_rect.top <=0:
        ship_rect.y -= ship_speed
    if ship_rect.bottom >= screen_height:
        ship_rect.y -= ship_speed

def create_asteroid():
    global random_asteroid_posx, random_asteroid_posy
    random_asteroid_posy = random.choice(asteroid_height)
    random_asteroid_posx = random.choice(asteroid_distance)
    random_asteroid_distance_js = random.choice(asteroid_distance_js)
    first_asteroid = asteroid_surface.get_rect(midtop = (1700,random_asteroid_posy))
    second_asteroid = asteroid_surface.get_rect(midbottom=(1700 - random_asteroid_posx, random_asteroid_posy - random_asteroid_distance_js))
    return first_asteroid, second_asteroid

def create_barrel():
    random_barrel_posy = random.choice(barrel_height)
    barrel = barrel_surface.get_rect(midtop = (1700,random_barrel_posy))
    return barrel

def move_asteroids(asteroids):
    for asteroid in asteroids:
        asteroid.centerx -= 5
    return  asteroids

#def move_barrel(barrels):
    #for barrel in barrels:
        #barrel.centerx -= 5
    #return  barrels

def draw_asteroids(asteroids):
    for asteroid in asteroids:
        screen.blit(asteroid_surface,asteroid)

#def draw_barrel(barrels):
    #for barrel in barrels:
        #screen.blit(barrel_surface,barrel)

def check_collision(asteroids):
    for asteroid in asteroids:
        if ship_rect.colliderect(asteroid):
            return False
    return True

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)) + ' km', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (550,700))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'{int(score)} km', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (550,700))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score: {int(score)} km', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (550,100))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()
clock = pygame.time.Clock()
game_font = pygame.font.Font(None,40)

# Setting up the window
screen_width = 1100
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('My game')


bg_surface = pygame.image.load('game_assets/background.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
bg_x_pos = 0

# Game variable
ship_speed = 0
game_active = True
score = 0
high_score = 0


ship_pos1 = pygame.image.load('game_assets/spaceship_pos1.png').convert_alpha()
ship_pos2 = pygame.image.load('game_assets/spaceship_pos2.png').convert_alpha()
ship_frames = [ship_pos1, ship_pos2]
ship_index = 0
ship_surface = ship_frames[ship_index]
ship_rect = ship_surface.get_rect(center = (100,400))


asteroid_surface = pygame.image.load('game_assets/asteroid.png').convert_alpha()
asteroid_list = []

SPAWNASTEROID = pygame.USEREVENT
pygame.time.set_timer(SPAWNASTEROID,1200)
asteroid_height = [100,200,300,400,500,600]
asteroid_distance =[300,400,500,0]
asteroid_distance_js = [100,200,300,400]

SHIPFLAME = pygame.USEREVENT + 1
pygame.time.set_timer(SHIPFLAME,200)


barrel_surface = pygame.image.load('game_assets/barrel.png').convert_alpha()

barrel_list = []

SPAWNBARREL = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNBARREL,5000)
barrel_height = [100,150,200,250,300,350,400,450,500,550,600]


# ship_surface = pygame.image.load('game_assets/spaceship_pos2.png').convert_alpha()
# ship_surface = pygame.transform.scale(ship_surface, (200,200))
# ship_rect = ship_surface.get_rect(center = (100, 400))

game_over_surface = pygame.image.load('game_assets/start.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (550,400))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SHIPFLAME:
            if ship_index < 1:
                ship_index += 1
            else:
                ship_index = 0

            ship_surface, ship_rect = ship_animation()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                ship_speed += 5
            if event.key == pygame.K_UP:
                ship_speed -= 5

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                asteroid_list.clear()
                barrel_list.clear()
                ship_rect.center = (100,400)
                score = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                ship_speed -= 5
            if event.key == pygame.K_UP:
                ship_speed += 5


        if event.type == SPAWNASTEROID:
            asteroid_list.extend(create_asteroid())

        if event.type == SPAWNBARREL:
            barrel_list.extend(create_barrel())

    draw_bg()
    bg_x_pos -= 1
    if game_active:
        ship_movement()

        # Asteroizi
        asteroid_list = move_asteroids(asteroid_list)
        game_active = check_collision(asteroid_list)

        # Butoaie
        #barrel_list = move_barrel(asteroid_list)


        # Visuals
        screen.blit(ship_surface, ship_rect)
        draw_ship()
        draw_asteroids(asteroid_list)
        draw_asteroids(asteroid_list)
        #draw_barrel(barrel_list)
        if bg_x_pos < -1100:
            bg_x_pos = 0
        score += 0.01
        score_display('main_game')

    else:
        high_score = update_score(score,high_score)
        score_display('game_over')
        screen.blit(game_over_surface,game_over_rect)

    pygame.display.update()
    clock.tick(120)