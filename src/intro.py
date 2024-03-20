import pygame
from pygame.locals import QUIT
import sys 
import cv2

def get_screen_size():
    pygame.init()
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h
    return width, height

def fade_in(screen, image, image_rect):
    fade = pygame.Surface(screen.get_size())
    fade.fill((0, 0, 0))
    opacity = 255 
    for r in range(0, 255):  
        fade.set_alpha(opacity)
        screen.blit(image, image_rect)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        opacity -= 1

def fade_out(screen, image, image_rect):
    fade = pygame.Surface(screen.get_size())
    fade.fill((0, 0, 0))
    opacity = 0 
    for r in range(0, 255):
        fade.set_alpha(opacity)
        screen.blit(image, image_rect)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        opacity += 1

def main():
    pygame.init()

    width, height = get_screen_size()
    moglogo = pygame.image.load('assets/moglogo.png')
    moglogo = pygame.transform.scale(moglogo, (width//3, height//3))
    moglogo_rect = moglogo.get_rect(center=(width/2, height/2))
    
    smartgameslogo = pygame.image.load('assets/smartgames.png')
    smartgameslogo = pygame.transform.scale(smartgameslogo, (width//2, height//4))
    smartgameslogo_rect = smartgameslogo.get_rect(center=(width/2, height/2))

    cap = cv2.VideoCapture('assets/background.mp4')
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit()
    
    # Video loop
    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED)
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    fade_alpha = 255
    moglogo_faded = False
    smartgameslogo_faded = False
    pygame.display.set_caption('Yinsh')
    running = True

    # Video frame rate management
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        frame_delay = 100  # Prevents from crashing if fps = 0 
    else:
        frame_delay = 1000 // int(fps)
    
    while running:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
            
        if not moglogo_faded:
            fade_out(screen, moglogo, moglogo_rect)
            moglogo_faded = True

        if moglogo_faded and not smartgameslogo_faded:
            pygame.time.delay(1500)
            fade_in(screen, smartgameslogo, smartgameslogo_rect)
            fade_out(screen, smartgameslogo, smartgameslogo_rect)
            pygame.time.delay(1500)
            smartgameslogo_faded = True
        
        frame = cv2.resize(frame, (width, height))
        video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")
        
        screen.blit(video_surf, (0, 0))
        
        if fade_alpha > 0:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha -= 5 

        pygame.display.update()
        pygame.time.delay(frame_delay) 

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

    cap.release()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
