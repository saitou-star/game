import pygame
import sys
import random
# pythonで敵をよけて進むゲームを作って,
# 敵の数を減らしたい,
# リプレイできるようにするには？,

# pygameの初期化
pygame.init()

# 画面の設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ウォーキングデッド")

# 色の定義
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# プレイヤーの初期位置
player_width = 50
player_height = 50
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 10

# プレイヤーの速度
player_speed = 7

# 敵の初期設定
enemy_width = 50
enemy_height = 50
enemy_speed = 6
max_enemies = 10
enemy_list = []

# 敵を作成する関数
def create_enemy():
    if len(enemy_list) < max_enemies:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = 0
        enemy_list.append([enemy_x, enemy_y])

# ゲームの初期化
def initialize_game():
    global player_x, player_y, enemy_list
    player_x = (screen_width - player_width) // 2
    player_y = screen_height - player_height - 10
    enemy_list = []
initialize_game()

# ゲームオーバーのメッセージ表示
font = pygame.font.Font(None, 36)
def display_game_over():
    game_over_text = font.render("Game Over ⇒ スペースを押してリプレイ", True, black)
    screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, (screen_height - game_over_text.get_height()) // 2))
    pygame.display.flip()


# ゲームループ
clock = pygame.time.Clock()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            initialize_game()

    keys = pygame.key.get_pressed()
    player_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed

    # 敵の生成
    create_enemy()

    # 敵の移動
    for enemy in enemy_list:
        enemy[1] += enemy_speed

    # 敵が画面外に出たら削除
    enemy_list = [enemy for enemy in enemy_list if enemy[1] < screen_height]

    # プレイヤーと敵の衝突判定
    for enemy in enemy_list:
        if(
            player_x < enemy[0] + enemy_width
            and player_x + player_width > enemy[0]
            and player_y < enemy[1] + enemy_height
            and player_y + player_height > enemy[1]
        ):
            game_over = True

    # 画面の描画
    screen.fill(white)
    pygame.draw.rect(screen, black, [player_x, player_y, player_width, player_height])
    for enemy in enemy_list:
        pygame.draw.rect(screen, red, [enemy[0], enemy[1], enemy_width, enemy_height])

    if game_over:
        display_game_over()

    pygame.display.flip()

    # フレームレートの設定
    clock.tick(30)
