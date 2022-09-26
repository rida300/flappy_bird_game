import pygame
# import neat
import time
import os
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # tilt the bird upwards/downwards by 25 degrees
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5  # how long to show wach animation for

    def __init__(self, x, y):

        # initial position of flappy bird when game is first started
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0  # when we last jumped so we can calculate which direction to go next
        self.velocity = 0
        self.height = self.y
        self.img_count = 0  # tracks which image of flappy is currenly being dislayed
        self.img = self.IMGS[0]  # first pic of fappy that is shown

    def jump(self):
        # for moving up, we need negatie velocity as the starting point is top left corner where the coordinates are (0,0)
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y  # where the bird starting juping FROM

    def move(self):
        self.tick_count += 1  # calculates how many times bird has moved since its last jump
        # 1 tick = 1 frame

        # displacement calculates how much the bird has moved up or down
        displacement = (self.velocity * self.tick_count) + \
            (1.5*self.tick_count**2)
        # distance = speed * time + (1.5*(time)^2)
        # Upon jump, within the 1st second:
        # (-10.5 * 1) +(1.5 * 1^2) = -10.5 + (1.5 * 1) = -10.5 + 1.5 = -9
        # means bird moves 9 pixels upwards (hence the negative) in the first scond of jumping
        # 2nd second: (-10.5 * 2) +(1.5 * 2^2) = -21 + (1.5 * 4) = -21 + 6 = -15 IDK

        # for keeping bird in the frame, only allow it to move 16 pixels down max
        if d >= 16:
            d = 16

        # makes jump higher, random number
        if d < 0:
            d -= 2

        self.y = self.y + d

        # if bird is moving upwards (d<0) or there's still space to go up then tilt bird upwards
        if d < 0 or self.y < self.height + 50:
            if self.tilt < seld.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt birds downwards
            if self.tilt > -90:
                # determines how much to rotate the bird downwards
                self.tilt -= self.ROTATION_VELOCITY
                # when bird goes up, we don't want it to look like it's upright but when it's down, we let it plummet hence more tilting

    def draw(self, window):
        # drawing the bird
        # 1. we need to keep track of how many ticks(seconds) we've shown the current bird image for
        self.img_count += 1

        # ANIMATION_TIME = duration of time to display each bird image for
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:  # reset
            self.img = self.IMGS[0]
            self.img_count = 0

        # case for nose-diving down when game is over
        if self.tilt <= -80:
            # display the image where the wings are level and not flapping
            self.img = self.IMGS[1]
            # when we start the game again, show the pic where wings are flapping up using the if case above
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # rootate the image around the center, not around the top left corner
        new_rectangle = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        # returns a 2D array of all the pixels an image is occcupying
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200  # space between top and bottom pipes
    PIPE_VELOCITY = 5  # how fast the pipes move, pipes are moving, birds aren't

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0  # where to draw the top of our pipe
        self.bottom == 0  # where to draw bottom of pipe
        self.PIPE_TOP = pygame.transform.flip(
            PIPE_IMG, False, True)  # pipe top /UPSIDE_DOWN
        self.PIPE_BOTTOM = PIPE_IMG  # pipe bottom /UPRIGHT

        self.passed = False  # indicates whether bird has already passed by this pipe
        self.set_height()

    def self_height(self):
        # get random number for what the pipe heght should be
        self.height = random.randrange(0, 450)
        self.top = self.height - self.PIPE_TOP
        self.bottom = self.height + self.GAP

        def move(self):
            self.x -= self.PIPE_VELOCITY

        def draw(self, win):  # draws both top and bottom pipe
            win.blit(self.PIPE_TOP, (self.x, self.top))
            win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

        def collide(self, bird):
            bird_mask = bird.get_mask()

            # mask for top pipe (the box around top pipe's pixels)
            top_mask = pygame.mask.from_surface(self.PIPE_TOP)

            # mask for bottom pipe (the box around bottom pipe's pixels)
            bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

            # calculate how far away these masks are from each other
            # offset from bird to top pipe (distance between top pipe and bird)
            top_offset = (self.x - bird.x, self.top - round(bird.y))

            # offset from bird to bottom pipe (distance between bottom pipe and bird)
            bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

            # point of overlap between the bird mask and the bottom pipe
            b_point = bird_mask.overlap(bottom_mask, bottom_offset)

            # point of overlap between the bird mask and the top pipe
            t_point = bird_mask.overlap(top_mask, top_offset)

            if t_point or b_point:
                return True
            return False


class Base:
    # there's 2 base images that we're using.
    # 1. Move the first image to the left as the game goes on
    # 2. Move the second image to the left as well
    # 3. As soon as the first image is out of frame (too far to the left),
    #    we re-draw the image to the end of the second image and second image becomes the first image

    VEL = 5  # Must be same as Pipe or it'll look like they're moving at 2 different speeds
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # moving image to the right once they're out of frame
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(window, bird):
    # draw background image, blit is a method that draws
    # top left position / where you want to draw the image
    window.blit(BG_IMG, (0, 0))

    bird.draw(window)
    pygame.display.update()  # refresh the display


def main():
    # create bird with starting position (200,200)
    birdd = Bird(200, 200)
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # setting up main loop to keep the game running
    run = True
    while run:
        for event in pygame.event.get():  # loops through user events (e.g.: mouse click)
            if event.type == pygame.QUIT:  # clicking red X in the top right corner
                run = false

        draw_window(window, birdd)

    pygame.quit()
    quit()


# if __name__ == "__main__":
main()
