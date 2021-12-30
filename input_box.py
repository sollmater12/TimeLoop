import pygame


class InputBox():

    def __init__(self, x, y):

        self.font = pygame.font.Font(None, 32)

        self.inputBox = pygame.Rect(x, y, 140, 32)

        self.colourInactive = pygame.Color('white')
        self.colourActive = pygame.Color('grey')
        self.colour = self.colourInactive

        self.text = ''
        self.result = ''

        self.active = False
        self.isBlue = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.inputBox.collidepoint(event.pos)
            self.colour = self.colourActive if self.active else self.colourInactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.result = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        txtSurface = self.font.render(self.text, True, self.colour)
        width = max(200, txtSurface.get_width() + 10)
        self.inputBox.w = width
        screen.blit(txtSurface, (self.inputBox.x + 5, self.inputBox.y + 5))
        pygame.draw.rect(screen, self.colour, self.inputBox, 2)

        if self.isBlue:
            self.color = (0, 128, 255)
        else:
            self.color = (255, 100, 0)
