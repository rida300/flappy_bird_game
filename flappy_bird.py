import pygame
#import neat
import time
import os
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
	IMGS = BIRD_IMGS
	MAX_ROTATION = 25 #tilt the bird upwards/downwards by 25 degrees
	ROTATION_VELOCITY = 20
	ANIMATION_TIME = 5 # how long to show wach animation for

	def __init__(self,x,y):

		#initial position of flappy bird when game is first started
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0 # when we last jumped so we can calculate which direction to go next
		self.velocity = 0
		self.height = self.y
		self.img_count = 0 # tracks which image of flappy is currenly being dislayed
		self.img = self.IMGS[0] #first pic of fappy that is shown


	def jump(self):
		self.vel = -10.5 #for moving up, we need negatie velocity as the starting point is top left corner where the coordinates are (0,0)
		self.tick_count = 0
		self.height = self.y #where the bird starting juping FROM

	def move (self):
		self.tick_count +=1 # calculates how many times bird has moved since its last jump
		# 1 tick = 1 frame

		#displacement calculates how much the bird has moved up or down
		displacement = (self.velocity * self.tick_count)+ (1.5*self.tick_count**2)
		# distance = speed * time + (1.5*(time)^2)
		# Upon jump, within the 1st second:
		# (-10.5 * 1) +(1.5 * 1^2) = -10.5 + (1.5 * 1) = -10.5 + 1.5 = -9 
		# means bird moves 9 pixels upwards (hence the negative) in the first scond of jumping
		# 2nd second: (-10.5 * 2) +(1.5 * 2^2) = -21 + (1.5 * 4) = -21 + 6 = -15 IDK

		# for keeping bird in the frame, only allow it to move 16 pixels down max
		if d >= 16:
			d = 16

		#makes jump higher, random number
		if d <0:
			d -=2

		self.y = self.y +d

		#if bird is moving upwards (d<0) or there's still space to go up then tilt bird upwards
		if d<0 or self.y < self.height + 50:
			if self.tilt < seld.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION
		else: #tilt birds downwards
			if self.tilt > -90:
				self.tilt -= self.ROTATION_VELOCITY #determines how much to rotate the bird downwards
				#when bird goes up, we don't want it to look like it's upright but when it's down, we let it plummet hence more tilting

	def draw(self, window):
		#drawing the bird
		# 1. we need to keep track of how many ticks(seconds) we've shown the current bird image for
		self.img_count +=1		

		# ANIMATION_TIME = duration of time to display each bird image for
		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count == self.ANIMATION_TIME*4 +1: #reset
			self.img = self.IMGS[0]
			self.img_count = 0

		#case for nose-diving down when game is over
		if self.tilt <= -80:
			self.img = self.IMGS[1] #display the image where the wings are level and not flapping
			self.img_count = self.ANIMATION_TIME*2 # when we start the game again, show the pic where wings are flapping up using the if case above

		rotated_image = pygame.transform.rotate(self.img, self.tilt)
		#rootate the image around the center, not around the top left corner
		new_rectangle = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
		window.blit(rotated_image, new_rectangle.topleft)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)


def draw_window(window, bird):
	#draw background image, blit is a method that draws
	window.blit(BG_IMG, (0,0)) #top left position / where you want to draw the image

	bird.draw(window)
	pygame.display.update() # refresh the display

def main():
	#create bird with starting position (200,200)
	birdd = Bird(200,200)
	window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

	#setting up main loop to keep the game running
	run = True
	while run:
		for event in pygame.event.get(): #loops through user events (e.g.: mouse click)
			if event.type == pygame.QUIT: #clicking red X in the top right corner
				run = false

		draw_window(window, birdd)

	pygame.quit()
	quit()

#if __name__ == "__main__":
main()