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

        self.victory_screen = Menus().victory_screen

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

    def random_music(self) -> None:
        music = random.choice([self.first_music, self.second_music, self.third_music])
        pygame.mixer.music.load(music)
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        
        self.music_volume = settings['volumes']['music']
        self.sfx_volume = settings['volumes']['sfx']
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
                        online_mode = self.select_online_mode(self, screen, video_path, mode, "Online")
                        self.select_online_mode(self, screen, video_path, mode, online_mode)
                        return
                    elif local_button_rect.collidepoint(event.pos):
                        self.winner = Game("Local", mode).run(screen)
                        if self.winner != "Menu":
                            self.victory_screen(screen, video_path, self.winner, "Local", mode)
                        return
                    
    def select_online_mode(self, screen: pygame.Surface, video_path: str, mode: str, online_mode: str) -> str:
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
                        Menus.host_mode(self, screen, video_path, mode, online_mode)
                        return
                    elif self.join_button_rect.collidepoint(event.pos):
                        Menus.join_mode(self, screen, video_path, mode, online_mode)
                        return

    def draw_text(screen, text: str, rect: pygame.Rect, font: pygame.freetype.Font, color: tuple, center: bool = True):
        text_surf, text_rect = font.render(text, color)
        if center:
            text_rect.center = rect.center
        else:
            text_rect.midleft = rect.midleft
            text_rect.centery = rect.centery
        screen.blit(text_surf, text_rect)

    def host_mode(self, screen: pygame.Surface, video_path: str, mode: str, online_mode: str) -> None:
        width, height = 1920, 1080

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
        self.arrow_rect.topleft = (10, 10)

        pygame.freetype.init()
        font = pygame.freetype.SysFont(None, 24)

        input_box_room = pygame.Rect(250, 400, 500, 50)
        create_button = pygame.Rect(425, 600, 150, 50)
        start_button = pygame.Rect(425, 600, 150, 50)

        title_room_rect = pygame.Rect(250, 370, 500, 30)

        input_active_room = True
        input_text_room = ""
        room_name = ""
        show_teams = False

        running = True
        while running:
            self.check_quit_event
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
                continue

            frame = cv2.resize(frame, (width, height))
            video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

            screen.blit(video_surf, (0, 0))
            screen.blit(self.yinshlogo, self.yinshlogo_rect)
            screen.blit(self.arrow, self.arrow_rect)

            pygame.draw.rect(screen, (0, 0, 0), (175, 350, 750, 500))
            pygame.draw.rect(screen, (255, 255, 255), (175, 350, 750, 500), 2)

            if show_teams:
                Menus.draw_text(screen, f"Room: {room_name}", pygame.Rect(200, 400, 500, 50), font, (255, 255, 255), center=False)
            else:
                Menus.draw_text(screen, "Gameroom's Name", title_room_rect, font, (255, 255, 255), center=False)

                pygame.draw.rect(screen, (255, 255, 255), input_box_room, 2 if input_active_room else 1)
                Menus.draw_text(screen, input_text_room, input_box_room, font, (255, 255, 255), center=False)

                pygame.draw.rect(screen, (50, 50, 50), create_button)
                Menus.draw_text(screen, "Create", create_button, font, (255, 255, 255))

            pygame.display.update()
            pygame.time.delay(frame_delay)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if input_active_room:
                        if event.key == pygame.K_RETURN:
                            input_active_room = False
                        elif event.key == pygame.K_BACKSPACE:
                            input_text_room = input_text_room[:-1]
                        else:
                            input_text_room += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box_room.collidepoint(event.pos):
                        input_active_room = True
                    elif create_button.collidepoint(event.pos):
                        room_name = input_text_room
                        input_text_room = ""  
                        input_active_room = False
                        show_teams = True
                    elif self.arrow_rect.collidepoint(event.pos):
                        Menus.select_online_mode(self, screen, video_path, mode, online_mode)
                        return

    def join_mode(self, screen: pygame.Surface, video_path: str, mode: str, online_mode: str) -> None:
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
        self.arrow, self.arrow_rect

        self.yinshlogo_rect.topleft = (370, 90)
        self.arrow_rect.topleft = (10, 10)

        ip_addresses = [{
            "ip": f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "member": f"{random.randint(1, 2)}/2"
        } for _ in range(20)]

        ip_font = pygame.font.Font(None, 36)
        ip_rect = pygame.Rect(175, 350, 750, 500)
        scroll_offset = 0

        col_headers = ["Gamehost (IP)", "Member"]
        col_count = len(col_headers)
        col_width = ip_rect.width // col_count

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
            screen.blit(self.yinshlogo, self.yinshlogo_rect)
            screen.blit(self.arrow, self.arrow_rect)
            pygame.draw.rect(screen, (0, 0, 0), ip_rect)

            y = ip_rect.top + 10
            for i, header in enumerate(col_headers):
                header_surf = ip_font.render(header, True, (255, 255, 255))
                header_pos = header_surf.get_rect(topleft=(ip_rect.left + i * col_width + 10, y))
                screen.blit(header_surf, header_pos)

            y_start = y + ip_font.get_height() + 10 - scroll_offset
            for idx, details in enumerate(ip_addresses):
                y = y_start + idx * (ip_font.get_height() + 10)
                if ip_rect.top + ip_font.get_height() + 20 <= y <= ip_rect.bottom - (ip_font.get_height() + 10):
                    ip_pos = (ip_rect.left + 10, y)
                    member_pos = (ip_rect.left + 10 + col_width, y)

                    ip_surf = ip_font.render(details["ip"], True, (255, 255, 255))
                    screen.blit(ip_surf, ip_pos)

                    member_surf = ip_font.render(details["member"], True, (255, 255, 255))
                    screen.blit(member_surf, member_pos)

            content_height = len(ip_addresses) * (ip_font.get_height() + 10)
            if content_height > ip_rect.height:
                scrollbar_height = max(10, ip_rect.height * ip_rect.height // content_height)
                scrollbar_pos = min(ip_rect.bottom - scrollbar_height, ip_rect.top + scroll_offset * ip_rect.height // content_height)
                pygame.draw.rect(screen, (200, 200, 200), (ip_rect.right - 20, scrollbar_pos, 10, scrollbar_height))

            pygame.display.update()
            pygame.time.delay(frame_delay)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.arrow_rect.collidepoint(event.pos):
                        return
                elif event.type == pygame.MOUSEWHEEL:
                    scroll_offset -= event.y * 20
                    max_offset = max(0, content_height - ip_rect.height + 20)
                    scroll_offset = max(0, min(scroll_offset, max_offset))

                
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