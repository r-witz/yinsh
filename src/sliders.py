import pygame
import sys

class DraggableBar:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (150, 150, 150)
        self.BLUE = (0, 0, 255)
        self.width = 800
        self.height = 600

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Draggable Bar")

        self.rect_width = 600
        self.rect_height = 20
        self.bar_length = 20
        self.bar_thickness = self.rect_height * 2

        self.rect_x = (self.width - self.rect_width) // 2
        self.rect_y = (self.height - self.rect_height) // 2
        self.bar_x = self.rect_x + (self.rect_width - self.bar_length) // 2
        self.bar_y = self.rect_y + (self.rect_height - self.bar_thickness) // 2
        self.initial_bar_y = self.bar_y

        self.button_radius = 25
        self.button_padding = 10
        self.button_x = self.rect_x - self.button_radius - self.button_padding
        self.button_y = self.rect_y + (self.rect_height - self.button_radius) // 2
        self.mute_button_clicked = False

        self.dragging = False
        self.offset_x = 0
        self.volume = 0.5
        self.prev_volume = self.volume
        pygame.mixer.music.set_volume(self.volume)

    def check_mute_button(self, mouse_x, mouse_y):
        if (
            self.button_x - self.button_radius < mouse_x < self.button_x + self.button_radius and
            self.button_y - self.button_radius < mouse_y < self.button_y + self.button_radius
        ):
            if self.mute_button_clicked:
                self.mute_button_clicked = False
                self.volume = (self.bar_x - self.rect_x) / (self.rect_width - self.bar_length)
                pygame.mixer.music.set_volume(self.volume)
            else:
                self.prev_volume = self.volume
                self.volume = 0
                pygame.mixer.music.set_volume(self.volume)
                self.mute_button_clicked = True

    def check_draggable_bar(self, mouse_x, mouse_y):
        if (
            self.rect_x < mouse_x < self.rect_x + self.rect_width and
            self.rect_y < mouse_y < self.rect_y + self.rect_height
        ):
            if (
                self.bar_x < mouse_x < self.bar_x + self.bar_length and
                self.bar_y < mouse_y < self.bar_y + self.bar_thickness
            ):
                self.dragging = True
                self.offset_x = mouse_x - self.bar_x
                self.offset_y = mouse_y - self.bar_y
                self.mute_button_clicked = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.check_mute_button(mouse_x, mouse_y)
                    self.check_draggable_bar(mouse_x, mouse_y)

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        self.bar_x, _ = pygame.mouse.get_pos()
                        self.bar_x -= self.offset_x

                        self.bar_x = max(self.rect_x, min(self.rect_x + self.rect_width - self.bar_length, self.bar_x))

                        self.volume = (self.bar_x - self.rect_x) / (self.rect_width - self.bar_length)
                        pygame.mixer.music.set_volume(self.volume)

            if self.volume != self.prev_volume:
                self.prev_volume = self.volume
                print(f"Volume: {self.volume}")

            self.window.fill(self.BLACK)

            rect_color = self.GREY if self.volume == 0 else self.BLUE
            pygame.draw.rect(self.window, rect_color, (self.rect_x, self.rect_y, self.rect_width, self.rect_height))

            pygame.draw.rect(self.window, self.WHITE, (self.bar_x, self.initial_bar_y, self.bar_length, self.bar_thickness))

            pygame.draw.circle(self.window, self.GREY, (self.button_x, self.button_y), self.button_radius)
            mute_font = pygame.font.Font(None, 20)
            mute_text = mute_font.render("Mute", True, self.BLACK)
            mute_text_rect = mute_text.get_rect(center=(self.button_x, self.button_y))
            self.window.blit(mute_text, mute_text_rect)

            cursor_x, _ = pygame.mouse.get_pos()

            if self.rect_x < cursor_x < self.rect_x + self.rect_width and pygame.mouse.get_pressed()[0]:
                self.bar_x = cursor_x - self.bar_length // 2
                self.bar_x = max(self.rect_x, min(self.rect_x + self.rect_width - self.bar_length, self.bar_x))
                self.volume = (self.bar_x - self.rect_x) / (self.rect_width - self.bar_length)
                pygame.mixer.music.set_volume(self.volume)

            pygame.display.flip()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    draggable_bar = DraggableBar()
    draggable_bar.run()
