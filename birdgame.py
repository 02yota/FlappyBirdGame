import pygame
import sys
import random

def create_pipe():
    """
    Эта функция создает 2 трубы на случайной высоте из списка "pipe_height", одна труба сверху, вторая снизу.
    :return: Координаты верхней трубы и нижней
    """
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom  =(700, random_pipe_pos-300))
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    return  bottom_pipe, top_pipe

def move_pipes(pipes):
    """
    Эта функция постепенно двигает созданные трубы к птице, имитируя движение птицы.
    :param pipes: Координаты труб
    :return: Координаты труб смешенные на 6 к птице
    """
    for pipe in pipes:
        pipe.centerx -= 6
    return pipes

def check_score(pipes,score):
    """
    Эта функция проверяет прошла ли птица через трубу(проверяет, совпадает ли первая координата птицы и трубы), и добавляет балл если птица прошла.
    :param pipes: Координаты трубы
    :param score: Текущий счет
    :return: Новый счет
    """
    if len(pipes) >1:
        if pipes[score*2][0] == bird_rect[0]:
            score = score + 1
            point_sound.play()
    else:
        score=score

    return score

def game_floor():
    """
    Эта функция постоянно дорисовывает пол
    :return: None
    """
    screen.blit(floor_base,(floor_x_pos,900))
    screen.blit(floor_base, (floor_x_pos + 576, 900))

def check_collision(pipes):
    """
    Эта функция проверяет не столкнулась ли птица с полом, потолком или трубами, и если столкнулась то принимает значение False.
    :param pipes: Координаты труб
    :return: True если не столкнулась, False если столкнулась
    """
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        die_sound.play()
        return False
    else:
        return True


def draw_pipes(pipes):
    """
    Эта функция рисует трубы в зависимости от их координат.
    :param pipes: Координаты труб
    :return: None
    """
    for pipe in pipes:
        if pipe.bottom >=1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)

def rotate_bird(bird):
    """
    Эта функция вращает птицу в зависимости от ее движения.
    :param bird: Текущая птица
    :return: Повернутая птица
    """
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
    return new_bird

def bird_animation():
    """
    Эта функция создает анимацию полета птицы постановкой различных спрайтов.
    :return: Изображение птицы с нужной анимацией крыльев, ее расположение
    """
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    """
    Эта функция отображает счет во время игры, и во время проигрыша отображает счет, которого смогли достигнуть в прошлой попытке и наилучший результат за все попытки.
    :param game_state: Текущее состояние игры("main_game" если идет игра, "game_over" если игра не идет)
    :return: None
    """
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center =(288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'HighScore:{int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    """
    Эта функция проверяет выше ли ваш текущий счет вашего наилучшего, если да то обновляет его.
    :param score: Текущий счет
    :param high_score: Наилучший счет
    :return: Обновленные наилучший счет
    """
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
clock = pygame.time.Clock()
gravity = 0.25
bird_movement = 0
game_font = pygame.font.Font('C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/04B_19_.TTF',40)

screen = pygame.display.set_mode((576,1024))

backgroud = pygame.image.load("C:/Users/User/Desktop/flappybird/background-day.png").convert()
backgroud = pygame.transform.scale2x(backgroud)

bird_down = pygame.image.load("C:/Users/User/Desktop/flappybird/yellowbird-downflap.png").convert_alpha()
bird_down = pygame.transform.scale2x(bird_down)
bird_mid = pygame.image.load("C:/Users/User/Desktop/flappybird/yellowbird-midflap.png").convert_alpha()
bird_mid = pygame.transform.scale2x(bird_mid)
bird_up = pygame.image.load("C:/Users/User/Desktop/flappybird/yellowbird-upflap.png").convert_alpha()
bird_up = pygame.transform.scale2x(bird_up)

bird_frames = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_frames[bird_index]
bird_rect = bird.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

floor_base = pygame.image.load("C:/Users/User/Desktop/flappybird/base.png").convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x_pos = 0

message = pygame.image.load("C:/Users/User/Desktop/flappybird/message.png").convert_alpha()
message = pygame.transform.scale2x(message)
game_over_rect = message.get_rect(center=(288,512))

pipe_surface = pygame.image.load("C:/Users/User/Desktop/flappybird/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400,600,800]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

score = 0
high_score = 0

flap_sound = pygame.mixer.Sound("C:/Users/User/Desktop/flappybird/audio_flap.wav")
die_sound = pygame.mixer.Sound("C:/Users/User/Desktop/flappybird/audio_die.wav")
point_sound = pygame.mixer.Sound("C:/Users/User/Desktop/flappybird/audio_point.wav")

game_active = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0
                pipe_list.clear()
                game_active = True
        if event.type == SPAWNPIPE and game_active:
                pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP and game_active:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird,bird_rect = bird_animation()

    screen.blit(backgroud,(0,0))
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        pipe_list = move_pipes(pipe_list)
        score = check_score(pipe_list,score)
        draw_pipes(pipe_list)
        game_active = check_collision(pipe_list)
        score_display('main_game')
    else:
        high_score = update_score(score,high_score)
        screen.blit(message,game_over_rect)
        score_display('game_over')



    floor_x_pos -=1
    game_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(60)