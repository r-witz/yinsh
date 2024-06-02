import pygame
import pygame.freetype
from pygame.locals import QUIT
import cv2
import sys
from resizing import Resizer
from settings import launch_volume_control
import random  

def load_assets():
    resizer = Resizer(1920, 1080)
    return resizer.load_assets()

def draw_main_screen(screen, video_surf, yinshlogo, yinshlogo_rect):
    screen.blit(video_surf, (0, 0))
    screen.blit(yinshlogo, yinshlogo_rect)

def fade_function(screen, image, image_rect, direction, speed=5):
    fade = pygame.Surface(screen.get_size())
    fade.fill((0, 0, 0))
    if direction == "in":       
        for opacity in range(255, -1, -speed):
            fade.set_alpha(opacity)
            screen.blit(image, image_rect)
            screen.blit(fade, (0, 0))
            pygame.display.update()
    elif direction == "out":
        for opacity in range(0, 256, speed):
            fade.set_alpha(opacity)
            screen.blit(image, image_rect)
            screen.blit(fade, (0, 0))
            pygame.display.update()

def check_quit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

def intro():
    pygame.init()
    width, height = 1920, 1080
    assets = load_assets()
    
    moglogo, moglogo_rect = assets['moglogo']
    smartgameslogo, smartgameslogo_rect = assets['smartgameslogo']

    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
    moglogo_faded = False
    smartgameslogo_faded = False
    pygame.display.set_caption('Yinsh')
    running = True

    while running:
        check_quit_event()
        if not moglogo_faded:
            fade_function(screen, moglogo, moglogo_rect, "out", 5)  
            moglogo_faded = True

        if moglogo_faded and not smartgameslogo_faded:
            pygame.time.delay(1500)
            fade_function(screen, smartgameslogo, smartgameslogo_rect, "in", 5)
            fade_function(screen, smartgameslogo, smartgameslogo_rect, "out", 5) 
            pygame.time.delay(1500)
            smartgameslogo_faded = True
        
        main_menu(screen, 'assets/graphics/background/menu.mp4', comeback_mainmenu=False, volume_state={'volumes': {'general': 0.5, 'music': 0.5, 'sfx': 0.5}})

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def main_menu(screen, video_path, comeback_mainmenu, volume_state):
    width, height = 1920, 1080
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    fade_alpha = 255
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1000 // int(fps) if fps != 0 else 100

    assets = load_assets()
    yinshlogo, yinshlogo_rect = assets['yinshlogo']
    play_button, play_button_rect = assets['play_button']
    settings_button, settings_button_rect = assets['settings_button']
    quit_button, quit_button_rect = assets['quit_button']   
    blitz_button, blitz_button_rect = assets['blitz_button']
    normal_button, normal_button_rect = assets['normal_button']

    play_button_rect = play_button.get_rect(topleft=(225, 400))
    settings_button_rect = settings_button.get_rect(topleft=(225, 600))
    quit_button_rect = quit_button.get_rect(topleft=(225, 800))
    yinshlogo_rect = yinshlogo.get_rect(topleft=(370, 90))

    buttons = {'play_button': (play_button, play_button_rect),
               'settings_button': (settings_button, settings_button_rect),
               'quit_button': (quit_button, quit_button_rect)}

    hover_sound = pygame.mixer.Sound('assets/audio/hover.mp3')

    last_hovered_button = None

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
            continue

        check_quit_event()

        frame = cv2.resize(frame, (width, height))
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
            hover_sound.play()
        last_hovered_button = hovered_button

        if fade_alpha > 0 and comeback_mainmenu == False:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha -= 5

        screen.blit(yinshlogo, yinshlogo_rect)
        pygame.display.update()
        pygame.time.delay(frame_delay)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    select_mode(screen, video_path, blitz_button, normal_button)
                elif settings_button_rect.collidepoint(event.pos):
                    settings_mode(screen, video_path, volume_state)
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def settings_mode(screen, video_path, volume_state):
    width, height = 1920, 1080
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1000 // int(fps) if fps != 0 else 100

    assets = load_assets()
    yinshlogo, yinshlogo_rect = assets['yinshlogo']
    yinshlogo_rect.topleft = (370, 90)

    running = True
    while running:
        check_quit_event()
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
            continue

        frame = cv2.resize(frame, (width, height))
        video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

        screen.blit(video_surf, (0, 0))
        screen.blit(yinshlogo, yinshlogo_rect)

        def draw_callback():
            draw_main_screen(screen, video_surf, yinshlogo, yinshlogo_rect)

        def return_to_menu_callback():
            print("Returning back to the menu")
            nonlocal running 
            running = False
            main_menu(screen, video_path, comeback_mainmenu=True, volume_state=volume_state)

        launch_volume_control(screen, (175, 350, 750, 500), draw_callback, return_to_menu_callback, volume_state)

        pygame.display.update()
        pygame.time.delay(frame_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def select_mode(screen, video_path, blitz_button, normal_button):
    width, height = 1920, 1080
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1000 // int(fps) if fps != 0 else 100

    assets = load_assets()
    yinshlogo, yinshlogo_rect = assets['yinshlogo'] 
    arrow, arrow_rect = assets['arrow'] 

    yinshlogo_rect.topleft = (370, 90)
    blitz_button_rect = blitz_button.get_rect(topleft=(225, 400))
    normal_button_rect = normal_button.get_rect(topleft=(225, 600))

    arrow_rect.topleft = (10, 10) 

    hover_sound = pygame.mixer.Sound('assets/audio/hover.mp3')

    last_hovered_button = None

    while True:
        check_quit_event()
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0) 
            continue

        frame = cv2.resize(frame, (width, height))
        video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

        screen.blit(video_surf, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        hovered_button = None
        buttons = {'blitz_button': (blitz_button, blitz_button_rect),
                   'normal_button': (normal_button, normal_button_rect)}

        for button_name, (button, rect) in buttons.items():
            if rect.collidepoint(mouse_pos):
                scaled_button = pygame.transform.scale(button, (int(rect.width * 1.1), int(rect.height * 1.1)))
                scaled_rect = scaled_button.get_rect(center=rect.center)
                screen.blit(scaled_button, scaled_rect)
                hovered_button = button_name
            else:
                screen.blit(button, rect)

        if hovered_button and hovered_button != last_hovered_button:
            hover_sound.play()
        last_hovered_button = hovered_button

        screen.blit(yinshlogo, yinshlogo_rect)
        screen.blit(arrow, arrow_rect)  
        
        pygame.display.update()
        pygame.time.delay(frame_delay)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arrow_rect.collidepoint(event.pos): 
                    return
                elif blitz_button_rect.collidepoint(event.pos):  
                    mode_type = select_mode_type(screen, video_path, "Blitz") 
                    if mode_type: 
                        print(f"{mode_type} selected.")
                    return
                elif normal_button_rect.collidepoint(event.pos): 
                    mode_type = select_mode_type(screen, video_path, "Normal") 
                    if mode_type: 
                        print(f"{mode_type} selected.")
                    return

def select_mode_type(screen, video_path, mode):
    width, height = 1920, 1080
    fade_surface = pygame.Surface((width, height))
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1000 // int(fps) if fps != 0 else 100

    assets = load_assets()
    yinshlogo, yinshlogo_rect = assets['yinshlogo']  
    arrow, arrow_rect = assets['arrow']  

    yinshlogo_rect.topleft = (370, 90)

    botmode_button, botmode_button_rect = assets['botmode_button']
    online_button, online_button_rect = assets['online_button']
    local_button, local_button_rect = assets['local_button']
    blitz_button, normal_button = assets['blitz_button'], assets['normal_button']

    botmode_button_rect = botmode_button.get_rect(topleft=(225, 400))
    online_button_rect = online_button.get_rect(topleft=(225, 600))
    local_button_rect = local_button.get_rect(topleft=(225, 800))

    arrow_rect.topleft = (10, 10)

    hover_sound = pygame.mixer.Sound('assets/audio/hover.mp3')

    last_hovered_button = None

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
            continue

        frame = cv2.resize(frame, (width, height))
        video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

        screen.blit(video_surf, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        hovered_button = None
        buttons = {'botmode_button': (botmode_button, botmode_button_rect),
                   'online_button': (online_button, online_button_rect),
                   'local_button': (local_button, local_button_rect)}

        for button_name, (button, rect) in buttons.items():
            if rect.collidepoint(mouse_pos):
                scaled_button = pygame.transform.scale(button, (int(rect.width * 1.1), int(rect.height * 1.1)))
                scaled_rect = scaled_button.get_rect(center=rect.center)
                screen.blit(scaled_button, scaled_rect)
                hovered_button = button_name
            else:
                screen.blit(button, rect)

        if hovered_button and hovered_button != last_hovered_button:
            hover_sound.play()
        last_hovered_button = hovered_button

        screen.blit(yinshlogo, yinshlogo_rect)
        screen.blit(arrow, arrow_rect)  
        
        pygame.display.update()
        pygame.time.delay(frame_delay)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arrow_rect.collidepoint(event.pos): 
                    select_mode(screen, video_path, assets['blitz_button'][0], assets['normal_button'][0]) 
                    return
                elif botmode_button_rect.collidepoint(event.pos):
                    online_mode = select_online_mode(screen, video_path, mode, "Botmode")                    
                    return
                elif online_button_rect.collidepoint(event.pos):
                    fade_function(screen, fade_surface, None, "out", 5)  
                    return
                elif local_button_rect.collidepoint(event.pos):
                    fade_function(screen, fade_surface, None, "out", 5)  
                    return
                
def select_online_mode(screen, video_path, mode, online_mode):
    width, height = 1920, 1080
    fade_surface = pygame.Surface((width, height))
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1000 // int(fps) if fps != 0 else 100

    assets = load_assets()
    yinshlogo, yinshlogo_rect = assets['yinshlogo']  
    arrow, arrow_rect = assets['arrow']  

    host_button, host_button_rect = assets['host_button']
    join_button, join_button_rect = assets['join_button']

    yinshlogo_rect.topleft = (370, 90)

    host_button_rect = host_button.get_rect(topleft=(225, 400))
    join_button_rect = join_button.get_rect(topleft=(225, 600))

    arrow_rect.topleft = (10, 10)

    hover_sound = pygame.mixer.Sound('assets/audio/hover.mp3')

    last_hovered_button = None

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
            continue

        frame = cv2.resize(frame, (width, height))
        video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

        screen.blit(video_surf, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        hovered_button = None
        buttons = {'host_button': (host_button, host_button_rect),
                   'join_button': (join_button, join_button_rect)}

        for button_name, (button, rect) in buttons.items():
            if rect.collidepoint(mouse_pos):
                scaled_button = pygame.transform.scale(button, (int(rect.width * 1.1), int(rect.height * 1.1)))
                scaled_rect = scaled_button.get_rect(center=rect.center)
                screen.blit(scaled_button, scaled_rect)
                hovered_button = button_name
            else:
                screen.blit(button, rect)

        if hovered_button and hovered_button != last_hovered_button:
            hover_sound.play()
        last_hovered_button = hovered_button

        screen.blit(yinshlogo, yinshlogo_rect)
        screen.blit(arrow, arrow_rect)

        pygame.display.update()
        pygame.time.delay(frame_delay)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arrow_rect.collidepoint(event.pos): 
                    select_mode_type(screen, video_path, mode) 
                    return
                elif host_button_rect.collidepoint(event.pos):
                    host_mode(screen, video_path, mode, online_mode)
                    return
                elif join_button_rect.collidepoint(event.pos):
                    join_mode(screen, video_path, mode, online_mode)
                    return



def draw_text(screen, text, rect, font, color, center=True):
    text_surf, text_rect = font.render(text, color)
    if center:
        text_rect.center = rect.center
    else:
        text_rect.midleft = rect.midleft
        text_rect.centery = rect.centery
    screen.blit(text_surf, text_rect)

def host_mode(screen, video_path, mode, online_mode):
    width, height = 1920, 1080

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1000 // int(fps) if fps != 0 else 100

    assets = load_assets()
    yinshlogo, yinshlogo_rect = assets['yinshlogo']
    arrow, arrow_rect = assets['arrow']
    yinshlogo_rect.topleft = (370, 90)
    arrow_rect.topleft = (10, 10)

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
        check_quit_event()
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
            continue

        frame = cv2.resize(frame, (width, height))
        video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

        screen.blit(video_surf, (0, 0))
        screen.blit(yinshlogo, yinshlogo_rect)
        screen.blit(arrow, arrow_rect)

        pygame.draw.rect(screen, (0, 0, 0), (175, 350, 750, 500))
        pygame.draw.rect(screen, (255, 255, 255), (175, 350, 750, 500), 2)

        if show_teams:
            draw_text(screen, f"Room: {room_name}", pygame.Rect(200, 400, 500, 50), font, (255, 255, 255), center=False)
        else:
            draw_text(screen, "Gameroom's Name", title_room_rect, font, (255, 255, 255), center=False)

            pygame.draw.rect(screen, (255, 255, 255), input_box_room, 2 if input_active_room else 1)
            draw_text(screen, input_text_room, input_box_room, font, (255, 255, 255), center=False)

            pygame.draw.rect(screen, (50, 50, 50), create_button)
            draw_text(screen, "Create", create_button, font, (255, 255, 255))

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
                elif arrow_rect.collidepoint(event.pos):
                    select_online_mode(screen, video_path, mode, online_mode)
                    return

def join_mode(screen, video_path, mode, online_mode):
    width, height = 1920, 1080
    fade_surface = pygame.Surface((width, height))
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1000 // int(fps) if fps != 0 else 100

    assets = load_assets()
    yinshlogo, yinshlogo_rect = assets['yinshlogo']
    arrow, arrow_rect = assets['arrow']

    yinshlogo_rect.topleft = (370, 90)
    arrow_rect.topleft = (10, 10)

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

    # Main loop
    running = True
    while running:
        check_quit_event()
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
            continue

        frame = cv2.resize(frame, (width, height))
        video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

        screen.blit(video_surf, (0, 0))
        screen.blit(yinshlogo, yinshlogo_rect)
        screen.blit(arrow, arrow_rect)
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
                if arrow_rect.collidepoint(event.pos):
                    return
            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * 20
                max_offset = max(0, content_height - ip_rect.height + 20)
                scroll_offset = max(0, min(scroll_offset, max_offset))


def tab_menu(screen, video_path, tabs, tab_names, tab_contents, tab_rects, tab_font):
    width, height = 1920, 1080
    fade_surface = pygame.Surface((width, height))
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1000 // int(fps) if fps != 0 else 100

    volume_state = {'volumes': {'general': 0.5, 'music': 0.5, 'sfx': 0.5}}

    running = True
    while running:
        check_quit_event()
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
            continue

        frame = cv2.resize(frame, (width, height))
        video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

        screen.blit(video_surf, (0, 0))

        settings_button, settings_button_rect = load_assets()['settings_button']
        menu_button, menu_button_rect = load_assets()['menu_button']

        resume_button, resume_button_rect = load_assets()['resume_button']
        resume_button, settings_button, menu_button = (
            pygame.transform.scale(resume_button, (400, 125)), 
            pygame.transform.scale(settings_button, (400, 125)), 
            pygame.transform.scale(menu_button, (400, 125))
        )

        resume_button_rect.topleft=(755, 340) 
        settings_button_rect.topleft = (755, 490)
        menu_button_rect.topleft = (755, 635)

        pygame.draw.rect(screen, (0, 0, 0), (700, 300, 500, 505), border_radius=30)
        pygame.draw.rect(screen, (249, 240, 194), (700, 300, 500, 505), 7, border_radius=30)
        screen.blit(resume_button, resume_button_rect)
        screen.blit(settings_button, settings_button_rect)
        screen.blit(menu_button, menu_button_rect)

        pygame.display.update()
        pygame.time.delay(frame_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(event.pos):
                    return
                elif settings_button_rect.collidepoint(event.pos):
                    return
                elif menu_button_rect.collidepoint(event.pos):
                    return
                
def victory_screen(screen, video_path, winner):
    width, height = 1920, 1080
    fade_surface = pygame.Surface((width, height))
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1000 // int(fps) if fps != 0 else 100

    running = True
    while running:
        check_quit_event()
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
            continue

        frame = cv2.resize(frame, (width, height))
        video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

        screen.blit(video_surf, (0, 0))

        replay_button, replay_button_rect = load_assets()['replay_button']
        menu_button, menu_button_rect = load_assets()['menu_button']

        replay_button, menu_button = (
            pygame.transform.scale(replay_button, (360, 120)),
            pygame.transform.scale(menu_button, (360, 120))
        )


        pygame.draw.rect(screen, (0, 0, 0), (500, 300, 900, 400), border_radius=30)
        pygame.draw.rect(screen, (249, 240, 194), (500, 300, 900, 400), 7, border_radius=30)
        replay_button_rect.topleft=(575, 500)
        menu_button_rect.topleft = (975, 500)

        font = pygame.font.Font("./assets/font/Daydream.ttf", 50)
        text_surf = font.render(winner, True, (249, 240, 194))
        text_rect = text_surf.get_rect(center=(950, 400))
        screen.blit(text_surf, text_rect)

        screen.blit(replay_button, replay_button_rect)
        screen.blit(menu_button, menu_button_rect)


        pygame.display.update()
        pygame.time.delay(frame_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption('Yinsh')
    pygame.font.init()
    join_mode(screen, 'assets/graphics/background/menu.mp4', "Normal", "Botmode")