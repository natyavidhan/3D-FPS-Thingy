from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import pyautogui
import random
import math
import json

app = Ursina()
Sky()
window.title = 'FPS'
window.fps_counter.enabled = True
window.borderless = False

latest_mouse_pos = pyautogui.position()
pyautogui.FAILSAFE = False
sensibility = 2.5
mouse.visible = True


floorcube = Entity(model="cube", color = color.lime, scale=(100, 1, 100), collider="box", position=(0, 10, 0), texture="grass",
	texture_scale=(100, 100))

playerController = FirstPersonController()
playerController.speed = 10
playerController.position = (0, 100, 0)

player = Entity(model="cube", scale=(0.5, 1, 0.5), texture="white_cube", texture_scale=(100, 100),
                position=playerController.position, rotation=playerController.rotation)

def update():
    global latest_mouse_pos
    global player
    if held_keys['f']:
        camera.fov += 1
    if held_keys['r']:
        camera.fov -= 1
    if playerController.y < 0:
        playerController.y = 0
    
    x, y, z = playerController.position
    rotX, rotY, rotZ = playerController.rotation
    player.position = Vec3(float(x), float(y)+0.5, float(z))
    player.rotation = Vec3(float(rotX), float(rotY), float(rotZ))

app.run()