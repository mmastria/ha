#!/usr/bin/python

import pygame
import pygame.camera
from PIL import Image

pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()
img = cam.get_image()
pygame.image.save(img,"/tmp/allskyfull.jpg")
img = Image.open("/tmp/allskyfull.jpg")
img = img.crop(( 86, 4, 550, 400))
img.save("/home/aagsolo/www/allsky.jpg")

