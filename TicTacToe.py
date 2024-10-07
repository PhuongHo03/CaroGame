import pygame

pygame.init()
field_size = 300
screen = pygame.display.set_mode((field_size,field_size))
pygame.display.set_caption("TicTacToe")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None,40)
running = True
line_width = 6
marker = [[0 for x in range(0,3)] for y in range(0,3)]
clicked = False
pos = []
player = 1
winner = 0
step = 0
game_over = False

def draw_grid():
    bg = (255,255,200)
    grid = (50,50,50)
    screen.fill(bg)
    for x in range(1,3):
        pygame.draw.line(screen,grid,(0,x*100),(field_size,x*100),line_width)
        pygame.draw.line(screen,grid,(x*100,0),(x*100,field_size),line_width)

def draw_marker():
    x_pos = 0
    for row in marker:
        y_pos = 0
        for cell in row:
            if cell == 1:
                pygame.draw.line(screen,(0,255,0),(x_pos*100+15,y_pos*100+15),(x_pos*100+85,y_pos*100+85),line_width)
                pygame.draw.line(screen,(0,255,0),(x_pos*100+15,y_pos*100+85),(x_pos*100+85,y_pos*100+15),line_width)
            if cell == -1:
                pygame.draw.circle(screen,(255,0,0),(x_pos*100+50,y_pos*100+50),38,line_width)
            y_pos += 1
        x_pos += 1

def check_winner():
    global winner, game_over
    y_pos = 0
    for row in marker:
        if sum(row) == 3:
            winner = 1
            game_over = True
        if sum(row) == -3:
            winner = 2
            game_over = True

        if marker[0][y_pos] + marker[1][y_pos] + marker[2][y_pos] == 3:
            winner = 1
            game_over = True
        if marker[0][y_pos] + marker[1][y_pos] + marker[2][y_pos] == -3:
            winner = 2
            game_over = True
        y_pos += 1
        
        if marker[0][0] + marker[1][1] + marker[2][2] == 3 or marker[2][0] + marker[1][1] + marker[0][2] == 3:
            winner = 1
            game_over = True
        if marker[0][0] + marker[1][1] + marker[2][2] == -3 or marker[2][0] + marker[1][1] + marker[0][2] == -3:
            winner = 2
            game_over = True

    return game_over

def draw_winner(winner):
    global again_rect
    if winner == -1:
        win_img = font.render("No player wins",True,(0,0,255))
    else:
        win_img = font.render("Player " + str(winner) + " wins!",True,(0,0,255))
    pygame.draw.rect(screen,(0,255,0),(field_size//2-100,field_size//2-60,200,50))
    screen.blit(win_img,(field_size//2-100,field_size//2-50))

    again_img = font.render("Play again?",True,(0,0,255))
    again_rect = again_img.get_rect(center = (field_size//2,field_size//2+20))
    pygame.draw.rect(screen,(0,255,0),again_rect)
    screen.blit(again_img,again_rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                x_pos = pos[0]
                y_pos = pos[1]
                if marker[x_pos//100][y_pos//100] == 0:
                    marker[x_pos//100][y_pos//100] = player
                    step += 1
                    if step == 9:
                        winner = -1
                        game_over = True
                    player *= -1
                    check_winner()                
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):
                    game_over = False

    if not game_over:
        draw_grid()
        draw_marker()       
    else:
        draw_winner(winner)
        marker = [[0 for x in range(0,3)] for y in range(0,3)]
        pos = []
        player = 1
        step = 0
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()