import pygame

class Resizer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.assets_info = {
            'moglogo': {'path': 'assets/graphics/logo/MOG.png', 'type': 'moglogo'},
            'smartgameslogo': {'path': 'assets/graphics/logo/Smart-Games.png', 'type': 'smartgameslogo'},
            'arrow': {'path': 'assets/graphics/buttons/BACK.png', 'type': 'arrow'},
            'yinshlogo': {'path': 'assets/graphics/logo/Yinsh.png', 'type': 'yinshlogo'},
            'play_button': {'path': 'assets/graphics/buttons/PLAY.png', 'type': 'button'},
            'settings_button': {'path': 'assets/graphics/buttons/SETTINGS.png', 'type': 'button'},
            'quit_button': {'path': 'assets/graphics/buttons/QUIT.png', 'type': 'button'},
            'blitz_button': {'path': 'assets/graphics/buttons/BLITZ.png', 'type': 'button'},
            'normal_button': {'path': 'assets/graphics/buttons/NORMAL.png', 'type': 'button'},
            'botmode_button': {'path': 'assets/graphics/buttons/BOTMODE.png', 'type': 'button'},
            'online_button': {'path': 'assets/graphics/buttons/ONLINE.png', 'type': 'button'},
            'local_button': {'path': 'assets/graphics/buttons/LOCAL.png', 'type': 'button'},
            'resume_button': {'path': 'assets/graphics/buttons/RESUME.png', 'type': 'button'},
            'menu_button': {'path': 'assets/graphics/buttons/MENU.png', 'type': 'button'},
            'replay_button': {'path': 'assets/graphics/buttons/REPLAY.png', 'type': 'button'},
            'red_cross': {'path': 'assets/graphics/buttons/CROSS.png', 'type': 'sound_icon'},
            'sound_on': {'path': 'assets/graphics/buttons/SOUND_ON.png', 'type': 'sound_icon'},
            'sound_off': {'path': 'assets/graphics/buttons/SOUND_OFF.png', 'type': 'sound_icon'},
            'host_button': {'path': 'assets/graphics/buttons/HOST.png', 'type': 'button'},
            'join_button': {'path': 'assets/graphics/buttons/JOIN.png', 'type': 'button'},
        }

    def load_assets(self):
        loaded_assets = {}
        for asset_name, info in self.assets_info.items():
            scale = self.get_scale(info['type'])
            image = pygame.image.load(info['path'])
            image = pygame.transform.scale(image, scale)
            rect = image.get_rect(center=(self.width / 2, self.height / 2))
            loaded_assets[asset_name] = (image, rect)

        return loaded_assets

    def get_scale(self, asset_type):
        if asset_type == 'moglogo':
            return self.width // 3, self.height // 3
        elif asset_type == 'smartgameslogo':
            return self.width // 2, self.height // 4
        elif asset_type == 'yinshlogo':
            return self.width // 4.25, self.height // 8
        elif 'arrow' in asset_type:
            return self.width // 20, self.height // 12
        elif 'button' in asset_type:
            return self.width // 3.5, self.height // 7
        elif 'sound_icon' in asset_type:
            return self.width // 25, self.height // 15
        else:
            return self.width, self.height

