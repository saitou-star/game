import pygame
import sys
import random
import os
from glob import glob

# Pygameの初期化
pygame.init()

# 画面のサイズ
WIDTH, HEIGHT = 800, 600

# 色
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# プレイヤークラス
class Player:
    def __init__(self, name, hp, mp, image_path, x, y):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def attack(self):
        return random.randint(1, 10)

    def cast_spell(self):
        if self.mp >= 5:
            self.mp -= 5
            return random.randint(5, 15)
        else:
            print("銃弾が足りません!! 通常攻撃します。")
            return self.attack()

    def use_item(self):
        return random.randint(5, 10)

# プレイヤーと敵の数をランダムに決定
num_players = 2
num_enemies = random.randint(2, 5)

# Pygameの画面初期化
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WALKING_RPG Battle")

# 背景画像の読み込み（PNGファイル）
background = pygame.image.load("enemy_img/onigashima.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# フォントの設定
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# プレイヤーの初期化
players = []
player_names = ["Rick", "Darryl"]
for i in range(num_players):
    player = Player(player_names[i], 30, 20, f"img/player{i+1}.png", 50, 200 + i * 100)
    players.append(player)

# 敵の初期化
enemies = []

images = glob(r"enemy_img/*")

# 生成する敵の数を2体に固定
num_enemies = 2

# 敵の縮小率
scale_factor = 0.8

for i in range(num_enemies):
    enemy_image_path = images[random.randint(0, len(images) - 1)]
    
    # 敵画像のサイズを取得
    enemy_image = pygame.image.load(enemy_image_path)
    enemy_width, enemy_height = enemy_image.get_size()
    
    # サイズを縮小
    enemy_width = int(enemy_width * scale_factor)
    enemy_height = int(enemy_height * scale_factor)
    
    # 画面右側の上部に2体の敵を表示し、重ならないように配置
    initial_x = WIDTH - enemy_width
    initial_y = i * (HEIGHT // (2 * num_enemies))  # 画面を垂直方向に均等に分割して配置
    
    # 画面からはみ出ないように再配置
    while initial_y + enemy_height > HEIGHT or initial_y < 0:
        initial_y = random.randint(0, HEIGHT - enemy_height)
    
    enemy = Player(f"monster{i+1}", 20, 10, enemy_image_path, initial_x, initial_y)
    enemies.append(enemy)


# 戦闘画面のメインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # マウスクリックでコマンドを実行
            x, y = event.pos
            if attack_button.collidepoint(x, y):
                for player in players:
                    damage = player.attack()
                    target_enemy = random.choice(enemies)
                    target_enemy.hp -= damage
                    print(f"{player.name}が{target_enemy.name}に{damage}のダメージを与えました！")
            elif magic_button.collidepoint(x, y):
                for player in players:
                    damage = player.cast_spell()
                    target_enemy = random.choice(enemies)
                    target_enemy.hp -= damage
                    print(f"{player.name}が{target_enemy.name}に{damage}のダメージを与えました！")
            elif item_button.collidepoint(x, y):
                for player in players:
                    heal = player.use_item()
                    player.hp += heal
                    print(f"{player.name}が{heal}の回復アイテムを使用し、HPが回復しました")
            elif escape_button.collidepoint(x, y):
                print("逃げる！")

    # プレイヤーのHPが0以下の場合
    for player in players:
        if player.hp <= 0:
            game_over_text = font.render("Game Over!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.wait(5000)  # 5秒間メッセージ表示後に終了
            pygame.quit()
            sys.exit()

    # 敵のHPが0以下の場合
    for enemy in enemies:
        if enemy.hp <= 0:
            enemies.remove(enemy)

    # 背景を描画
    screen.blit(background, (0, 0))

    # プレイヤーの画像表示
    for player in players:
        screen.blit(player.image, (player.rect.x, player.rect.y))
    # 敵の画像表示と位置調整
    for enemy in enemies:
        # 敵が画面外にはみ出さないように位置を制限
        enemy.rect.x = max(0, min(WIDTH - enemy.rect.width, enemy.rect.x))
        enemy.rect.y = max(0, min(HEIGHT - enemy.rect.height, enemy.rect.y))
        screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))


    # コマンドボタンの表示
    button_width, button_height = 150, 50
    button_margin = 20

    attack_button = pygame.draw.rect(screen, RED, (50, 450, button_width, button_height))
    magic_button = pygame.draw.rect(screen, RED, (attack_button.right + button_margin, 450, button_width, button_height))
    item_button = pygame.draw.rect(screen, RED, (magic_button.right + button_margin, 450, button_width, button_height))
    escape_button = pygame.draw.rect(screen, RED, (item_button.right + button_margin, 450, button_width, button_height))

    # ボタンにラベルを表示
    attack_label = font.render("Attack", True, WHITE)
    magic_label = font.render("Handgun", True, WHITE)
    item_label = font.render("Item", True, WHITE)
    escape_label = font.render("Escape", True, WHITE)

    # ラベルの描画位置調整
    screen.blit(attack_label, (attack_button.centerx - attack_label.get_width() // 2, attack_button.centery - attack_label.get_height() // 2))
    screen.blit(magic_label, (magic_button.centerx - magic_label.get_width() // 2, magic_button.centery - magic_label.get_height() // 2))
    screen.blit(item_label, (item_button.centerx - item_label.get_width() // 2, item_button.centery - item_label.get_height() // 2))
    screen.blit(escape_label, (escape_button.centerx - escape_label.get_width() // 2, escape_button.centery - escape_label.get_height() // 2))

    # 画面を更新
    pygame.display.flip()