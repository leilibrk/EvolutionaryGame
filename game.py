from sys import exit
import pygame
from random import randint, choice

config = {
    'title': "Snail Jumper",
    'screen_width': 604,
    'screen_height': 800
}


def display_score():
    score = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = game_font.render(f"Score: {score}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(520, 50))
    screen.blit(score_surf, score_rect)
    return score


def display_best_score():
    score_surf = game_font.render(f"BScore: {best_score}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(520, 100))
    screen.blit(score_surf, score_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # loading images
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()

        # rotating -90 degree and scaling by factor of 0.5
        player_walk1 = pygame.transform.rotozoom(player_walk1, -90, 0.5)
        player_walk2 = pygame.transform.rotozoom(player_walk2, -90, 0.5)

        # flipping vertically
        player_walk1 = pygame.transform.flip(player_walk1, flip_x=False, flip_y=True)
        player_walk2 = pygame.transform.flip(player_walk2, flip_x=False, flip_y=True)

        self.player_walk = [player_walk1, player_walk2]
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midleft=(177, 656))

        self.player_gravity = 'left'
        self.gravity = 0

    def player_input(self):
        for pygame_event in events:
            if pygame_event.type == pygame.KEYDOWN:
                if pygame_event.key == pygame.K_SPACE:
                    self.player_gravity = "left" if self.player_gravity == 'right' else 'right'
                    self.flip_player_horizontally()
                    self.gravity = 0

    def apply_gravity(self):
        self.gravity += 1
        if self.player_gravity == 'left':
            self.rect.x -= self.gravity
            if self.rect.left <= 177:
                self.rect.left = 177
        else:
            self.rect.x += self.gravity
            if self.rect.right >= 430:
                self.rect.right = 430

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0

            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def flip_player_horizontally(self):
        for i, player_surface in enumerate(self.player_walk):
            self.player_walk[i] = pygame.transform.flip(player_surface, flip_x=True, flip_y=False)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type, position=None):
        super().__init__()

        if obstacle_type == "snail":
            snail_1 = pygame.image.load('Graphics/Snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('Graphics/Snail/snail2.png').convert_alpha()

            # rotating -90 degree and scaling by factor of 0.5
            snail_1 = pygame.transform.rotozoom(snail_1, -90, 0.5)
            snail_2 = pygame.transform.rotozoom(snail_2, -90, 0.5)

            if position == "left":
                # flipping vertically
                snail_1 = pygame.transform.flip(snail_1, flip_x=False, flip_y=True)
                snail_2 = pygame.transform.flip(snail_2, flip_x=False, flip_y=True)
            else:
                # flipping vertically and horizontally
                snail_1 = pygame.transform.flip(snail_1, flip_x=True, flip_y=True)
                snail_2 = pygame.transform.flip(snail_2, flip_x=True, flip_y=True)

            self.frames = [snail_1, snail_2]

            self.animation_index = 0
            self.image = self.frames[self.animation_index]
            if position == "left":
                self.rect = self.image.get_rect(midleft=(177, randint(-100, -50)))
            else:
                self.rect = self.image.get_rect(midright=(430, randint(-100, -50)))
        else:
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()

            fly_1 = pygame.transform.rotozoom(fly_1, 0, 0.5)
            fly_2 = pygame.transform.rotozoom(fly_2, 0, 0.5)

            self.frames = [fly_1, fly_2]

            self.animation_index = 0
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center=(303, randint(-100, -50)))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.y += 6
        self.destroy_if_necessary()

    def destroy_if_necessary(self):
        if self.rect.top > 800:
            self.kill()


def collision_sprite():
    for player in players:
        if pygame.sprite.spritecollide(player, obstacle_group, dokill=False):
            obstacle_group.empty()
            return False
    return True


def draw_intro_text(text, height, width=config['screen_width'] // 2, color=(111, 196, 169)):
    message = game_font.render(text, False, color)
    message_rect = message.get_rect(center=(width, height))
    screen.blit(message, message_rect)


def draw_btn(btn, btn_rect):
    pygame.draw.rect(screen, '#E8F3F1', btn_rect)
    pygame.draw.rect(screen, '#E8F3F1', btn_rect, 10)
    screen.blit(btn, btn_rect)


def create_players(player_numbers):
    global players

    players = pygame.sprite.Group()
    for i in range(player_numbers):
        players.add(Player())


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((config['screen_width'], config['screen_height']))
    pygame.display.set_caption(config['title'])
    clock = pygame.time.Clock()
    game_font = pygame.font.Font('Font/PixelType.ttf', 40)
    title_font = pygame.font.Font('Font/PixelType.ttf', 80)

    game_active = False
    start_time = 0
    best_score = 0

    background_surface = pygame.image.load('graphics/Background.jpg').convert()

    # Players
    players = None

    # Snails
    obstacle_group = pygame.sprite.Group()

    # Intro screen
    player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 3)
    player_stand_rect = player_stand.get_rect(center=(config['screen_width'] // 2, 250))

    game_name = title_font.render('Snail Jumper', False, (111, 196, 169))
    game_name_rectangle = game_name.get_rect(center=(config['screen_width'] // 2, 80))

    start_game_btn = game_font.render("Start Game", False, (111, 196, 169))
    start_game_btn_rect = start_game_btn.get_rect(center=(config['screen_width'] // 2, 440))

    start_evolutionary_btn = game_font.render("Start With Neuroevolution", False, (111, 196, 169))
    start_evolutionary_btn_rect = start_evolutionary_btn.get_rect(center=(config['screen_width'] // 2, 490))

    exit_btn = game_font.render("Exit", False, (111, 196, 169))
    exit_btn_rect = exit_btn.get_rect(center=(config['screen_width'] // 2, 540))

    # Timer
    snail_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(snail_timer, 400)

    fly_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(fly_timer, 800)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active:
                if event.type == snail_timer:
                    obstacle_group.add(Obstacle('snail', choice(['left', 'right'])))
                if event.type == fly_timer:
                    obstacle_group.add(Obstacle('fly'))
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_start_btn = start_game_btn_rect.collidepoint(pygame.mouse.get_pos())
                    clicked_start_evolutionary_btn = start_evolutionary_btn_rect.collidepoint(pygame.mouse.get_pos())
                    clicked_exit_btn = exit_btn_rect.collidepoint(pygame.mouse.get_pos())

                    if clicked_start_btn or clicked_start_evolutionary_btn:
                        game_active = True
                        start_time = pygame.time.get_ticks()
                        if clicked_start_btn:
                            create_players(player_numbers=1)
                        else:
                            create_players(player_numbers=300)
                    if clicked_exit_btn:
                        pygame.quit()
                        exit()

        if game_active:
            screen.blit(background_surface, (0, 0))

            # Player
            players.draw(screen)
            players.update()

            # Obstacle Group
            obstacle_group.draw(screen)
            obstacle_group.update()

            # collision
            game_active = collision_sprite()

            current_score = display_score()
            if current_score > best_score:
                best_score = current_score
            display_best_score()
        else:
            screen.fill("#2F4858")
            screen.blit(player_stand, player_stand_rect)
            screen.blit(game_name, game_name_rectangle)

            draw_btn(start_game_btn, start_game_btn_rect)
            draw_btn(start_evolutionary_btn, start_evolutionary_btn_rect)
            draw_btn(exit_btn, exit_btn_rect)

            if best_score > 0:
                draw_intro_text(f"Best score: {best_score}", height=400)

            draw_intro_text("Computational Intelligence Assignment", height=600, color='#D5ED8B')
            draw_intro_text("Amirkabir University of Technology", height=650, color='#AB8CD5')
        pygame.display.update()
        clock.tick(60)