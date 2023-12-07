import random
import pygame

pygame.init()
pygame.mixer.init()

font14 = pygame.font.Font('freesansbold.ttf', 14)
font20 = pygame.font.Font('freesansbold.ttf', 20)
font30 = pygame.font.Font('freesansbold.ttf', 30)
font40 = pygame.font.Font('freesansbold.ttf', 40)

ICON = pygame.image.load('rainbow_ball.png')
pygame.display.set_icon(ICON)

hit_sound = pygame.mixer.Sound('hit.mp3')
victory_sound = pygame.mixer.Sound('victory.mp3')
victory_sound.set_volume(0.25)

pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.025)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пінг-Понг")

clock = pygame.time.Clock()
FPS = 30


class Player:
    def __init__(self, pos_x, pos_y, width, height, speed, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

        self.playerRect = pygame.Rect(pos_x, pos_y, width, height)
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)

    def display(self):
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)

    def update(self, yFac):
        self.pos_y = self.pos_y + self.speed * yFac

        if self.pos_y <= 0:
            self.pos_y = 0
        elif self.pos_y + self.height >= HEIGHT:
            self.pos_y = HEIGHT - self.height

        self.playerRect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def getRect(self):
        return self.playerRect


class Ball:
    def __init__(self, pos_x, pos_y, radius, speed, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.speed = speed
        self.initial_speed = speed
        self.color = color
        self.xFac = random.choice([-1, 1])
        self.yFac = random.choice([-1, 1])
        self.ball = pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)
        self.firstTime = 1
        self.hit_sound = hit_sound

    def display(self):
        self.ball = pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)

    def update(self):
        self.pos_x += self.speed * self.xFac
        self.pos_y += self.speed * self.yFac

        if self.pos_y <= 0 or self.pos_y >= HEIGHT:
            self.yFac *= -1

        if self.pos_x <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.pos_x >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.pos_x = WIDTH // 2
        self.pos_y = HEIGHT // 2
        self.xFac *= -1
        self.firstTime = 1
        self.speed += 0.625

    def reset_speed(self):
        self.speed = self.initial_speed

    def hit(self):
        self.xFac *= -1
        self.hit_sound.play()

    def getRect(self):
        return self.ball


def draw_main_menu(selected_option):
    title_text = font40.render("Пінг-Понг", True, WHITE)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title_text, title_text_rect)

    start_text = font20.render("Старт", True, WHITE)
    start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(start_text, start_text_rect)

    settings_text = font20.render("Налаштування", True, WHITE)
    settings_text_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(settings_text, settings_text_rect)

    about_text = font20.render("Про гру", True, WHITE)
    about_text_rect = about_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(about_text, about_text_rect)

    exit_text = font20.render("Вихід", True, WHITE)
    exit_text_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(exit_text, exit_text_rect)

    if selected_option == 1:
        pygame.draw.rect(screen, WHITE, (start_text_rect.left - 5, start_text_rect.top - 5,
                                         start_text_rect.width + 10, start_text_rect.height + 10), 3)
    elif selected_option == 2:
        pygame.draw.rect(screen, WHITE, (settings_text_rect.left - 5, settings_text_rect.top - 5,
                                         settings_text_rect.width + 10, settings_text_rect.height + 10), 3)
    elif selected_option == 3:
        pygame.draw.rect(screen, WHITE, (about_text_rect.left - 5, about_text_rect.top - 5,
                                         about_text_rect.width + 10, about_text_rect.height + 10), 3)

    elif selected_option == 4:
        pygame.draw.rect(screen, WHITE, (exit_text_rect.left - 5, exit_text_rect.top - 5,
                                         exit_text_rect.width + 10, exit_text_rect.height + 10), 3)


def main_menu():
    selected_option = 1
    running = True

    while running:
        screen.fill(BLACK)
        draw_main_menu(selected_option)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option % 4) + 1
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 2) % 4 + 1
                elif event.key == pygame.K_RETURN:
                    if selected_option == 1:
                        game_loop()
                        running = False
                    elif selected_option == 2:
                        settings_menu()
                        running = False
                    elif selected_option == 3:
                        about_menu()
                        running = False
                    elif selected_option == 4:
                        pygame.quit()

    return selected_option


def draw_about_menu():
    about_title_text = font30.render("Про гру", True, WHITE)
    about_title_text_rect = about_title_text.get_rect(center=(WIDTH // 2, HEIGHT // 5 - 50))
    screen.blit(about_title_text, about_title_text_rect)

    a_text = font14.render("Гра 'Пінг-понг' - захоплива комп'ютерна гра, яка пропонує гравцям захопливі емоції та "
                           "конкуренцію на віртуальному полі.", True, WHITE)
    a_text2 = font14.render("Ваше завдання полягає у перемозі над супротивником, забиваючи м'ячик за його поле.",
                            True, WHITE)
    a_text3 = font14.render("Використовуйте свою спритність і реакцію, щоб перемогти опонента у цій швидкісній грі.",
                            True, WHITE)
    a_text4 = font14.render("Зберіть п'ять балів, щоб заслужити звання переможця!", True, WHITE)

    a_text_rect = a_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 190))
    a_text2_rect = a_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 170))
    a_text3_rect = a_text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    a_text4_rect = a_text4.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 130))

    screen.blit(a_text, a_text_rect)
    screen.blit(a_text2, a_text2_rect)
    screen.blit(a_text3, a_text3_rect)
    screen.blit(a_text4, a_text4_rect)

    controls_title_text = font30.render("Правила гри", True, WHITE)
    controls_title_text_rect = controls_title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90))
    screen.blit(controls_title_text, controls_title_text_rect)

    c_text = font14.render("1. Гра здійснюється між двома гравцями на віртуальному столі для пінг-понгу.", True, WHITE)
    c_text2 = font14.render("2. Кожен гравець керує своєю платформою, яку можна рухати вгору і вниз.", True, WHITE)
    c_text3 = font14.render("3. Гравець може переміщувати свою платформу вгору, натискаючи клавішу \"W\" або стрілку "
                            "\"Вгору\" на клавіатурі.", True, WHITE)
    c_text4 = font14.render("4. Для руху вниз використовуйте клавішу \"S\" або стрілку \"Вниз\".", True, WHITE)
    c_text5 = font14.render("5. М'ячик буде переміщуватись між гравцями, відскакуючи від платформ.", True, WHITE)
    c_text6 = font14.render("6. Якщо м'ячик пролітає за поле вашого суперника, ви отримуєте один бал.", True, WHITE)
    c_text7 = font14.render("7. Гра триває до того моменту, коли один з гравців набере п'ять балів.", True, WHITE)
    c_text8 = font14.render("8. Гравець, який першим набере п'ять балів, вважається переможцем.", True, WHITE)
    c_text9 = font14.render("9. Після завершення гри ви можете розпочати нову гру або вийти з програми.", True, WHITE)

    c_text_rect = c_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    c_text2_rect = c_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    c_text3_rect = c_text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
    c_text4_rect = c_text4.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    c_text5_rect = c_text5.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    c_text6_rect = c_text6.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    c_text7_rect = c_text7.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))
    c_text8_rect = c_text8.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 160))
    c_text9_rect = c_text9.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 190))

    screen.blit(c_text, c_text_rect)
    screen.blit(c_text2, c_text2_rect)
    screen.blit(c_text3, c_text3_rect)
    screen.blit(c_text4, c_text4_rect)
    screen.blit(c_text5, c_text5_rect)
    screen.blit(c_text6, c_text6_rect)
    screen.blit(c_text7, c_text7_rect)
    screen.blit(c_text8, c_text8_rect)
    screen.blit(c_text9, c_text9_rect)

    back_text = font20.render("Назад (Esc)", True, WHITE)
    back_text_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 240))
    screen.blit(back_text, back_text_rect)


def about_menu():
    running = True

    while running:
        screen.fill(BLACK)
        draw_about_menu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu()


def draw_settings_menu(volume_option):
    settings_title_text = font40.render("Налаштування", True, WHITE)
    settings_title_text_rect = settings_title_text.get_rect(center=(WIDTH // 2, HEIGHT // 5 - 50))
    screen.blit(settings_title_text, settings_title_text_rect)

    volume_text = font20.render("Гучність фонової музики: " + str(volume_option), True, WHITE)
    volume_text_rect = volume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(volume_text, volume_text_rect)

    back_text = font20.render("Назад (Esc)", True, WHITE)
    back_text_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
    screen.blit(back_text, back_text_rect)


def settings_menu():
    running = True
    volume_option = int(pygame.mixer.music.get_volume() * 100)

    while running:
        screen.fill(BLACK)
        draw_settings_menu(volume_option)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    main_menu()
                elif event.key == pygame.K_UP and volume_option < 100:
                    volume_option += 1
                    pygame.mixer.music.set_volume(volume_option / 100)
                elif event.key == pygame.K_DOWN and volume_option > 0:
                    volume_option -= 1
                    pygame.mixer.music.set_volume(volume_option / 100)

    pygame.mixer.music.set_volume(0.025)


def game_loop():
    running = True
    restart_game = False
    game_over = False
    victory_sound_played = False

    pygame.mixer.music.play(-1)

    player1 = Player(20, 0, 10, 80, 10, RED)
    player2 = Player(WIDTH - 30, 0, 10, 80, 10, RED)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 12, 7, WHITE)

    listOfPlayers = [player1, player2]

    player1Score, player2Score = 0, 0
    player1YFac, player2YFac = 0, 0

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and restart_game:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    if game_over:
                        main_menu()
                if event.key == pygame.K_UP:
                    player2YFac = -1
                if event.key == pygame.K_DOWN:
                    player2YFac = 1
                if event.key == pygame.K_w:
                    player1YFac = -1
                if event.key == pygame.K_s:
                    player1YFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1YFac = 0

        if not game_over:
            for player in listOfPlayers:
                if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                    ball.hit()

            player1.update(player1YFac)
            player2.update(player2YFac)
            point = ball.update()

            if point == -1:
                player1Score += 1
                player1.height += 10
                player2.height -= 10
                if player1Score >= 5:
                    restart_game = True
                    game_over = True
                    pygame.mixer.music.stop()
                    if not victory_sound_played:
                        victory_sound.play()
                        victory_sound_played = True
                else:
                    ball.reset()
            elif point == 1:
                player2Score += 1
                player2.height += 10
                player1.height -= 10
                if player2Score >= 5:
                    restart_game = True
                    game_over = True
                    pygame.mixer.music.stop()
                    if not victory_sound_played:
                        victory_sound.play()
                        victory_sound_played = True
                else:
                    ball.reset()

        player1.display()
        player2.display()
        ball.display()

        player1.displayScore("Гравець №1: ", player1Score, 110, 30, WHITE)
        player2.displayScore("Гравець №2: ", player2Score, WIDTH - 110, 30, WHITE)

        if restart_game:
            screen.fill(BLACK)

            victory_text = font40.render("Гра закінчена. Гравець {} переміг!"
                                         .format("№1" if player1Score == 5 else "№2"), True, WHITE)
            victory_text_rect = victory_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            screen.blit(victory_text, victory_text_rect)

            restart_text = font20.render("Натисніть ПРОБІЛ, щоб перезапустити гру", True, WHITE)
            restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, restart_text_rect)

            if game_over:
                restart_text = font20.render("Натисніть ESC, щоб вийти", True, WHITE)
                restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(restart_text, restart_text_rect)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()

pygame.quit()
