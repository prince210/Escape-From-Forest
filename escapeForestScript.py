import pygame,sys,glob,random,math
from pygame import mixer

## pygame setup
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Escape From Forest")
icon = pygame.image.load("assets/woodland.png")
pygame.display.set_icon(icon)


## game variables
game_active = True
CollisionElement = set()
collision_count = 0
score_font = pygame.font.Font('assets/04B_19.TTF',60)
high_score_font = pygame.font.Font('assets/04B_19.TTF',45)
knife_count_font = pygame.font.Font('assets/04B_19.TTF',60)
restart_text_font = pygame.font.Font('assets/04B_19.TTF',30)
level_count = 0
level_count_font = pygame.font.Font('assets/04B_19.TTF',130)
blinkCount = 0
score = 0
high_score = 0
game_coin_surface = pygame.transform.scale(pygame.image.load('assets/coins/coin_1.png').convert_alpha(),(60,60))
game_coin_rect = game_coin_surface.get_rect(center = (screen_width - 110,100))
game_over_surface = pygame.transform.scale(pygame.image.load('assets/gameover.png').convert_alpha(),(420,200))
knife_count_surface = pygame.transform.scale(pygame.image.load('assets/knifes/french-knife-5.png').convert_alpha(),(60,60))
knife_count_rect = knife_count_surface.get_rect(center = (screen_width - 250,100))
knifeCount = 3
isOpen = True



## adding music
mixer.music.load('assets/background-1.mp3')
mixer.music.play(-1)
walk_sound = mixer.Sound('assets/Running-footsteps-in-grass-.wav')
jump_sound = mixer.Sound('assets/jump.mp3')
knife_throw_sound = mixer.Sound('assets/throw-knife.mp3')
player_hurt_sound = mixer.Sound('assets/player-hurt.wav')
level_up_sound = mixer.Sound('assets/level-up.wav')
enemy_die_sound = mixer.Sound('assets/enemy-die.mp3')
player_die_sound = mixer.Sound('assets/player-die.wav')
coin_grab_sound = mixer.Sound('assets/coin.wav')




## background
background = pygame.image.load('assets/Layers/backGround.png').convert()
background_2 = pygame.image.load('assets/Layers/backGround2.png').convert()
background_3 = pygame.image.load('assets/Layers/backGround3.png').convert()
background_4 = pygame.image.load('assets/Layers/backGround4.png').convert()
speedOfBackGround = 0.25
count = [5,10,20,40]
backGround_list = [background,background_2,background_3,background_4]
groundX = 0
ind = 0
isBackGroundChange = False
isCollided = False

def slideBackGround(back_ground):
    screen.blit(back_ground,(groundX,0))
    screen.blit(back_ground,(groundX + 800,0))


def display_score(score,state,high_score):
    if state == 'INGAME':
        score_surface = score_font.render(str(score),True,(255,255,255))  ## arg2 show how sharp the image should look like
        screen.blit(score_surface,(screen_width-70,80))
    if state == 'GAMEOVER':
        score_surface = score_font.render(str(score), True,(255, 255, 255))  ## arg2 show how sharp the image should look like
        screen.blit(score_surface, (screen_width-70, 80))

        high_score_surface = high_score_font.render('High Score : ' + str(high_score), True,(255, 255, 255))  ## arg2 show how sharp the image should look like
        screen.blit(high_score_surface, (240, 470))

def display_knifeCount(knifeCount):
    CountOfKnifes = knife_count_font.render(str(knifeCount),True,(255,255,255))
    screen.blit(CountOfKnifes,(screen_width - 220,80))

def display_level_count(levelCount):
    countOfLevels = level_count_font.render('Level ' + str(levelCount),True,(255,255,255))
    screen.blit(countOfLevels,(200,150))

def update_high_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

def drawHealth(health):
    screen.blit(health, (50, 50))

def restartText():
    renderedText = restart_text_font.render(" PRESS ENTER TO RESTART ", True, (255, 255, 255))
    screen.blit(renderedText, (215, 400))

class player:
    def __init__(self):

        ## character idle
        self.idle_movements_surfaces = []
        self.total_images_idle = 0
        for img in glob.glob('assets/Idle/*'):
            man_surface_idle = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (200, 200))
            self.idle_movements_surfaces.append(man_surface_idle)
            self.total_images_idle += 1
        self.char_movement_ind = 0
        self.man_surface_idle = self.idle_movements_surfaces[self.char_movement_ind]
        self.man_rect_idle = self.man_surface_idle.get_rect(center=(140, 450))
        self.IDLE = pygame.USEREVENT
        pygame.time.set_timer(self.IDLE, 80)
        self.isIdle = True

        ## character walking
        self.walk_movements_surfaces = []
        self.total_images_walking = 0
        for img in glob.glob('assets\Walking\*'):
            man_surface_walk = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (200, 200))
            self.walk_movements_surfaces.append(man_surface_walk)
            self.total_images_walking += 1
        self.char_walk_ind = 0
        self.man_surface_walk = self.walk_movements_surfaces[self.char_walk_ind]
        self.man_rect_walk = self.man_surface_walk.get_rect(center=(150, 450))
        self.isWalk = False
        self.WALKING = pygame.USEREVENT + 1
        pygame.time.set_timer(self.WALKING, 50)

        ## character jump
        self.jump_movements_surfaces = []
        self.total_images_jumping = 0
        for img in glob.glob('assets\Jump\*'):
            man_surface_Jump = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (200, 200))
            self.jump_movements_surfaces.append(man_surface_Jump)
            self.total_images_jumping += 1
        self.char_jump_ind = 0
        self.man_surface_Jump = self.jump_movements_surfaces[self.char_jump_ind]
        self.man_rect_Jump = self.man_surface_Jump.get_rect(center=(160, 450))
        self.isJump = False
        self.playerX = self.man_rect_Jump.centerx
        self.playerY = self.man_rect_Jump.centery
        self.jump_height = 20


        ## character slide
        self.slide_movements_surfaces = []
        self.total_images_slide = 0
        for img in glob.glob('assets\Sliding\*'):
            man_surface_sliding = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (200, 200))
            self.slide_movements_surfaces.append(man_surface_sliding)
            self.total_images_slide += 1
        self.char_slide_ind = 0
        self.man_surface_sliding = self.slide_movements_surfaces[self.char_slide_ind]
        self.man_rect_slide = self.man_surface_sliding.get_rect(center=(170, 450))
        self.isSlide = False

        ## character die
        self.die_movements_surfaces = []
        self.total_images_die = 0
        for img in glob.glob('assets\Die\*'):
            man_surface_dying = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (200, 200))
            self.die_movements_surfaces.append(man_surface_dying)
            self.total_images_die += 1
        self.char_die_ind = 0
        self.man_surface_dying = self.die_movements_surfaces[self.char_die_ind]
        self.isDie = False

        ## character throw
        self.throw_movements_surfaces = []
        self.total_images_throw = 0
        for img in glob.glob('assets\Run Throw\*'):
            man_surface_throwing = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (200, 200))
            self.throw_movements_surfaces.append(man_surface_throwing)
            self.total_images_throw += 1
        self.char_throw_ind = 0
        self.man_surface_throwing = self.throw_movements_surfaces[self.char_throw_ind]
        self.isThrown = False

        ## character hurt
        self.hurt_movements_surfaces = []
        self.total_images_hurt = 0
        for img in glob.glob('assets\Hurt\*'):
            man_surface_hurted = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (200, 200))
            self.hurt_movements_surfaces.append(man_surface_hurted)
            self.total_images_hurt += 1
        self.char_hurt_ind = 0
        self.man_surface_hurted = self.hurt_movements_surfaces[self.char_hurt_ind]
        self.isHurt = False

        ## knife
        self.knife_surface_list = []
        self.total_knife = 0
        for img in glob.glob('assets\knifes\*'):
            self.total_knife += 1
            knife_surface = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (60, 60))
            self.knife_surface_list.append(knife_surface)
        self.knife_ind = 0
        self.knife_surface = self.knife_surface_list[self.knife_ind]
        self.SPAWNKNIFES = pygame.USEREVENT + 5
        pygame.time.set_timer(self.SPAWNKNIFES, 100)
        self.knifesLocationX = self.playerX + 10
        self.knifesLocationY = self.playerY + 30
        self.knifeThrown = False

        ## health bar
        self.health_6 = pygame.transform.scale(pygame.image.load(
            'assets\heath\health-6.png').convert_alpha(),
                                          (150, 45))
        self.health_1 = pygame.transform.scale(pygame.image.load(
            'assets\heath\health-1.png').convert_alpha(),
                                          (150, 45))
        self.health_2 = pygame.transform.scale(pygame.image.load(
            'assets\heath\health-2.png').convert_alpha(),
                                          (150, 45))
        self.health_3 = pygame.transform.scale(pygame.image.load(
            'assets\heath\health-3.png').convert_alpha(),
                                          (150, 45))
        self.health_4 = pygame.transform.scale(pygame.image.load(
            'assets\heath\health-4.png').convert_alpha(),
                                          (150, 45))
        self.health_5 = pygame.transform.scale(pygame.image.load(
            'assets\heath\health-5.png').convert_alpha(),
                                          (150, 45))
        self.heath_list = [self.health_6, self.health_5, self.health_4, self.health_3, self.health_2, self.health_1]
        self.health_index = 0

    def animate_idle_char(self):
        new_man_surface = self.idle_movements_surfaces[self.char_movement_ind]
        new_man_rect = new_man_surface.get_rect(center=(300, self.man_rect_idle.centery))
        return new_man_surface, new_man_rect

    def animate_walk_char(self):
        global groundX

        if self.playerX < screen_width // 2:
            self.playerX += 2
        groundX -= 8
        new_walk_surface = self.walk_movements_surfaces[self.char_walk_ind]
        new_walk_rect = new_walk_surface.get_rect(center=(300, self.man_rect_walk.centery))
        return new_walk_surface, new_walk_rect

    def animate_jump_char(self):
        global groundX

        groundX -= 10
        if self.playerX < screen_width // 2:
            self.playerX += 8
        new_jump_surface = self.jump_movements_surfaces[self.char_jump_ind]
        new_jump_rect = new_jump_surface.get_rect(center=(self.playerX, self.man_rect_Jump.centery))
        return new_jump_surface, new_jump_rect

    def animate_slide_char(self):
        global groundX

        groundX -= self.total_images_slide + self.total_images_walking * 2
        if self.playerX < screen_width // 2:
            self.playerX += self.total_images_slide + self.total_images_walking * 2
        new_slide_surface = self.slide_movements_surfaces[self.char_slide_ind]
        new_slide_rect = new_slide_surface.get_rect(center=(self.playerX, self.man_rect_slide.centery))
        return new_slide_surface, new_slide_rect

    def animate_die_char(self):
        new_die_surface = self.die_movements_surfaces[self.char_die_ind]
        new_die_rect = new_die_surface.get_rect(center=(self.playerX, self.man_rect_slide.centery))
        return new_die_surface, new_die_rect

    def animate_throw_char(self):
        new_throw_surface = self.throw_movements_surfaces[self.char_throw_ind]
        new_throw_rect = new_throw_surface.get_rect(center=(self.playerX, self.man_rect_walk.centery))
        return new_throw_surface, new_throw_rect

    def animate_hurt_char(self):
        new_hurt_surface = self.hurt_movements_surfaces[self.char_hurt_ind]
        new_hurt_rect = new_hurt_surface.get_rect(center=(self.playerX, self.man_rect_walk.centery))
        return new_hurt_surface, new_hurt_rect

    def animate_throw_knife(self):
        new_throw_knife = self.knife_surface_list[self.knife_ind]
        new_throw_knife_rect = new_throw_knife.get_rect(center=(self.playerX, self.man_rect_walk.centery))
        return new_throw_knife, new_throw_knife_rect

    def move_enemies(self,enemies):
        for enemy in enemies:
            if self.isIdle:
                if 'pumpkin' in enemy.keys():
                    enemy['pumpkin'].centerx -= 5
                if 'blob' in enemy.keys():
                    enemy['blob'].centerx -= 5
                if 'monster' in enemy.keys():
                    enemy['monster'].centerx -= 3
                if 'coins' in enemy.keys():
                    enemy['coins'].centerx -= 4
            if self.isJump:
                if 'pumpkin' in enemy.keys():
                    enemy['pumpkin'].centerx -= self.total_images_jumping + self.total_images_slide + self.total_images_walking
                if 'blob' in enemy.keys():
                    enemy['blob'].centerx -= self.total_images_jumping + self.total_images_slide + self.total_images_walking
                if 'monster' in enemy.keys():
                    enemy['monster'].centerx -= self.total_images_jumping + self.total_images_slide + self.total_images_walking - 5
                if 'coins' in enemy.keys():
                    enemy['coins'].centerx -= self.total_images_jumping + self.total_images_slide + self.total_images_walking - 5
            if self.isWalk:
                if 'pumpkin' in enemy.keys():
                    enemy['pumpkin'].centerx -= 12
                if 'blob' in enemy.keys():
                    enemy['blob'].centerx -= 12
                if 'monster' in enemy.keys():
                    enemy['monster'].centerx -= 9
                if 'coins' in enemy.keys():
                    enemy['coins'].centerx -= 7
            if self.isSlide:
                if 'pumpkin' in enemy.keys():
                    enemy['pumpkin'].centerx -= (self.total_images_slide * 2 + self.total_images_walking * 2) * 2
                if 'blob' in enemy.keys():
                    enemy['blob'].centerx -= (self.total_images_slide * 2 + self.total_images_walking * 2) * 2
                if 'monster' in enemy.keys():
                    enemy['monster'].centerx -= (self.total_images_slide * 2 + self.total_images_walking * 2) * 2
                if 'coins' in enemy.keys():
                    enemy['coins'].centerx -= (self.total_images_slide * 2 + self.total_images_walking * 2) * 2
            if self.isThrown:
                if 'pumpkin' in enemy.keys():
                    enemy['pumpkin'].centerx -= 5
                if 'blob' in enemy.keys():
                    enemy['blob'].centerx -= 5
                if 'monster' in enemy.keys():
                    enemy['monster'].centerx -= 3
                if 'coins' in enemy.keys():
                    enemy['coins'].centerx -= 4
        return enemies

    def checkCollision(self,enemies, man):
        global CollisionElement
        global isCollided
        global score
        global coin_grab_sound

        for count, enemy in enumerate(enemies):
            x2 = man.centerx
            y2 = man.centery

            if 'monster' in enemy.keys():
                x1_monster = enemy['monster'].centerx
                y1_monster = enemy['monster'].centery
                dist_monster = math.sqrt((y2 - y1_monster) ** 2 + (x2 - x1_monster) ** 2)
                if (dist_monster <= 50):
                    if (count not in CollisionElement):
                        isCollided = True
                        CollisionElement.add(count)

                if self.knifeThrown:
                    knx = self.knifesLocationX
                    kny = self.knifesLocationY
                    distKnifeFromMonster = math.sqrt((kny - y1_monster) ** 2 + (knx - x1_monster) ** 2)
                    if distKnifeFromMonster <= 50:
                        self.knifeThrown = False
                        enemy['monster'].centerx = -50
                        enemy['monster'].centery = 650

            if 'pumpkin' in enemy.keys():
                x1_pump = enemy['pumpkin'].centerx
                y1_pump = enemy['pumpkin'].centery
                dist_pump = math.sqrt((y2 - y1_pump) ** 2 + (x2 - x1_pump) ** 2)
                if dist_pump >= 83 and dist_pump <= 86:
                    if count not in CollisionElement:
                        isCollided = True
                        CollisionElement.add(count)
                if self.knifeThrown:
                    knx = self.knifesLocationX
                    kny = self.knifesLocationY
                    distKnifeFromPump = math.sqrt((kny - y1_pump) ** 2 + (knx - x1_pump) ** 2)
                    if distKnifeFromPump <= 65:
                        self.knifeThrown = False
                        enemy['pumpkin'].centerx = -50
                        enemy['pumpkin'].centery = 650

            if 'blob' in enemy.keys():
                x1_blob = enemy['blob'].centerx
                y1_blob = enemy['blob'].centery
                dist_blob = math.sqrt((y2 - y1_blob) ** 2 + (x2 - x1_blob) ** 2)
                if dist_blob <= 50:
                    if count not in CollisionElement:
                        isCollided = True
                        CollisionElement.add(count)
                if self.knifeThrown:
                    knx = self.knifesLocationX
                    kny = self.knifesLocationY
                    distKnifeFromBlob = math.sqrt((kny - y1_blob) ** 2 + (knx - x1_blob) ** 2)
                    if distKnifeFromBlob <= 50:
                        self.knifeThrown = False
                        enemy['blob'].centerx = -50
                        enemy['blob'].centery = 650

            if 'coins' in enemy.keys():
                if count not in CollisionElement and enemy['coins'].colliderect(man):
                    score += 1
                    enemy['coins'].centerx = -50
                    enemy['coins'].centery = 650
                    CollisionElement.add(count)
                    coin_grab_sound.play()

        return isCollided

    def ThrowKnife(self,x, y):
        global knifeCount
        global muteSound

        if knifeCount >= 0:
            self.knifeThrown = True
            screen.blit(self.knife_surface, (x + 16, y))
        else:
            knifeCount = 0


class Enemy:
    def __init__(self):
        ## creating enemies
        ## first pumpkin
        self.pumpkin_surface = pygame.image.load(
            'assets\pumpkin_11.png')
        self.pumpkin_surface = pygame.transform.scale(self.pumpkin_surface, (120, 120))
        self.pumpkin_Xpos = [1190, 1200, 1300, 1400, 1500, 1600, 1700, 1780]
        self.pumpkin_Ypos = [130, 215, 370]

        ## second blob [insect]
        self.blob_surface = pygame.image.load(
            'assets\\blob.png')
        self.blob_surface = pygame.transform.scale(self.blob_surface, (65, 65))
        self.blob_Xpos = [1520, 1660, 1770]

        ## third monster
        self.monster_surface_list = []
        self.total_monster = 0
        for img in glob.glob('assets\enemy\enemy_1\*'):
            self.total_monster += 1
            monster_surface_attack = pygame.transform.scale(pygame.image.load(img), (120, 120))
            self.monster_surface_list.append(monster_surface_attack)
        self.monster_attack_ind = 0
        self.monster_surface_attack = self.monster_surface_list[self.monster_attack_ind]
        # monster_surface_rect = monster_surface_attack.get_rect(midbottom = (650,550))
        self.SPAWNMONSTER = pygame.USEREVENT + 3
        pygame.time.set_timer(self.SPAWNMONSTER, 200)

        self.enemies = []
        self.SPAWNENEMY = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SPAWNENEMY, 7000)

        ## coins
        self.coin_surface_list = []
        self.total_coins = 0
        for img in glob.glob('assets\coins\*'):
            self.total_coins += 1
            coins_surface = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (60, 60))
            self.coin_surface_list.append(coins_surface)
        self.coins_ind = 0
        self.coins_surface = self.coin_surface_list[self.coins_ind]
        self.SPAWNCOINS = pygame.USEREVENT + 4
        pygame.time.set_timer(self.SPAWNCOINS, 100)
        self.coinslocationX = [850, 900, 950]
        self.coinslocationY = [500, 450, 400]

    def create_enemies(self):
        global isBackGroundChange

        pumpkin_rect_choice_1 = self.pumpkin_surface.get_rect(
            center=(random.choice(self.pumpkin_Xpos), random.choice(self.pumpkin_Ypos)))
        blob_rect_choice_1 = self.blob_surface.get_rect(center=(random.choice(self.blob_Xpos), 480))
        monster_rect_choice_1 = self.monster_surface_attack.get_rect(midbottom=(900, 550))
        coins = self.coins_surface.get_rect(center=(random.choice(self.coinslocationX), random.choice(self.coinslocationY)))
        enemy_type_1 = {'pumpkin': pumpkin_rect_choice_1}
        enemy_type_2 = {'blob': blob_rect_choice_1}
        enemy_type_3 = {'monster': monster_rect_choice_1}
        create_coins = {'coins': coins}
        return enemy_type_1, enemy_type_2, enemy_type_3, create_coins


    def draw_enemies(self,enemies):
        for enemy in enemies:
            if 'pumpkin' in enemy.keys():
                screen.blit(self.pumpkin_surface, enemy['pumpkin'])
            if 'blob' in enemy.keys():
                screen.blit(self.blob_surface, enemy['blob'])
            if 'monster' in enemy.keys():
                screen.blit(self.monster_surface_attack, enemy['monster'])
            if 'coins' in enemy.keys():
                screen.blit(self.coins_surface, enemy['coins'])

    def animate_attack_monster(self):
        self.new_monster_surface = self.monster_surface_list[self.monster_attack_ind]
        self.new_monster_rect = self.new_monster_surface.get_rect(midbottom=(650, 500))
        return self.new_monster_surface, self.new_monster_rect

    def animate_coins_movement(self):
        self.new_coins_surface = self.coin_surface_list[self.coins_ind]
        self.new_coins_rect = self.new_coins_surface.get_rect(midbottom=(650, 500))
        return self.new_coins_surface, self.new_coins_rect


start_time = pygame.time.get_ticks()
newPlayer = player()
newEnemy = Enemy()
while isOpen:
    screen.fill((0,0,0))

    # background
    slideBackGround(backGround_list[ind])
    if groundX <= -800:
        groundX = 0
        count[ind] = count[ind] - 1
        if count[ind] == 0:
            start_time = pygame.time.get_ticks()
            ind += 1
            if ind > 0:
                print('played level up sound')
                level_up_sound.play()
            if knifeCount == 0:
                knifeCount = 2
            else:
                knifeCount *= 2

    # level
    if start_time:
        if (pygame.time.get_ticks() - start_time) < 1500:
            display_level_count(ind + 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                newPlayer.isThrown = True
                newPlayer.isIdle = False
                newPlayer.isJump = False
                newPlayer.isWalk = False
                newPlayer.isSlide = False
                if not newPlayer.knifeThrown:
                    knifeCount -= 1
                    if knifeCount < 0:
                        newPlayer.knifeThrown = False
                    else:
                        knife_throw_sound.play()
                    newPlayer.knifesLocationX = newPlayer.man_rect_walk.centerx
                    newPlayer.knifesLocationY = newPlayer.man_rect_walk.centery
                    newPlayer.ThrowKnife(newPlayer.knifesLocationX,newPlayer.knifesLocationY)
            if event.key == pygame.K_RETURN and not game_active:
                game_active = True
                isCollided = False
                score = 0
                knifeCount = 3
                groundX = 0
                mixer.music.play(-1)
            if event.key == pygame.K_RIGHT:
                newPlayer.isWalk = True
                newPlayer.isIdle = False
                newPlayer.isJump = False
                newPlayer.isSlide = False

            elif event.key == pygame.K_SPACE:
                jump_sound.play()
                newPlayer.isJump = True
                newPlayer.isWalk = False
                newPlayer.isIdle = False
                newPlayer.isSlide = False

            elif event.key == pygame.K_RIGHT and pygame.key == pygame.K_SPACE:
                newPlayer.isJump = True
                newPlayer.isWalk = True
                newPlayer.isIdle = False
                newPlayer.isSlide = False

            elif pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                newPlayer.isSlide = True
                newPlayer.isWalk = False
                newPlayer.isJump = False
                newPlayer.isIdle = False
            else:
                newPlayer.isJump = False
                newPlayer.isWalk = False
                newPlayer.isSlide = False
                newPlayer.isIdle = True

        if event.type == pygame.KEYUP:
            newPlayer.isWalk = False
            newPlayer.isJump = False
            newPlayer.isIdle = True
            newPlayer.isSlide = False
            newPlayer.isThrown = False

        if event.type == newPlayer.IDLE:
            if newPlayer.char_movement_ind < newPlayer.total_images_idle-1:
                newPlayer.char_movement_ind += 1
            else:
                newPlayer.char_movement_ind = 0
            newPlayer.man_surface_idle,newPlayer.man_rect_idle = newPlayer.animate_idle_char()

        if event.type == newEnemy.SPAWNMONSTER:
            if newEnemy.monster_attack_ind < newEnemy.total_monster-1:
                newEnemy.monster_attack_ind += 1
            else:
                newEnemy.monster_attack_ind = 0
            newEnemy.monster_surface_attack, newEnemy.monster_surface_rect = newEnemy.animate_attack_monster()

        if event.type == newEnemy.SPAWNENEMY:
            newEnemy.enemies.extend(newEnemy.create_enemies())
        if event.type == newEnemy.SPAWNCOINS:
            if newEnemy.coins_ind < newEnemy.total_coins-1:
                newEnemy.coins_ind += 1
            else:
                newEnemy.coins_ind = 0
            newEnemy.coins_surface, newEnemy.coins_surface_rect = newEnemy.animate_coins_movement()

    if game_active:
        ## character idle
        if newPlayer.isIdle:
            newPlayer.man_rect_idle.centerx = newPlayer.playerX
            screen.blit(newPlayer.man_surface_idle,newPlayer.man_rect_idle)
            isCollided = newPlayer.checkCollision(newEnemy.enemies,newPlayer.man_rect_idle)

        elif newPlayer.isWalk:
            if newPlayer.char_walk_ind < newPlayer.total_images_walking - 1:
                newPlayer.char_walk_ind += 1
                if newPlayer.char_walk_ind == 1:
                    walk_sound.play()
            else:
                # walk_sound.play()
                newPlayer.char_walk_ind = 0
            newPlayer.man_surface_walk, newPlayer.man_rect_walk = newPlayer.animate_walk_char()
            newPlayer.man_rect_walk.centerx = newPlayer.playerX
            screen.blit(newPlayer.man_surface_walk, newPlayer.man_rect_walk)
            isCollided = newPlayer.checkCollision(newEnemy.enemies, newPlayer.man_rect_walk)

        elif newPlayer.isJump:
            if newPlayer.char_jump_ind < newPlayer.total_images_jumping - 1:
                newPlayer.char_jump_ind += 1
            else:
                newPlayer.char_jump_ind = 0
                newPlayer.isJump = False
                newPlayer.isIdle = True
            newPlayer.man_surface_Jump, newPlayer.man_rect_Jump = newPlayer.animate_jump_char()
            screen.blit(newPlayer.man_surface_Jump, newPlayer.man_rect_Jump)
            isCollided = newPlayer.checkCollision(newEnemy.enemies, newPlayer.man_rect_Jump)

        elif newPlayer.isSlide:
            if newPlayer.char_slide_ind < newPlayer.total_images_slide - 1:
                newPlayer.char_slide_ind += 1
            else:
                newPlayer.char_slide_ind = 0
                newPlayer.isSlide = False
                newPlayer.isIdle = True

            newPlayer.man_surface_sliding, newPlayer.man_rect_slide = newPlayer.animate_slide_char()
            screen.blit(newPlayer.man_surface_sliding,newPlayer.man_rect_slide)
            isCollided = newPlayer.checkCollision(newEnemy.enemies, newPlayer.man_rect_slide)

        newEnemy.enemies = newPlayer.move_enemies(newEnemy.enemies)
        newEnemy.draw_enemies(newEnemy.enemies)



        if newPlayer.isJump:
            newPlayer.man_rect_Jump.centery -= newPlayer.jump_height
        else:
            newPlayer.man_rect_Jump.centery = newPlayer.man_rect_walk.centery

        if newPlayer.playerX >= 790:
            newPlayer.playerX = 10

        if not isCollided:
            if newPlayer.health_index != len(newPlayer.heath_list):
                drawHealth(newPlayer.heath_list[newPlayer.health_index])
            else:
                newPlayer.isDie = True
        else:
            newPlayer.isHurt = True
            isCollided = False
            newPlayer.collision_count = 0
            if newPlayer.health_index == len(newPlayer.heath_list):
                newPlayer.isDie = True
            elif newPlayer.health_index < len(newPlayer.heath_list):
                newPlayer.health_index += 1

        display_score(score,'INGAME',high_score)
        display_knifeCount(knifeCount)

        if newPlayer.isHurt:
            newPlayer.isIdle = False
            newPlayer.isWalk = False
            newPlayer.isJump = False
            newPlayer.isSlide = False
            if newPlayer.char_hurt_ind < newPlayer.total_images_hurt - 1:
                newPlayer.char_hurt_ind += 1
            else:
                newPlayer.char_hurt_ind = 0
                player_hurt_sound.play()
                newPlayer.isHurt = False
                newPlayer.isIdle = True

            newPlayer.man_surface_hurted, newPlayer.man_rect_hurted = newPlayer.animate_hurt_char()
            screen.blit(newPlayer.man_surface_hurted, newPlayer.man_rect_hurted)

        if newPlayer.isDie:
            high_score = update_high_score(score, high_score)
            newPlayer.isIdle = False
            newPlayer.isWalk = False
            newPlayer.isJump = False
            newPlayer.isSlide = False
            newPlayer.isHurt = False
            if newPlayer.char_die_ind < newPlayer.total_images_die - 1:
                newPlayer.char_die_ind += 1
            else:
                newPlayer.char_die_ind = 0
                player_die_sound.play()
                game_active = False
            newPlayer.man_surface_dying, newPlayer.man_rect_die = newPlayer.animate_die_char()
            newPlayer.man_rect_die.centerx = newPlayer.playerX
            screen.blit(newPlayer.man_surface_dying, newPlayer.man_rect_die)

        if newPlayer.isThrown:
            newPlayer.isIdle = False
            newPlayer.isWalk = False
            newPlayer.isJump = False
            newPlayer.isSlide = False
            if newPlayer.char_throw_ind < newPlayer.total_images_throw - 1:
                newPlayer.char_throw_ind += 1
            else:
                newPlayer.char_throw_ind = 0
            newPlayer.man_surface_throwing,newPlayer.man_rect_throw = newPlayer.animate_throw_char()
            newPlayer.man_rect_throw.centerx = newPlayer.playerX
            screen.blit(newPlayer.man_surface_throwing,newPlayer.man_rect_throw)

        if newPlayer.knifesLocationX >= 820:
            newPlayer.knifeThrown = False
            newPlayer.knifesLocationX = newPlayer.man_rect_walk.centerx
            newPlayer.knifesLocationY = newPlayer.man_rect_walk.centery

        if newPlayer.knifeThrown:
            if newPlayer.knife_ind < newPlayer.total_knife - 1:
                newPlayer.knife_ind += 1
            else:
                newPlayer.knife_ind = 0
            newPlayer.knife_surface,newPlayer.knife_rect = newPlayer.animate_throw_knife()
            newPlayer.ThrowKnife(newPlayer.knifesLocationX,newPlayer.knifesLocationY)
            newPlayer.knifesLocationX += 10

    else:
        screen.blit(game_over_surface,(200,150))
        display_score(score,'GAMEOVER',high_score)
        if blinkCount < 12:
            restartText()
        blinkCount += 1
        if blinkCount > 24:
            blinkCount = 0
        display_knifeCount(knifeCount)
        newEnemy.enemies.clear()
        newPlayer.health_index = 0
        newPlayer.isDie = False
        newPlayer.isIdle = True
        groundX = 0
        ind = 0
        count = [5, 10, 20, 40]
        newPlayer.playerX = 160
        CollisionElement.clear()
        muteSound = True
        mixer.music.stop()

    screen.blit(game_coin_surface,game_coin_rect)
    screen.blit(knife_count_surface,knife_count_rect)

    clock.tick(27)
    pygame.display.update()

