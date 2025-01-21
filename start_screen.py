def start_screen():
    intro_text = ["САПЕР"]
    fon = pygame.transform.scale(load_image('fon.png'), (600, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('serif', 72) 
    text_coord = 120
    color = (255, 255, 255)
    rect_position = [205, 390, 200, 50]
    pygame.draw.rect(screen, color , rect_position)
    pygame.font.init()
    my_font_0 = pygame.font.SysFont('Classy Vogue', 50)
    text_surface_restart = my_font_0.render('Новая игра', False, (0, 0, 0))
    text_surface_restart_rect = text_surface_restart.get_rect(topleft=(210, 400))
    board.screen.blit(text_surface_restart, text_surface_restart_rect)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            mouse_pos = pygame.mouse.get_pos()
            if text_surface_restart_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)