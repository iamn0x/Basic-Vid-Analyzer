import pygame, sys
from PIL import Image

class MouseCropper():
    def __init__(self):
        self.left=0
        self.upper=0
        self.right=0
        self.lower=0
    
    def displayImage(self, screen, px, topleft, prior):
        # ensure that the rect always has positive width, height
        x, y = topleft
        width =  pygame.mouse.get_pos()[0] - topleft[0]
        height = pygame.mouse.get_pos()[1] - topleft[1]
        if width < 0:
            x += width
            width = abs(width)
        if height < 0:
            y += height
            height = abs(height)

        # eliminate redundant drawing cycles (when mouse isn't moving)
        current = x, y, width, height
        if not (width and height):
            return current
        if current == prior:
            return current

        # draw transparent box and blit it onto canvas
        screen.blit(px, px.get_rect())
        im = pygame.Surface((width, height))
        im.fill((128, 128, 128))
        pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
        im.set_alpha(128)
        screen.blit(im, (x, y))
        pygame.display.flip()

        # return current box extents
        return (x, y, width, height)



    def setup(self, path):
        px = pygame.image.load(path)
        im = Image.open(path)
        im_size = width, height = im.size
        screen = pygame.display.set_mode( im_size )
        screen.blit(px, px.get_rect())
        pygame.display.flip()
        return screen, px

    def mainLoop(self, screen, px):
        topleft = bottomright = prior = None
        n=0
        while n!=1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if not topleft:
                        topleft = event.pos
                    else:
                        bottomright = event.pos
                        n=1
            if topleft:
                prior = self.displayImage(screen, px, topleft, prior)
        return ( topleft + bottomright )

    def configure(self, inputLoc):
        pygame.init()
        
        screen, px = self.setup(inputLoc)
        self.left, self.upper, self.right, self.lower = self.mainLoop(screen, px)

        # ensure output rect always has positive width, height
        if self.right < self.left:
            self.left, self.right = self.right, self.left
        if self.lower < self.upper:
            self.lower, self.upper = self.upper, self.lower

        pygame.display.quit()
        
     


    def crop(self, inputLoc, saveFileName, left, upper, right, lower):
        self.left = left
        self.upper = upper
        self.right = right
        self.lower = lower

        if self.right < self.left:
            self.left, self.right = self.right, self.left
        if self.lower < self.upper:
            self.lower, self.upper = self.upper, self.lower
        
        im = Image.open(inputLoc)
        im = im.crop(( self.left, self.upper, self.right, self.lower))
        im.save(saveFileName)
