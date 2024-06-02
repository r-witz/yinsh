import pygame
import sys

class Utilities:
    
    def __init__(self) -> None:
        pass

    def draw_main_screen(self, screen, video_surf, yinshlogo, yinshlogo_rect):
        screen.blit(video_surf, (0, 0))
        screen.blit(yinshlogo, yinshlogo_rect)

    def fade_function(self, screen, image, direction, time):
        image_rect = image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        fade = pygame.Surface(screen.get_size())
        fade.fill((0, 0, 0))
        
        if direction == "in":       
            for opacity in range(0, 256):
                fade.set_alpha(opacity)
                screen.blit(image, image_rect)
                screen.blit(fade, (0, 0))
                pygame.display.update()
                pygame.time.delay(int(time * 1000 / 255))
        elif direction == "out":
            for opacity in range(255, -1, -1):
                fade.set_alpha(opacity)
                screen.blit(image, image_rect)
                screen.blit(fade, (0, 0))
                pygame.display.update()
                pygame.time.delay(int(time * 1000 / 255))

    def check_quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()