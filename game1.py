import random  # ランダムで旗とプレイヤーを配置
import math  # 旗とプレイヤーの距離を計算


def calc_distance(x1, y1, x2, y2):
    dif_x = x1 - x2
    dif_y = y1 - y2
    return math.sqrt(dif_x**2 + dif_y**2)


# 旗の座標決定（ランダム）
flag_x = random.randrange(0, 10)
flag_y = random.randrange(0, 10)

# プレイヤーの座標決定（ランダム）
player_x = random.randrange(0, 10)
player_y = random.randrange(0, 10)

# 旗とプレイヤーの位置が異なっているなら、繰り返す
while (flag_x != player_x) or (flag_y != player_y):

# 旗とプレイヤーの距離表示
distance = calc_distance(player_x, player_y, flag_x, flag_y)
print("旗への距離", distance)

# キー入力に応じて、プレイヤーを移動
key = input("w:上に移動 s:下に移動 d:右に移動 a:左に移動")

if key ==


