import pygame
import pygame_gui
import pygame.freetype
import json
import sys
import cv2
from src.resizing import Resizer
from src.utilities import Utilities

def load_assets():
    resizer = Resizer(1920, 1080)
    return resizer.load_assets()

class Settings:
    def __init__(self, screen, area_rect, settings_file, video_path):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.area_rect = area_rect
        self.settings_file = settings_file
        self.video_path = video_path
        self.initialize_pygame()
        self.current_mode = self.get_current_screen_mode()
        self.setup_ui()
        self.load_icons()
        self.initialize_volumes()
        self.settings_rect = pygame.Rect(area_rect) 

        self.assets = Resizer(self.width, self.height).load_assets()
        self.yinshlogo, self.yinshlogo_rect = self.assets['yinshlogo']

        self.check_quit_event = Utilities().check_quit_event

    def initialize_pygame(self):
        pygame.freetype.init()
        self.clock = pygame.time.Clock()
        self.FPS = 60

    def get_current_screen_mode(self):
        display_info = pygame.display.Info()
        if self.screen.get_flags() & pygame.FULLSCREEN:
            return 'Fullscreen'
        else:
            return 'Windowed Fullscreen'

    def setup_ui(self):
        self.manager = pygame_gui.UIManager(self.screen.get_size()) # what is this line doing? --> This line is creating a user interface manager to handle the UI elements.
        self.font = pygame.freetype.Font("./assets/font/04B.TTF", 36)
        dropdown_x = self.area_rect[0] + (self.area_rect[2] - 200) // 2 
        self.resolution_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['Windowed Fullscreen', 'Fullscreen'],
            starting_option=self.current_mode,
            relative_rect=pygame.Rect((dropdown_x, self.area_rect[1] + self.area_rect[3] - 80), (200, 30)), # what is this line doing? --> This line is creating a dropdown menu for the user to select the screen mode.
            manager=self.manager
        )

    def load_icons(self):
        assets = load_assets()
        self.sound_on_image = assets['sound_on'][0]
        self.sound_off_image = assets['sound_off'][0]
        self.cross_image = assets['red_cross'][0]
        self.icon_size = (40, 40)
        self.sound_on_image = pygame.transform.scale(self.sound_on_image, self.icon_size)
        self.sound_off_image = pygame.transform.scale(self.sound_off_image, self.icon_size)
        self.cross_image = pygame.transform.scale(self.cross_image, self.icon_size)  
        self.cross_rect = self.cross_image.get_rect(topright=(self.area_rect[0] + self.area_rect[2] - 10, self.area_rect[1] + 10)) 

    def initialize_volumes(self):
        self.volumes = self.load_settings().get('volumes', {'music': 0.5, 'sfx': 0.5})
        self.prev_volumes = self.volumes.copy()
        self.icon_states = {key: 'on' if self.volumes[key] > 0 else 'off' for key in self.volumes.keys()}
        self.slider_positions = {
            'music': (self.area_rect[0] + 75, self.area_rect[1] + 150),
            'sfx': (self.area_rect[0] + 75, self.area_rect[1] + 325)
        }

        self.slider_length = self.area_rect[2] - 250
        self.knob_radius = 10
        self.slider_color = (255, 255, 255)
        self.knob_color = (255, 0, 0)
        self.dragging_slider = None
        self.running = True

    def draw_slider(self, screen, pos, value, label, icon_state):
        start_pos = (pos[0], pos[1] + self.knob_radius)
        end_pos = (pos[0] + self.slider_length, pos[1] + self.knob_radius)
        pygame.draw.line(screen, self.slider_color, start_pos, end_pos, 2)
        knob_x = start_pos[0] + int(value * self.slider_length)
        pygame.draw.circle(screen, self.knob_color, (knob_x, start_pos[1]), self.knob_radius)
        self.font.render_to(screen, (pos[0], pos[1] - 40), label, (255, 255, 255))
        self.font.render_to(screen, (pos[0] + self.slider_length + 20, pos[1]), f"{int(value * 100)}%", (255, 255, 255))
        sound_image = self.sound_on_image if icon_state == 'on' else self.sound_off_image
        screen.blit(sound_image, (pos[0] - self.icon_size[0] - 10, pos[1] + self.knob_radius - self.icon_size[1] // 2))

    def toggle_volume(self, category):
        actions = {
            'music': lambda: self.update_volume('music'),
            'sfx': lambda: self.update_volume('sfx')
        }
        action = actions.get(category, lambda: None)
        action()

    def update_volume(self, category):
        update_actions = {
            'music': lambda: self.set_volume('music', pygame.mixer.music.set_volume),
            'sfx': lambda: self.set_volume('sfx', lambda v: pygame.mixer.set_num_channels(int(32 * v)))
        }
        action = update_actions.get(category, lambda: None)
        action()
        self.save_settings()

    def set_volume(self, category, set_func):
        if self.volumes[category] > 0:
            self.prev_volumes[category] = self.volumes[category]
            self.volumes[category] = 0
            self.icon_states[category] = 'off'
        else:
            self.volumes[category] = self.prev_volumes[category]
            self.icon_states[category] = 'on'
        set_func(self.volumes[category])
        self.save_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            default_settings = {'volumes': {'music': 0.5, 'sfx': 0.5}}
            with open(self.settings_file, 'w') as f:
                json.dump(default_settings, f)
            return default_settings

    def save_settings(self):
        settings = {'volumes': self.volumes}
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

    def handle_event(self, event):
        event_handlers = {
            pygame.QUIT: self.quit_game,
            pygame.MOUSEBUTTONDOWN: self.handle_mousebuttondown,
            pygame.MOUSEMOTION: self.handle_mousemotion,
            pygame.MOUSEBUTTONUP: self.handle_mousebuttonup,
            pygame.USEREVENT: self.handle_userevent
        }
        handler = event_handlers.get(event.type, lambda x: None)
        handler(event)

    def quit_game(self, event):
        self.running = False

    def handle_mousebuttondown(self, event):
        mouse_x, mouse_y = event.pos
        if self.cross_rect.collidepoint(mouse_x, mouse_y):  
            self.save_settings()
            self.running = False
            return

        for category, pos in self.slider_positions.items():
            if pos[0] <= mouse_x <= pos[0] + self.slider_length and pos[1] <= mouse_y <= pos[1] + 2 * self.knob_radius:
                self.dragging_slider = category
            if pos[0] - self.icon_size[0] - 10 <= mouse_x <= pos[0] - 10 and pos[1] <= mouse_y <= pos[1] + self.icon_size[1]:
                self.toggle_volume(category)

    def handle_mousemotion(self, event):
        if self.dragging_slider:
            mouse_x, _ = event.pos
            update_actions = {
                'music': lambda: self.update_slider('music', mouse_x),
                'sfx': lambda: self.update_slider('sfx', mouse_x)
            }
            action = update_actions.get(self.dragging_slider, lambda: None)
            action()

    def update_slider(self, category, mouse_x):
        self.volumes[category] = max(0, min(1, (mouse_x - self.slider_positions[category][0]) / self.slider_length))
        if category == 'music':
            pygame.mixer.music.set_volume(self.volumes[category])
        elif category == 'sfx':
            pygame.mixer.set_num_channels(int(32 * self.volumes[category]))
        self.icon_states[category] = 'off' if self.volumes[category] == 0 else 'on'
        self.save_settings()

    def handle_mousebuttonup(self, event):
        self.dragging_slider = None

    def handle_userevent(self, event):
        if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.resolution_dropdown:
            screen_modes = {
                'Fullscreen': pygame.FULLSCREEN | pygame.SCALED,
                'Windowed Fullscreen': pygame.SCALED
            }
            selected_mode = event.text
            if selected_mode != self.current_mode:
                self.current_mode = selected_mode
                screen_mode = screen_modes.get(selected_mode, pygame.FULLSCREEN | pygame.SCALED)
                self.screen = pygame.display.set_mode(self.screen.get_size(), screen_mode)

    def run(self, screen, video_path):
            self.width, self.height
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print("Error: Could not open video.")
                sys.exit()

            cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_delay = 1000 // int(fps) if fps != 0 else 100

            self.yinshlogo, self.yinshlogo_rect
            self.yinshlogo_rect.topleft = (370, 90)

            self.running = True
            while self.running:
                self.check_quit_event
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
                    continue

                frame = cv2.resize(frame, (self.width, self.height))
                video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

                screen.blit(video_surf, (0, 0))
                screen.blit(self.yinshlogo, self.yinshlogo_rect)            
                
                time_delta = self.clock.tick(self.FPS) / 1000.0

                for event in pygame.event.get():
                    self.handle_event(event)
                    self.manager.process_events(event)

                self.screen.fill((0, 0, 0), self.settings_rect)

                for category, pos in self.slider_positions.items():
                    self.draw_slider(self.screen, pos, self.volumes[category], f"{category.capitalize()} Volume", self.icon_states[category])
                    
                self.screen.blit(self.cross_image, self.cross_rect.topleft)  

                self.manager.update(time_delta)
                self.manager.draw_ui(self.screen)

                pygame.display.update()
                pygame.time.delay(frame_delay)

def launch_volume_control(screen, area_rect, settings_file, video_path):
    Settings(screen, area_rect, settings_file, video_path).run(screen, video_path)
