import math
import random
import sys

import pygame.font
from pygame.constants import *

import Handshake
import data.engine as e
from Handshake import elist, font, display, txt_indicators, txt_colors, draw_particles, particle_burst
import PlayerHandshake
from RPlayer import RPlayer
from base.Item import Item
from base.ItemHoverable import ItemHoverable
from data.perlin.perlin_noise.perlin import Perlin
from entities.HomingMissile import HomingMissile
from entities.ZuraSlug import ZuraSlug
from entities.bosses.TestBoss import TestBoss
from items.HolyFeather import HolyFeather
from items.emeraldCharm import EmeraldCharm

clock = pygame.time.Clock()

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # initiates pygame
pygame.mixer.set_num_channels(64)
nfont = pygame.font.Font("data/fonts/Eight-Bit Madness.ttf", 40)
pygame.display.set_caption('Ruins')
icon = pygame.image.load("data/images/rlogo.png")
icon.set_colorkey((0, 0, 0))
pygame.display.set_icon(icon)
WIN_X = 1200
WIN_Y = 800
WINDOW_SIZE = (WIN_X, WIN_Y)  # 600, 400 image size

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window

# used as the surface for rendering, which is scaled 300,200
true_scroll = [0, 0]

CHUNK_SIZE = 8
largepfont = pygame.font.Font("data/fonts/small_pixel.ttf", 13)

e.load_animations('data/images/entities/')
PlayerHandshake.init_player(RPlayer(Handshake.jump_sound))  # TODO FIX

game_map = {}

ihovers = []
grass_img = pygame.image.load('data/images/grass.png')
dirt_img = pygame.image.load('data/images/dirt.png')
plant_img = pygame.image.load('data/images/plant.png').convert()
status_effect_imgs = {"poison": pygame.image.load("data/images/status effects/poison.png"),
                      "slow": pygame.image.load("data/images/status effects/slow.png")}

plant_img.set_colorkey((255, 255, 255))

tile_index = {1: grass_img,
              2: dirt_img,
              3: plant_img
              }

grass_sounds = [pygame.mixer.Sound('data/audio/grass_0.wav'), pygame.mixer.Sound('data/audio/grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('data/audio/music.wav')
pygame.mixer.music.play(-1)

grass_sound_timer = 0

background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]],
                      [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

colorgen = Perlin(5)
colorgen1 = Perlin(5)
colorgen2 = Perlin(5)
death_messages = ["loser", "L", "imaging dying couldn't be me", "bye bye"
    , " you have died, a man was playing and you died. look at yourself and think how you died, don't die "
    , "maybe get better"
    , "perhaps improve at the game"
    , "just way too cracked at the game"
    , "get good lmao"
    , "ez"
    , "go touch some grass now"
    , "Have you tried getting good"
    , "you’re as good at the game as Candice"
    , "just don’t suck"
    , "you just have to do good cmon"
    , "stop losing dumbass"
    , ":pepeclown:"]

current_message = death_messages[random.randint(0, len(death_messages) - 1)]

lsword = None


def generate_chunk(x, y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing
            if target_y > 10:
                tile_type = 2  # dirt
            elif target_y == 10:
                tile_type = 1  # grass
            elif target_y == 9:
                if random.randint(1, 5) == 1:
                    tile_type = 3  # plant
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data


def count(entry, entries):
    c = 0
    for e in entries:
        if e.entity.type == entry.entity.type:
            c += 1
    return c


def get_score_color():
    value = colorgen.valueAt(PlayerHandshake.player.score) * 100
    value = int(math.floor(value))
    value = abs(value)
    value1 = colorgen1.valueAt(PlayerHandshake.player.score) * 100
    value1 = int(math.floor(value1))
    value1 = abs(value1)
    value2 = colorgen2.valueAt(PlayerHandshake.player.score) * 100
    value2 = int(math.floor(value2))
    value2 = abs(value2)
    rainbow = (value + 150, value1 + 150, value2 + 150)
    return rainbow


def draw_landscape(grass_sound_timer):
    # display.fill((146, 244, 255))  # clear screen by filling it with blue
    display.fill((100, 100, 100))
    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += (PlayerHandshake.player.get_x() - true_scroll[0] - 300) / 20  # og - 152
    true_scroll[1] += (PlayerHandshake.player.get_y() - true_scroll[1] - 325) / 20  # og - 106
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0],
                               background_object[1][1] - scroll[1] * background_object[0], background_object[1][2],
                               background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (20, 170, 150), obj_rect)
        else:
            pygame.draw.rect(display, (15, 76, 73), obj_rect)

    tile_rects = []
    for y in range(3):
        for x in range(8):

            # target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 16)))
            # target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 16)))

            target_x = x - 4 + int(round(PlayerHandshake.player.entity.x / (CHUNK_SIZE * 16)))
            target_y = y - 1 + int(round(PlayerHandshake.player.entity.y / (CHUNK_SIZE * 16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x, target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]], (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]))
                if tile[1] in [1, 2]:
                    tile_rects.append(pygame.Rect(tile[0][0] * 16, tile[0][1] * 16, 16, 16))
    return tile_rects, scroll, grass_sound_timer


itemimages = {}
largeicon = pygame.transform.scale(icon, (256, 256))
while True:  # game loop
    clock.get_time()
    if Handshake.gamestate == 'dead':
        display.fill((0, 0, 0))
        boundingbox = pygame.draw.rect(display, (255, 255, 255),
                                       pygame.Rect(float(20), float(20), float(200), float(200)))
    if Handshake.gamestate == 'menu':
        display.fill((0, 0, 0))
        display.blit(largeicon, (170, 30))
        txt_surface = nfont.render("Press SPACEBAR to continue", False, (255, 255, 255))
        display.blit(txt_surface, (300 - (txt_surface.get_width() / 2), 300))  # 30, 120
    if Handshake.gamestate == 'alive':

        tile_rects, scroll, grass_sound_timer = draw_landscape(grass_sound_timer)
        PlayerHandshake.player.draw(tile_rects, grass_sound_timer, grass_sounds, display, scroll)
        for entry in elist:
            entry.draw(tile_rects, display, scroll)
        draw_particles(scroll)
        # -------------------------- draw hud -------------------------- #
        maxhealthbar = pygame.draw.rect(display, (139, 0, 0),
                                        pygame.Rect((float(10), float(10)),
                                                    (float(PlayerHandshake.player.max_health), float(10))))
        hpbar = pygame.draw.rect(display, (255, 127, 127),
                                 pygame.Rect((float(10), float(10)), (float(PlayerHandshake.player.health), float(10))))

        label = font.render(str(PlayerHandshake.player.health) + "/" + str(PlayerHandshake.player.max_health), False,
                            (255, 255, 255))

        display.blit(label, (min(PlayerHandshake.player.max_health / 2 - 10, 400), 12))
        if Handshake.bossbar is not None:
            maxbossbar = pygame.draw.rect(display, (139, 0, 139),
                                          pygame.Rect((float(100), float(100)), (float(300), float(10))))
            bbar = pygame.draw.rect(display, (255,0,255), pygame.Rect((float(100),float(100)), (float((
                                                                                                                  Handshake.bossbar.health / Handshake.bossbar.max_health) * 300), float(10))))
        iterated = []
        hudix = 10
        hudiy = 30
        hudex = 10
        hudey = 70

        for item in PlayerHandshake.player.items:
            if not iterated.__contains__(item.entity.type):
                c = count(item, PlayerHandshake.player.items)
                if not itemimages.keys().__contains__(item.entity.type):
                    iimg = pygame.image.load("data/images/entities/" + item.entity.type + "/idle/idle_0.png")
                    iimg.set_alpha(50)
                    iimg.set_colorkey((255, 255, 255))
                    itemimages[item.entity.type] = iimg

                itemimage = itemimages[item.entity.type]

                if c > 1:
                    countl = font.render("x" + str(c), False, (255, 255, 255))
                    display.blit(itemimage, (hudix, hudiy))
                    display.blit(countl, (hudix + item.entity.size_x, hudiy + item.entity.size_x + 5))

                else:
                    display.blit(itemimage, (hudix, hudiy))

                hovero = ItemHoverable(hudix, hudiy, hudix + itemimage.get_size()[0],
                                       hudiy + itemimage.get_size()[1], item.name, item.desc)
                if not ihovers.__contains__(hovero):
                    ihovers.append(hovero)
                hudix += item.entity.size_x + 12
                iterated.append(item.entity.type)

        for hoverable in ihovers:
            hoverable.onhover(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        for fading in txt_indicators:  # txt_indicators.append([amount,type,120,self.entity.x,self.entity.y])
            tlabel = largepfont.render(str(fading[0]), False, txt_colors[fading[1]])
            tlabel.set_alpha((fading[2] / 120) * 100)
            fading[2] -= 1
            display.blit(tlabel, (fading[3] - scroll[0], fading[4] - scroll[1]))
            if fading[2] <= 0:
                txt_indicators.remove(fading)

        for effect in PlayerHandshake.player.statuseffects.keys():
            ticks = PlayerHandshake.player.statuseffects[effect]
            if ticks > 0:
                display.blit(status_effect_imgs[effect], (hudex, hudey))
                hudex += 15

        color = (255, 255, 255)
        goldc = (212, 175, 55)
        if PlayerHandshake.player.score > 10:
            color = goldc
        scorel = font.render("Score: " + str(PlayerHandshake.player.score), False, color)
        display.blit(scorel, (10, 60))
        # -------------------------- draw hud -------------------------- #
        for event in pygame.event.get():  # event loop
            if event.type == KEYDOWN:
                if event.key == K_p:
                    particle_burst(100, (255, 255, 255), PlayerHandshake.player.entity.x,
                                   PlayerHandshake.player.entity.y)
                if event.key == K_h:
                    elist.append(HomingMissile(PlayerHandshake.player.entity.x, PlayerHandshake.player.entity.y - 100))
                if event.key == K_i:
                    elist.append(Item(PlayerHandshake.player.entity.x, PlayerHandshake.player.entity.y, 'tester',
                                      'Increases walk speed, jump strength and max hp', "potion of strength"))
                if event.key == K_e:
                    elist.append(EmeraldCharm(PlayerHandshake.player.entity.x, PlayerHandshake.player.entity.y))
                if event.key == K_n:
                    elist.append(HolyFeather(PlayerHandshake.player.entity.x, PlayerHandshake.player.entity.y))
                if event.key == K_f:
                    PlayerHandshake.player.heal(random.randint(1, 10), 'magical_heal')
                if event.key == K_a:
                    PlayerHandshake.player.attack()
                if event.key == K_t:
                    elist.append(TestBoss(PlayerHandshake.player.entity.x, PlayerHandshake.player.entity.y - 50))
                if event.key == K_z:
                    elist.append(ZuraSlug(PlayerHandshake.player.entity.x, 0))

            PlayerHandshake.player.event(event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if Handshake.gamestate == "menu":
                    Handshake.gamestate = 'alive'
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)
