import pygame
from pygame.locals import *
import random

pygame.init()

fps = 60
clock = pygame.time.Clock()

screen_width = 864
screen_height = 847

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Santa')

#variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
cane_gap = 150
cane_frequency = 1500
last_cane = pygame.time.get_ticks() - cane_frequency
score = 0
pass_cane = False

#score 
font = pygame.font.SysFont('Bauhaus 93', 60)

blue = (51, 153, 255)

#load images
backround_image = pygame.image.load('img/bg.png')
ground_image = pygame.image.load('img/ground.png')
button_image = pygame.image.load('img/restart.png')

def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

def reset_game():
        cane_group.empty()
        flappy.rect.x = 200
        flappy.rect.y = 350
        score = 0
        return score


class Santa(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range(1, 4):
			img = pygame.image.load(f'img/pukki.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

	def update(self):

	        #gravity
                if flying == True:
                        self.vel += 0.5
                        if self.vel > 8:
                                self.vel = 8
                        if self.rect.bottom < 590:
                                self.rect.y += int(self.vel)

                        #jump
                        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                                self.clicked == True
                                self.vel = -10
                        if pygame.mouse.get_pressed()[0] == 0:
                                self.clicked == False

                        #handle the animation
                        self.counter += 1
                        flap_cooldown = 5

                        if self.counter > flap_cooldown:
                                self.counter = 0
                                self.index += 1
                                if self.index >= len(self.images):
                                        self.index = 0
                        self.image = self.images[self.index]

class Cane(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/cane.png')
		self.rect = self.image.get_rect()
		
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(cane_gap / 2)]
		if position == -1:
			self.rect.topleft = [x, y + int(cane_gap / 2)]

	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):

                action = False

                #restart position
                pos = pygame.mouse.get_pos()

                #check if mouse is hovering the button
                if self.rect.collidepoint(pos):
                        if pygame.mouse.get_pressed()[0] == 1:
                                action = True

                #restart button
                screen.blit(self.image, (self.rect.x, self.rect.y))
                
                return action

santa_group = pygame.sprite.Group()
cane_group = pygame.sprite.Group()

flappy = Santa(200, 350)

santa_group.add(flappy)

button = Button(370, 350, button_image)


run = True
while run:

        clock.tick(fps)

        #backround image
        screen.blit(backround_image, (0,0))

        #santa image
        santa_group.draw(screen)
        santa_group.update()

        #cane
        cane_group.draw(screen)
        
        #ground image
        screen.blit(ground_image, (ground_scroll, 595))

        #score
        if len(cane_group) > 0:
                if santa_group.sprites()[0].rect.left > cane_group.sprites()[0].rect.left\
                        and santa_group.sprites()[0].rect.right < cane_group.sprites()[0].rect.right\
                        and pass_cane == False:
                        pass_cane = True
                if pass_cane == True:
                      if santa_group.sprites()[0].rect.left > cane_group.sprites()[0].rect.right:
                                score += 1
                                pass_cane = False
        
        draw_text(str(score), font, blue, 432, 20 )
        
        #collision
        if pygame.sprite.groupcollide(santa_group, cane_group, False, False) or flappy.rect.top < 0:
                game_over = True

        #game over
        if flappy.rect.bottom > 590:
                game_over = True
                flying = False
        
        if game_over == False and flying == True:

                #generate canes
                time_now = pygame.time.get_ticks()
                if time_now - last_cane > cane_frequency:
                        cane_height = random.randint(-100, 100)
                        btm_cane = Cane(screen_width, 350 + cane_height, -1)
                        top_cane = Cane(screen_width, 350 + cane_height, 1)
                        cane_group.add(btm_cane)
                        cane_group.add(top_cane)
                        last_cane = time_now


                #ground scroll loop
                ground_scroll -= scroll_speed
                if abs(ground_scroll) > 95:
                        ground_scroll = 0

                cane_group.update()
        
        #game over and reset
        if game_over == True:
                if button.draw() == True:
                        game_over = False
                        score = reset_game()
        

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                        flying = True


        pygame.display.update()

pygame.quit()