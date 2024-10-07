import pygame
from sys import exit
from random import randint

field_size = 600
cell_size = field_size // 3
inf = float("inf")
vec2 = pygame.math.Vector2
cell_center = vec2(cell_size / 2)

class TicTacToe:
    def __init__(self,game):
        self.game = game
        self.field_img = self.get_scale_image(path="./resources/field.png",res=[field_size]*2)
        self.X_img = self.get_scale_image(path="./resources/x.png",res=[cell_size]*2)
        self.O_img = self.get_scale_image(path="./resources/o.png",res=[cell_size]*2)

        self.game_array = [[inf,inf,inf],
                           [inf,inf,inf],
                           [inf,inf,inf]]
        self.player = randint(0,1)

        self.line_indices_array = [[(0, 0), (0, 1), (0, 2)],
                                   [(1, 0), (1, 1), (1, 2)],
                                   [(2, 0), (2, 1), (2, 2)],
                                   [(0, 0), (1, 0), (2, 0)],
                                   [(0, 1), (1, 1), (2, 1)],
                                   [(0, 2), (1, 2), (2, 2)],
                                   [(0, 0), (1, 1), (2, 2)],
                                   [(0, 2), (1, 1), (2, 0)]]
        self.winner = None
        self.game_steps = 0
        self.font = pygame.font.SysFont('Verdana', cell_size // 4, True)

    def check_winner(self):
        for line_indices in self.line_indices_array:
            sum_line = sum([self.game_array[i][j] for i, j in line_indices])
            if sum_line in {0, 3}:
                self.winner = 'XO'[sum_line == 0]
                self.winner_line = [vec2(line_indices[0][::-1]) * cell_size + cell_center,
                                    vec2(line_indices[2][::-1]) * cell_size + cell_center]

    def run_game_process(self):
        current_cell = vec2(pygame.mouse.get_pos()) // cell_size
        col,row = map(int, current_cell)
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == inf and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()

    def draw_object(self):
        for y,row in enumerate(self.game_array):
            for x,obj in enumerate(row):
                if obj != inf:
                    self.game.screen.blit(self.X_img if obj else self.O_img, vec2(x,y)*cell_size)

    def draw_winner(self):
        if self.winner:
            pygame.draw.line(self.game.screen, 'red', *self.winner_line, cell_size // 8)
            label = self.font.render(f'Player "{self.winner}" wins!', True, 'white', 'black')
            self.game.screen.blit(label, (field_size // 2 - label.get_width() // 2, field_size // 4))

    def draw(self):
        self.game.screen.blit(self.field_img, (0,0))
        self.draw_object()
        self.draw_winner()

    @staticmethod
    def get_scale_image(path,res):
        img = pygame.image.load(path)
        return pygame.transform.smoothscale(img,res)
    
    def print_caption(self):
        pygame.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
        if self.winner:
            pygame.display.set_caption(f'Player "{self.winner}" wins! Press Space to Restart')
        elif self.game_steps == 9:
            pygame.display.set_caption(f'Game Over! Press Space to Restart')


    def run(self):
        self.print_caption()
        self.draw()
        self.run_game_process()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((field_size,field_size))
        self.clock = pygame.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.new_game()

    def run(self):
        while True:
            self.tic_tac_toe.run()
            self.check_event()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()