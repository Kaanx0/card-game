import pygame
import random
import time
from sys import exit

# Pygame kütüphanesini başlat
pygame.init()

# Ses efektleri için mixer'ı başlat
pygame.mixer.init()
pygame.mixer.music.load("audio/sans.mp3")
pygame.mixer.music.set_volume(0.5)
on_game_music = pygame.mixer.Sound("audio/onGame.mp3")
on_game_music.set_volume(0.1)
win_music = pygame.mixer.Sound("audio/win.mp3")
lose_music = pygame.mixer.Sound("audio/lose.mp3")
on_game_music_played = False
lose_music_played = False
win_music_played = False
game_started = False
# Oyun başlamadıysa müziği başlat
if not game_started:
    pygame.mixer.music.play(-1)


# Ekran boyutları
screen_width, screen_height = 1920, 1080
# Oyun ekranını oluştur
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Matching Game")  # Oyun başlığı
clock = pygame.time.Clock()  # Fps için gerekli


# Kartın arka yüzü
back_card_surf = pygame.image.load("graphics/cards/back.png").convert_alpha()
resized_width, resized_height = 200, 300

# Kart resimleri
card_images = [
    pygame.transform.scale(
        pygame.image.load("graphics/cards/Alphys.png").convert_alpha(),
        (resized_width, resized_height),
    ),
    pygame.transform.scale(
        pygame.image.load("graphics/cards/Papyrus.png").convert_alpha(),
        (resized_width, resized_height),
    ),
    pygame.transform.scale(
        pygame.image.load("graphics/cards/sans.png").convert_alpha(),
        (resized_width, resized_height),
    ),
    pygame.transform.scale(
        pygame.image.load("graphics/cards/Toriel.png").convert_alpha(),
        (resized_width, resized_height),
    ),
    pygame.transform.scale(
        pygame.image.load("graphics/cards/Chara.png").convert_alpha(),
        (resized_width, resized_height),
    ),
]
# Görseller
background_img = pygame.image.load("graphics/bcrnd.png").convert()
EasyMode_img = pygame.image.load("graphics/EasyMode.png").convert_alpha()
EasyMode_img_rect = EasyMode_img.get_rect(
    center=(screen_width // 2 - 200, screen_height // 2 + 250)
)
HardMode_img = pygame.image.load("graphics/HardMode.png").convert_alpha()
HardMode_img_rect = HardMode_img.get_rect(
    center=(screen_width // 2 + 200, screen_height // 2 + 250)
)
match_cards = pygame.image.load("graphics/MatchTheCards.png").convert_alpha()
esc = pygame.image.load("graphics/esc.png").convert_alpha()
esc_rect = esc.get_rect(center=(100, 100))


# Kartların başlangıç durumu ve can sayısı
cards = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
random.shuffle(cards)
card_states = ["closed"] * len(cards)
lives_easy = 5
lives_hard = 3
selected_cards = []
card_width, card_height = card_images[0].get_size()  
card_positions = [
    (i % 5 * (card_width + 20) + 450, i // 5 * (card_height + 20) + 300)
    for i in range(len(cards))
]

# Karakterlerin açık kalma süresi ve oyunun başlangıç zamanı
open_duration = 5
start_time = time.time()  # Milisaniye
current_level = None


# Oyun bitim ekranını göster
def show_game_over_screen():
    on_game_music.stop()
    global lose_music_played

    if not lose_music_played:
        lose_music.play()
        lose_music_played = True

    screen.fill((0, 0, 0))
    background_img = pygame.image.load("graphics/lose.png").convert()
    background_rect = background_img.get_rect(
        center=(screen_width // 2, screen_height // 2 - 100)
    )
    screen.blit(background_img, background_rect.topleft)
    pygame.display.flip()

    # Bekleme süresince olayları kontrol et ve ekrana güncelle
    end_time = time.time() + 5  # 5 saniye bekleme süresi
    while time.time() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        pygame.time.Clock().tick(60)


# Oyun kazanma ekranını göster
def show_you_win_screen():
    screen.fill((0, 0, 0))
    on_game_music.stop()
    global win_music_played

    if not win_music_played:
        win_music.play()
        win_music_played = True

    background_img = pygame.image.load("graphics/won.png").convert()
    background_rect = background_img.get_rect(
        center=(screen_width // 2, screen_height // 2 - 100)
    )
    screen.blit(background_img, background_rect.topleft)
    pygame.display.flip()

    end_time = time.time() + 5
    while time.time() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        pygame.time.Clock().tick(60)


# Ana oyun döngüsü
while not game_started:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if EasyMode_img_rect.collidepoint(event.pos):
                current_level = EasyMode_img
                lives = lives_easy

            if HardMode_img_rect.collidepoint(event.pos):
                current_level = HardMode_img
                lives = lives_hard

            if EasyMode_img_rect.collidepoint(
                event.pos
            ) or HardMode_img_rect.collidepoint(event.pos):
                game_started = True
                pygame.mixer.music.stop()

    screen.blit(background_img, (0, 0))
    screen.blit(EasyMode_img, EasyMode_img_rect)
    screen.blit(HardMode_img, HardMode_img_rect)
    pygame.display.flip()
    clock.tick(60)

# Ana oyun döngüsü
while True:
    current_time = time.time()
    screen.fill((0, 0, 0))
    # Eşleşen kartları göster
    screen.blit(match_cards, (470, 200))
    # Esc
    screen.blit(esc, esc_rect)
    # on_game_music_played kontrolü ile içerideki müziği bir kere çal
    if not on_game_music_played:
        on_game_music.play()
        on_game_music_played = True

    if current_level == EasyMode_img:
        screen.blit(EasyMode_img, (1600, 960))
    if current_level == HardMode_img:
        screen.blit(HardMode_img, (1600, 960))

    original_lives_image = pygame.image.load("graphics/heart.png")
    heart_width, heart_height = 50, 50
    heart_spacing = 10
    heart_images = [
        pygame.transform.scale(original_lives_image, (heart_width, heart_height))
        for _ in range(lives)
    ]

    for i, heart_image in reversed(list(enumerate(heart_images))):
        screen.blit(
            heart_image,
            (screen_width - 100 - (i + 1) * (heart_width + heart_spacing), 100),
        )
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if esc_rect.collidepoint(event.pos):
                pygame.quit()
                exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_started:
            x, y = event.pos 
            for i, state in enumerate(card_states):
                if state == "closed":
                    card_rect = pygame.Rect(
                        card_positions[i][0],
                        card_positions[i][1],
                        card_width,
                        card_height,
                    )
                    if card_rect.collidepoint(x, y):
                        card_states[i] = "open"
                        selected_cards.append(i)
                        break

    for i, state in enumerate(card_states):
        if state == "open":
            screen.blit(card_images[cards[i]], card_positions[i])
        elif current_time - start_time < open_duration:
            screen.blit(card_images[cards[i]], card_positions[i])
        else:
            screen.blit(back_card_surf, card_positions[i])

    if len(selected_cards) == 2:
        if cards[selected_cards[0]] == cards[selected_cards[1]]:
            selected_cards = []
        else:
            for card_index in selected_cards:
                card_states[card_index] = "open"
            pygame.display.flip()
            pygame.time.delay(1000)
            for card_index in selected_cards:
                card_states[card_index] = "closed"
            selected_cards = []
            lives -= 1

    # Oyun kazanıldıysa kazanan ekranını göster
    if card_states.count("open") == len(card_states):
        show_you_win_screen()
    # Can sıfırlandıysa oyun bitim ekranını göster
    elif lives == 0:
        show_game_over_screen()

    pygame.display.flip()
    clock.tick(60)
