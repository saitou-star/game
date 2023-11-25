import pygame
import sys
import random

# ゾンビをよけるゲーム、敵の数を減らす、リプレイできるようにする:リプレイ＝スペース⇒画面クリック
# 敵のspeedをランダムでバラバラにしたい、敵の画像を2種類のゾンビ、他仕掛けを作る



# pygameの初期化
pygame.init()

# 画面の設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ウォーキングデッド")


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
max_enemies = 12
enemy_list = []

# 2つの敵画像を読み込む
enemy_images = [
    pygame.image.load("zonbi.png"),
    pygame.image.load("zonbi2.png")
]

# ゲームの初期化
def initialize_game():
    global player_x, player_y, enemy_list
    player_x = (screen_width - player_width) // 2
    player_y = screen_height - player_height - 10
    enemy_list = []

initialize_game()

# ゲームオーバーのメッセージ表示
font = pygame.font.Font(None, 36)
game_over_text = font.render("Game Over ⇒ クリックしてリプレイ", True, (0, 0, 0))


# ゲームループ
clock = pygame.time.Clock()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                initialize_game()
                game_over = False

    keys = pygame.key.get_pressed()
    player_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed

    # 敵の生成
    if len(enemy_list) < max_enemies:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = 0
        enemy_speed = random.uniform(1, 5)
        enemy_image = random.choice(enemy_images)  # enemy画像をランダムに選択
        enemy_list.append([enemy_x, enemy_y, enemy_speed, enemy_image])

    # 敵の移動
    for enemy in enemy_list:
        enemy[1] += enemy[2]  # 速度を考慮して移動

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
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), [player_x, player_y, player_width, player_height])
    for enemy in enemy_list:
        screen.blit(enemy[3], (enemy[0], enemy[1]))  # 敵画像を描画

    if game_over:
        screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, (screen_height - game_over_text.get_height()) // 2))

    pygame.display.flip()

    # フレームレートの設定
    clock.tick(30)
