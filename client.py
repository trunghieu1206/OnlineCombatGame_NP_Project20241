import os
import sys
import math
import pygame
from pygame import SCRAP_TEXT
import socket

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.button import Button
class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('combat game')

        self.clock  = pygame.time.Clock()
        self.screen = pygame.display.set_mode((960,720))
        self.display =  pygame.Surface((640,480), pygame.SRCALPHA)
        self.display_2 =  pygame.Surface((640,480))
        self.horizontal_movement = [False,False]
        self.game_state = "menu"
        self.assets = {
                'player': load_image('entities/Samurai/Idle/Idle_1.png'),
                'background': load_images('background'),
                'player/idle': Animation(load_images('entities/Samurai/Idle'), img_dur=5, loop = True),
                'player/attack1': Animation(load_images('entities/Samurai/Attack1'), img_dur = 5, loop =False),
                'player/attack2': Animation(load_images('entities/Samurai/Attack2'),img_dur = 5, loop = False),
                'player/death':Animation(load_images('entities/Samurai/Death'),img_dur = 5, loop = False),
                'player/run':Animation(load_images('entities/Samurai/Run'),img_dur=5, loop = True),
                'player/jump':Animation(load_images('entities/Samurai/Jump'),img_dur= 5, loop=False)
        }
        self.background_offset_y = -80

        self.background =  pygame.Surface(self.assets['background'][0].get_size())
        count = 0
        for each in self.assets['background']:
            count+=1
            if count>=3:
                self.background.blit(each,(0,self.background_offset_y))
            else :
                self.background.blit(each, (0,0))
        
        self.player = Player(id=1, game  = self, pos = (0,280),size = (128,128))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    
    def serializePlayerInfo(self, player):
        """
        Concatenates all relevant information of a Player object into a string.

        Args:
            player: A Player object representing the player's data.

        Returns:
            A string containing player information in a well-formatted way.
        """

        # Extract relevant information from the Player object
        id = player.id
        entity_type = player.entity_type
        pos = player.pos
        flip = player.flip
        action = player.action

        # Format the information into a string with clear labels
        info_string = f"{id}|{entity_type}|{pos[0]}|{pos[1]}|{flip}|{action}"    # send the existed info according to format message of server

        return info_string

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("data/images/menuAssets/font.ttf", size)

    def menu(self):
        # self.screen = pygame.display.set_mode((1280, 720))
        BG = pygame.image.load('data/images/menuAssets/Background.png')
        while True:
            self.screen.blit(BG, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = self.get_font(75).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(480, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("data/images/menuAssets/Play Rect.png"), pos=(480, 250),
                                 text_input="PLAY", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("data/images/menuAssets/Quit Rect.png"), pos=(480, 400),
                                 text_input="QUIT", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.run()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()




    def run(self):
        message = "Start game"
        self.client_socket.sendto(message.encode("utf-8"), ("127.0.0.1", 5500))
        self.screen = pygame.display.set_mode((960, 720))
        while True:
            self.display.fill(color = (0,0,0,0))
            self.display_2.blit(pygame.transform.scale(self.background, self.display.get_size()), (0,0))
            message = self.serializePlayerInfo(self.player)
            self.client_socket.sendto(message.encode("utf-8"), ("127.0.0.1", 5500))

            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                     pygame.quit()
                     sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.horizontal_movement[0]= True
                    if event.key == pygame.K_RIGHT:
                        self.horizontal_movement[1]= True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.horizontal_movement[0]= False
                    if event.key == pygame.K_RIGHT:
                        self.horizontal_movement[1]= False
            
            if self.player.velocity[0]!=0:
                self.player.set_action('run')
            self.player.update((self.horizontal_movement[1]-self.horizontal_movement[0],0))
            self.player.render(self.display)

            self.display_2.blit(self.display, (0,0))
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), dest = (0,0))
            pygame.display.update()
            self.clock.tick(60)

Game().menu()
