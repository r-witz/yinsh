import pygame
import pygame.freetype
from pygame.locals import QUIT
import cv2
import sys
from src.resizing import Resizer
from src.settings import launch_volume_control
from src.game import Game
from src.utilities import Utilities 
import random
import json
import threading
from socket import gethostbyname, gethostname
from src.server import Server
from src.scan import scan_network

class Introduction: 

    def __init__(self) -> None:
        pygame.init()
        self.width, self.height = 1920, 1080
        self.assets = Resizer(self.width, self.height).load_assets()

        self.utilities = Utilities()
        self.draw_main_screen = self.utilities.draw_main_screen
        self.fade_function = self.utilities.fade_function
        self.check_quit_event = self.utilities.check_quit_event

        self.moglogo, self.moglogo_rect = self.assets['moglogo']
        self.smartgameslogo, self.smartgameslogo_rect = self.assets['smartgameslogo']
        self.yinshlogo, self.yinshlogo_rect = self.assets['yinshlogo']
        self.play_button, self.play_button_rect = self.assets['play_button']
        self.settings_button, self.settings_button_rect = self.assets['settings_button']
        self.quit_button, self.quit_button_rect = self.assets['quit_button']
        self.blitz_button, self.blitz_button_rect = self.assets['blitz_button']
        self.normal_button, self.normal_button_rect = self.assets['normal_button']
        self.botmode_button, self.botmode_button_rect = self.assets['botmode_button']
        self.online_button, self.online_button_rect = self.assets['online_button']
        self.local_button, self.local_button_rect = self.assets['local_button']
        self.host_button, self.host_button_rect = self.assets['host_button']
        self.join_button, self.join_button_rect = self.assets['join_button']
        self.resume_button, self.resume_button_rect = self.assets['resume_button']
        self.menu_button, self.menu_button_rect = self.assets['menu_button']
        self.replay_button, self.replay_button_rect = self.assets['replay_button']
        self.arrow, self.arrow_rect = self.assets['arrow']

        self.fade_surface = pygame.Surface((self.width, self.height))
        self.moglogo_faded = False
        self.smartgameslogo_faded = False

        self.hover_path = 'assets/audio/hover.mp3'
        self.hover_sound = pygame.mixer.Sound(self.hover_path)

        self.first_music = 'assets/audio/piano-loop-1.mp3'
        self.second_music = 'assets/audio/piano-loop-2.mp3'
        self.third_music = 'assets/audio/piano-loop-3.mp3'

        self.select_online_mode = Menus().select_online_mode
        self.victory_screen = Menus().victory_screen

        with open('settings.json', 'r') as f:
            settings = json.load(f)

        self.music_volume = settings['volumes']['music']
        self.sfx_volume = settings['volumes']['sfx']

    def intro(self) -> None:
        screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)        
        
        self.moglogo, self.moglogo_rect
        self.smartgameslogo, self.smartgameslogo_rect

        pygame.display.set_caption('Yinsh')
        running = True
        while running:
            if not self.moglogo_faded:
                self.fade_function(screen, self.moglogo, "out", 0.1) 
                self.moglogo_faded = True

            if self.moglogo_faded and not self.smartgameslogo_faded:
                self.fade_function(screen, self.smartgameslogo, "out", 0.1) 
                self.smartgameslogo_faded = True
            
            Menus.main_menu(self, screen, 'assets/graphics/background/menu.mp4', comeback_mainmenu=False)
            pygame.display.update()


class Menus:

    def __init__(self) -> None:
        pygame.init()
        self.width, self.height = 1920, 1080
        self.assets = Resizer(self.width, self.height).load_assets()

        self.utilities = Utilities()
        self.draw_main_screen = self.utilities.draw_main_screen
        self.fade_function = self.utilities.fade_function
        self.check_quit_event = self.utilities.check_quit_event

        self.moglogo, self.moglogo_rect = self.assets['moglogo']
        self.smartgameslogo, self.smartgameslogo_rect = self.assets['smartgameslogo']
        self.yinshlogo, self.yinshlogo_rect = self.assets['yinshlogo']
        self.play_button, self.play_button_rect = self.assets['play_button']
        self.settings_button, self.settings_button_rect = self.assets['settings_button']
        self.quit_button, self.quit_button_rect = self.assets['quit_button']
        self.blitz_button, self.blitz_button_rect = self.assets['blitz_button']
        self.normal_button, self.normal_button_rect = self.assets['normal_button']
        self.botmode_button, self.botmode_button_rect = self.assets['botmode_button']
        self.online_button, self.online_button_rect = self.assets['online_button']
        self.local_button, self.local_button_rect = self.assets['local_button']
        self.host_button, self.host_button_rect = self.assets['host_button']
        self.join_button, self.join_button_rect = self.assets['join_button']
        self.resume_button, self.resume_button_rect = self.assets['resume_button']
        self.menu_button, self.menu_button_rect = self.assets['menu_button']
        self.replay_button, self.replay_button_rect = self.assets['replay_button']
        self.arrow, self.arrow_rect = self.assets['arrow']

        self.frame = cv2.VideoCapture('assets/graphics/background/menu.mp4')

        self.hover_path = 'assets/audio/hover.mp3'
        self.hover_sound = pygame.mixer.Sound(self.hover_path)

        self.first_music = 'assets/audio/piano-loop-1.mp3'
        self.second_music = 'assets/audio/piano-loop-2.mp3'
        self.third_music = 'assets/audio/piano-loop-3.mp3'

        with open('settings.json', 'r') as f:
            settings = json.load(f)
        
        self.music_volume = settings['volumes']['music']
        self.sfx_volume = settings['volumes']['sfx']

    def random_music(self) -> None:
        music = random.choice([self.first_music, self.second_music, self.third_music])
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def main_menu(self, screen: pygame.Surface, video_path: str, comeback_mainmenu: bool) -> None:
        self.height, self.width
        fade_surface = pygame.Surface((self.width, self.height))
        fade_surface.fill((0, 0, 0))
        fade_alpha = 255
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1000 // int(fps) if fps != 0 else 100


        play_button_rect = self.play_button.get_rect(topleft=(225, 400))
        settings_button_rect = self.settings_button.get_rect(topleft=(225, 600))
        quit_button_rect = self.quit_button.get_rect(topleft=(225, 800))
        yinshlogo_rect = self.yinshlogo.get_rect(topleft=(370, 90))

        self.yinshlogo, self.yinshlogo_rect = self.yinshlogo, yinshlogo_rect
        self.play_button, self.play_button_rect = self.play_button, play_button_rect
        self.settings_button, self.settings_button_rect = self.settings_button, settings_button_rect
        self.quit_button, self.quit_button_rect = self.quit_button, quit_button_rect

        buttons = {'play_button': (self.play_button, play_button_rect),
                    'settings_button': (self.settings_button, settings_button_rect),
                    'quit_button': (self.quit_button, quit_button_rect)}

        hover_sound = pygame.mixer.Sound(self.hover_path)

        last_hovered_button = None
        Menus.random_music(self)

        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
                continue

            self.check_quit_event

            frame = cv2.resize(frame, (self.width, self.height))
            video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

            screen.blit(video_surf, (0, 0))
            
            mouse_pos = pygame.mouse.get_pos()
            hovered_button = None

            for button_name, (button, rect) in buttons.items():
                if rect.collidepoint(mouse_pos):
                    scaled_button = pygame.transform.scale(button, (int(rect.width * 1.1), int(rect.height * 1.1)))
                    scaled_rect = scaled_button.get_rect(center=rect.center)
                    screen.blit(scaled_button, scaled_rect)
                    hovered_button = button_name
                else:
                    screen.blit(button, rect)

            if hovered_button and hovered_button != last_hovered_button:
                hover_sound.set_volume(self.sfx_volume)
                hover_sound.play()            
                last_hovered_button = hovered_button
            if fade_alpha > 0 and comeback_mainmenu == False:
                self.fade_surface.set_alpha(fade_alpha)
                screen.blit(self.fade_surface, (0, 0))
                fade_alpha -= 5

            screen.blit(self.yinshlogo, self.yinshlogo_rect)
            pygame.display.update()
            pygame.time.delay(frame_delay)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        Menus.select_mode(self, screen, video_path, self.blitz_button, self.normal_button)
                    elif settings_button_rect.collidepoint(event.pos):
                        launch_volume_control(screen, (175, 350, 750, 500), 'settings.json', video_path)
                    elif quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            

    def select_mode(self, screen: pygame.Surface, video_path: str, blitz_button: pygame.Surface, normal_button: pygame.Surface) -> None:
        self.width, self.height
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            sys.exit()

        cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1000 // int(fps) if fps != 0 else 100

        self.yinshlogo, self.yinshlogo_rect
        self.arrow, self.arrow_rect

        self.yinshlogo_rect.topleft = (370, 90)
        self.blitz_button_rect = self.blitz_button.get_rect(topleft=(225, 400))
        self.normal_button_rect = self.normal_button.get_rect(topleft=(225, 600))

        self.arrow_rect.topleft = (10, 10) 

        hover_sound = pygame.mixer.Sound(self.hover_path)

        last_hovered_button = None

        while True:
            self.check_quit_event
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0) 
                continue

            frame = cv2.resize(frame, (self.width, self.height))
            video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

            screen.blit(video_surf, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            hovered_button = None
            buttons = {'blitz_button': (self.blitz_button, self.blitz_button_rect),
                    'normal_button': (self.normal_button, self.normal_button_rect)}

            for button_name, (button, rect) in buttons.items():
                if rect.collidepoint(mouse_pos):
                    scaled_button = pygame.transform.scale(button, (int(rect.width * 1.1), int(rect.height * 1.1)))
                    scaled_rect = scaled_button.get_rect(center=rect.center)
                    screen.blit(scaled_button, scaled_rect)
                    hovered_button = button_name
                else:
                    screen.blit(button, rect)

            if hovered_button and hovered_button != last_hovered_button:
                hover_sound.set_volume(self.sfx_volume)
                hover_sound.play()            
                last_hovered_button = hovered_button

            screen.blit(self.yinshlogo, self.yinshlogo_rect)
            screen.blit(self.arrow, self.arrow_rect)  
            
            pygame.display.update()
            pygame.time.delay(frame_delay)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.arrow_rect.collidepoint(event.pos): 
                        Menus.main_menu(self, screen, video_path, comeback_mainmenu=True)
                        return
                    elif self.blitz_button_rect.collidepoint(event.pos):  
                        mode_type = Menus.select_mode_type(self, screen, video_path, "Blitz") 
                        if mode_type: 
                            print(f"{mode_type} selected.")
                        return
                    elif self.normal_button_rect.collidepoint(event.pos): 
                        mode_type = Menus.select_mode_type(self, screen, video_path, "Normal")
                        if mode_type: 
                            print(f"{mode_type} selected.")
                        return

    def select_mode_type(self, screen: pygame.Surface, video_path: str, mode: str) -> str:
        self.width, self.height
        fade_surface = pygame.Surface((self.width, self.height))
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            sys.exit()

        cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1000 // int(fps) if fps != 0 else 100

        self.yinshlogo, self.yinshlogo_rect
        self.botmode_button, self.botmode_button_rect 
        self.online_button, self.online_button_rect
        self.local_button, self.local_button_rect
        self.arrow, self.arrow_rect
        

        self.yinshlogo_rect.topleft = (370, 90)
        botmode_button_rect = self.botmode_button.get_rect(topleft=(225, 400))
        online_button_rect = self.online_button.get_rect(topleft=(225, 600))
        local_button_rect = self.local_button.get_rect(topleft=(225, 800))
        self.arrow_rect.topleft = (10, 10)

        hover_sound = pygame.mixer.Sound(self.hover_path)
        last_hovered_button = None

        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
                continue

            frame = cv2.resize(frame, (self.width, self.height))
            video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

            screen.blit(video_surf, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            hovered_button = None
            buttons = {'botmode_button': (self.botmode_button, botmode_button_rect),
                    'online_button': (self.online_button, online_button_rect),
                    'local_button': (self.local_button, local_button_rect)}

            for button_name, (button, rect) in buttons.items():
                if rect.collidepoint(mouse_pos):
                    scaled_button = pygame.transform.scale(button, (int(rect.width * 1.1), int(rect.height * 1.1)))
                    scaled_rect = scaled_button.get_rect(center=rect.center)
                    screen.blit(scaled_button, scaled_rect)
                    hovered_button = button_name
                else:
                    screen.blit(button, rect)

            if hovered_button and hovered_button != last_hovered_button:
                hover_sound.set_volume(self.sfx_volume)
                hover_sound.play()            
                last_hovered_button = hovered_button

            screen.blit(self.yinshlogo, self.yinshlogo_rect)
            screen.blit(self.arrow, self.arrow_rect)  
            
            pygame.display.update()
            pygame.time.delay(frame_delay)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.arrow_rect.collidepoint(event.pos): 
                        Menus.select_mode(self, screen, video_path, self.blitz_button, self.normal_button)
                        return
                    elif botmode_button_rect.collidepoint(event.pos):
                        self.winner = Game("AI", mode).run(screen)
                        if self.winner != "Menu":
                            self.victory_screen(screen, video_path, self.winner, "AI", mode)
                        return
                    elif online_button_rect.collidepoint(event.pos):
                        self.winner = self.select_online_mode(screen, video_path, mode)
                    elif local_button_rect.collidepoint(event.pos):
                        self.winner = Game("Local", mode).run(screen)
                        if self.winner != "Menu":
                            self.victory_screen(screen, video_path, self.winner, "Local", mode)
                        return
                    
    def select_online_mode(self, screen: pygame.Surface, video_path: str, mode: str) -> str:
        self.width, self.height
        fade_surface = pygame.Surface((self.width, self.height))
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            sys.exit()

        cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1000 // int(fps) if fps != 0 else 100

        self.yinshlogo, self.yinshlogo_rect
        self.host_button, self.host_button_rect
        self.join_button, self.join_button_rect
        self.arrow, self.arrow_rect 

        self.yinshlogo_rect.topleft = (370, 90)
        self.host_button_rect = self.host_button.get_rect(topleft=(225, 400))
        self.join_button_rect = self.join_button.get_rect(topleft=(225, 600))
        self.arrow_rect.topleft = (10, 10)

        hover_sound = pygame.mixer.Sound(self.hover_path)
        last_hovered_button = None

        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
                continue

            frame = cv2.resize(frame, (self.width, self.height))
            video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

            screen.blit(video_surf, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            hovered_button = None
            buttons = {'host_button': (self.host_button, self.host_button_rect),
                    'join_button': (self.join_button, self.join_button_rect)}

            for button_name, (button, rect) in buttons.items():
                if rect.collidepoint(mouse_pos):
                    scaled_button = pygame.transform.scale(button, (int(rect.width * 1.1), int(rect.height * 1.1)))
                    scaled_rect = scaled_button.get_rect(center=rect.center)
                    screen.blit(scaled_button, scaled_rect)
                    hovered_button = button_name
                else:
                    screen.blit(button, rect)

            if hovered_button and hovered_button != last_hovered_button:
                hover_sound.set_volume(self.sfx_volume)
                hover_sound.play()            
                last_hovered_button = hovered_button

            screen.blit(self.yinshlogo, self.yinshlogo_rect)
            screen.blit(self.arrow, self.arrow_rect)

            pygame.display.update()
            pygame.time.delay(frame_delay)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.arrow_rect.collidepoint(event.pos): 
                        Menus.select_mode_type(self, screen, video_path, mode) 
                        return
                    elif self.host_button_rect.collidepoint(event.pos):
                        self.host_mode(screen, mode)
                        return
                    elif self.join_button_rect.collidepoint(event.pos):
                        self.join_mode(screen, video_path, mode)
                        return

    def draw_text(screen, text: str, rect: pygame.Rect, font: pygame.freetype.Font, color: tuple, center: bool = True):
        text_surf, text_rect = font.render(text, color)
        if center:
            text_rect.center = rect.center
        else:
            text_rect.midleft = rect.midleft
            text_rect.centery = rect.centery
        screen.blit(text_surf, text_rect)

    def host_mode(self, screen: pygame.Surface, mode: str) -> None:
        thread = threading.Thread(target=Server().start_server, args=()).start()
        Game("Online", mode, gethostbyname(gethostname())).run(screen)

    def join_mode(self, screen: pygame.Surface, video_path: str, mode: str) -> None:
        self.width, self.height = screen.get_size()
        fade_surface = pygame.Surface((self.width, self.height))
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            sys.exit()

        cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1000 // int(fps) if fps != 0 else 100

        self.yinshlogo, self.yinshlogo_rect 
        self.arrow, self.arrow_rect

        ip_addresses = scan_network()

        ip_font = pygame.font.Font(None, 36)
        ip_rect = pygame.Rect(175, 350, 750, 500)
        scroll_offset = 0

        col_headers = ["Gamehost (IP)"]
        col_width = ip_rect.width

        running = True
        while running:
            self.check_quit_event()
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
                continue

            frame = cv2.resize(frame, (self.width, self.height))
            video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

            screen.blit(video_surf, (0, 0))
            screen.blit(self.yinshlogo, self.yinshlogo_rect)
            screen.blit(self.arrow, self.arrow_rect)
            pygame.draw.rect(screen, (0, 0, 0), ip_rect)

            ip_surf = pygame.Surface((col_width, len(ip_addresses) * 40))
            ip_surf.fill((0, 0, 0))
            ip_surf.set_alpha(200)
            screen.blit(ip_surf, ip_rect.topleft)

            left_padding = 300
            vertical_padding = 20
            top_padding = 50

            cursor_over_ip = False

            for index, ip in enumerate(ip_addresses):
                ip_text = ip_font.render("Room " + str(index+1), True, (255, 255, 255))
                ip_pos = ip_rect.topleft[0] + left_padding, ip_rect.topleft[1] + top_padding + vertical_padding + index * 40 - scroll_offset
                screen.blit(ip_text, ip_pos)

                ip_text_rect = pygame.Rect(ip_pos, (col_width, 40))
                if ip_text_rect.collidepoint(pygame.mouse.get_pos()):
                    cursor_over_ip = True

            if cursor_over_ip:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.update()
            pygame.time.delay(frame_delay)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.arrow_rect.collidepoint(event.pos):
                        self.select_online_mode(screen, video_path, mode)
                    for index, ip in enumerate(ip_addresses):
                        ip_pos = ip_rect.topleft[0], ip_rect.topleft[1] + index * 40
                        ip_text_rect = pygame.Rect(ip_pos, (col_width, 40))
                        if ip_text_rect.collidepoint(event.pos):
                            Game("Online", mode, ip).run(screen)
                
    def victory_screen(self, screen: pygame.Surface, video_path: str, winner: str, gamemode: str, difficulty: str) -> None:
        self.width, self.height
        winner = winner[:-1] + " " + winner[-1] + " wins !"
        fade_surface = pygame.Surface((self.width, self.height))
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            sys.exit()

        cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1000 // int(fps) if fps != 0 else 100

        running = True
        while running:
            self.check_quit_event
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
                continue

            frame = cv2.resize(frame, (self.width, self.height))
            video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

            screen.blit(video_surf, (0, 0))

            self.replay_button, self.replay_button_rect
            self.menu_button, self.menu_button_rect
            font = pygame.font.Font("./assets/font/Daydream.ttf", 50)
            text_surf = font.render(winner, True, (249, 240, 194))

            self.replay_button, self.menu_button = (
                pygame.transform.scale(self.replay_button, (360, 120)),
                pygame.transform.scale(self.menu_button, (360, 120))
            )

            pygame.draw.rect(screen, (0, 0, 0), (500, 300, 900, 400), border_radius=30)
            pygame.draw.rect(screen, (249, 240, 194), (500, 300, 900, 400), 7, border_radius=30)
            self.replay_button_rect.topleft=(575, 500)
            self.menu_button_rect.topleft = (975, 500)
            text_rect = text_surf.get_rect(center=(950, 400))
            screen.blit(text_surf, text_rect)

            screen.blit(self.replay_button, self.replay_button_rect)
            screen.blit(self.menu_button, self.menu_button_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.replay_button_rect.collidepoint(event.pos):
                        winner = Game(gamemode, difficulty).run(screen)
                        if winner != "Menu":
                            self.victory_screen(screen, video_path, self.winner, gamemode, difficulty)
                        return
                    elif self.menu_button_rect.collidepoint(event.pos):
                        Menus.main_menu(self, screen, video_path, comeback_mainmenu=True)
                        return

            pygame.display.update()
            pygame.time.delay(frame_delay)