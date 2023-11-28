import pygame
import sys
import random

# ゾンビをよけるゲーム、　敵の数を減らす、　リプレイできるようにする:リプレイ＝スペース⇒画面クリック
# 敵のspeedをランダムでバラバラにしたい、　敵の画像を2種類のゾンビ、　敵画像の大きさを統一したい、
# 敵のスピードで大きさが変わる、　背景に画像を設定、　playerに画像を設定、　7秒ごとに特殊敵出現
# 特殊敵の大きさ調整、　くるくる回る



# pygameの初期化
pygame.init()

# 画面の設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ウォーキングデッド")


# 背景画像を設定
background_image = pygame.image.load("img/haikyo.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


# プレイヤーの初期位置
player_width = 50
player_height = 50
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 10
player_speed = 7

# プレイヤーの画像を設定
player_image = pygame.image.load("img/hengao.png")
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# 敵の初期設定
enemy_width = 50
enemy_height = 50
max_enemies = 20
enemy_list = []

# 2つの敵画像を読み込む
enemy_images = [
    pygame.image.load("img/zonbi.png"),
    pygame.image.load("img/zonbi2.png")
]

# 特殊な敵の設定
new_enemy_width = 400
new_enemy_height = 400
new_enemy_images = [
    pygame.image.load("img/enemy_speed_20.png")
]

# 新しい敵の最後の出現時刻　＆　5秒ごとに新しい敵を生成
new_enemy_spawn_time = pygame.time.get_ticks()
new_enemy_spawn_interval = 5000

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
    current_time = pygame.time.get_ticks()

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

    # 5秒ごとに新しい敵を生成
    if current_time - new_enemy_spawn_time > new_enemy_spawn_interval:
        new_enemy_x = random.randint(0, screen_width - new_enemy_width)
        new_enemy_y = 0
        new_enemy_speed = 20
        new_enemy_image = random.choice(new_enemy_images)

        scale_factor = max(0.5, min(3.0, 1 / new_enemy_speed))
        scaled_width = int(new_enemy_width * scale_factor)
        scaled_height = int(new_enemy_height * scale_factor)
        scaled_image = pygame.transform.scale(new_enemy_image, (scaled_width, scaled_height))
        enemy_list.append([new_enemy_x, new_enemy_y, new_enemy_speed, scaled_image])

        # 最後に新しい敵が生成された時刻を更新
        new_enemy_spawn_time = current_time

    # 通常の敵を生成
    if len(enemy_list) < max_enemies:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = 0
        enemy_speed = random.uniform(1, 10)
        enemy_image = random.choice(enemy_images)

        scale_factor = max(0.5, min(3.0, 1 / enemy_speed))
        scaled_width = int(enemy_width * scale_factor)
        scaled_height = int(enemy_height * scale_factor)
        scaled_image = pygame.transform.scale(enemy_image, (scaled_width, scaled_height))
        enemy_list.append([enemy_x, enemy_y, enemy_speed, scaled_image])

    # 敵の移動
    for enemy in enemy_list:
        enemy[1] += enemy[2]  # 敵の縦（ｙ）座標に、敵[2]の速度を加える⇒敵が画面上部から下方向に移動

    # 画面下端に到達した敵をリストから排除
    enemy_list = [enemy for enemy in enemy_list if enemy[1] < screen_height]

    for enemy in enemy_list:
        if(
            player_x < enemy[0] + enemy_width       # プレイヤの左端が敵の右端よりも左側にあるか
            and player_x + player_width > enemy[0]  # プレイヤの右端が敵の左端よりも右側にあるか
            and player_y < enemy[1] + enemy_height  # プレイヤの上端が敵の下端よりも上にあるか
            and player_y + player_height > enemy[1] # プレイヤの下端が敵の上端よりも下にあるか
        ):
            game_over = True  # 上記の全てが満たされた場合はプレイヤと敵が重なっているためゲームオーバー

    # 画像の描画
    screen.blit(background_image, (0,0))  # background_image, (0,0)で画面全体を背景で覆う
    screen.blit(player_image, (player_x, player_y))  
    for enemy in enemy_list:
        screen.blit(enemy[3], (enemy[0], enemy[1]))  # リスト内の各敵の画像を描画

    # ゲームオーバー状態で、テキストを描画
    if game_over:
        screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, (screen_height - game_over_text.get_height()) // 2))

    # 画面の描画を反映。全ての描画が表示される
    pygame.display.flip()
     
    # フレームレート制限（1秒当たり30フレーム）
    clock.tick(30)