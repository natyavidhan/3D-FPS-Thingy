from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import pyautogui
import random
import math
import socket
import json


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.connect()

    def connect(self):
        self.client.connect(self.addr)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            response = self.client.recv(2048).decode()
            return response
        except socket.error as e:
            return str(e)

net = Network()

app = Ursina()
Sky()
window.title = '3D FPS Thingy'
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
playerController.position = (0, 35, 0)

players = {}
playerChar = Entity(model="cube", scale=(0.5, 1, 0.5), texture="white_cube", texture_scale=(100, 100),
                position=playerController.position, rotation=playerController.rotation)

def update():
    global latest_mouse_pos
    global players, playerChar
    if held_keys['f']:
        camera.fov += 1
    if held_keys['r']:
        camera.fov -= 1
    if playerController.y < 0:
        playerController.y = 35
    if playerController.x > 49:
        playerController.x = 49
    if playerController.x < -49:
        playerController.x = -49
    if playerController.z > 49:
        playerController.z = 49
    if playerController.z < -49:
        playerController.z = -49
    
    playerData = [[], []]
    for i in range(3):
        playerData[0].append(round(list(playerController.position)[i], 4))
        playerData[1].append(round(list(playerController.rotation)[i], 4))

    net.send("update||" + json.dumps(playerData))

    allPlayers = json.loads(net.send("get||all"))
    user = json.loads(net.send("get||self"))
    for addr in allPlayers:
        if addr != user[2]:
            player = allPlayers[addr]
            pos = Vec3(player[0][0], player[0][1], player[0][2])
            rot = Vec3(player[1][0], player[1][1], player[1][2])

            if addr not in players:
                players[addr] = Entity(model="cube", color = color.red, scale=(1, 1, 1), collider="box", position=pos, rotation=rot)
            else:
                players[addr].position = pos
                players[addr].rotation = rot

    

    x, y, z = playerController.position
    rotX, rotY, rotZ = playerController.rotation
    playerChar.position = Vec3(float(x), float(y)+0.5, float(z))
    playerChar.rotation = Vec3(float(rotX), float(rotY), float(rotZ))

app.run()