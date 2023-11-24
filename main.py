import tkinter as tk
# importされるファイルは、関数やクラスの定義のみしかしない。どうせimportすると実行されるから
import pokeapi  # import = pokeapiを一回全て実行しているという事になる。


def key(e):
    print(e.keysym) # keysym　はどのキーを押したかを表示

def mouse(e):
        print(e.x) # 画面のX軸のどこを押したかを表示（y軸はe.yと記載）

# ボタンクリック時に実行する関数
# 入力した番号を読み込んで、ポケモンデータを取得
def change_data(entry_id):
    pokemon = pokeapi.get_pokemon(entry_id)
    name_label["text"] = pokemon.ja_name
    data_label["text"] = f"高さ:{pokemon.height}m,重さ:{pokemon.weight}kg"
    img["file"] = pokemon.img
    flavor_text_msg["text"] = pokemon.flavor_text


# __name__は実行したファイルかimportしたファイルかを判定できる
if __name__ == "__main__": 
    font_size = 20  # ウィンドウ上の文字サイズ
    pokemon = pokeapi.get_pokemon(1)  # 最初のポケモンデータ(フシギダネ）を取得しておく

    # ウィンドウ作成
    root = tk.Tk() # ウィンドウを作り、一行下で大きさを指定
    root.geometry("1280x720")

    # フレーム用意、配置 (画面は図鑑番号のフレームとポケモンデータフレームの２個だけ)
    entry_frame = tk.Frame(root)  # 入力欄フレーム
    pokemon_frame = tk.Frame(root)  # ポケモンデータ(画像と説明文)表示フレーム
    entry_frame.pack()
    pokemon_frame.pack()

    # 図鑑番号入力欄用のウィジェット(パーツ)用意
    entry_label = tk.Label(entry_frame, text="図鑑番号:", font=font_size)
    entry_id = tk.Entry(entry_frame,font=font_size)
    entry_button = tk.Button(
        # commandはラムダ式（lambda）,change_dataが関数と（）内が引数
        entry_frame, text="検索", command=lambda: change_data(entry_id.get())
    )
    # ウィジェット配置(grid = 横並び、row=縦、column=横)　←　entry_frameの設定
    entry_label.grid(row=0, column=0)
    entry_id.grid(row=0, column=1)
    entry_button.grid(row=0, column=2)

    # ポケモンデータ表示用のウィジェット用意
    name_label = tk.Label(pokemon_frame, text=pokemon.ja_name, font=font_size)
    img = tk.PhotoImage(file=pokemon.img) # photoimage = 画像の読み込み作業
    image_label = tk.Label(pokemon_frame, image=img)
    data_label = tk.Label(
        pokemon_frame,
        text=f"高さ:{pokemon.height}m,重さ:{pokemon.weight}kg",
        font=font_size,
    )
    # 説明文を表示
    flavor_text_msg = tk.Message(
        pokemon_frame,
        text=pokemon.flavor_text,
        font=font_size,
        width=400,
    )

    # ウィジェット配置(ポケモンデータフレームの並び、上から。)
    name_label.pack()
    image_label.pack()
    data_label.pack()
    flavor_text_msg.pack(pady=(10, 0))


    root.bind("<Key>",key)
    root.bind("<Button-1>",mouse) # button-1は左クリックのこと
    root.bind("<Button-2>",mouse)
    root.bind("<Button-3>",mouse)
    root.bind("<KeyRelease>",mouse)
    root.bind("<Motion>",mouse) # マウスを動かすと表示(マウスの座標を取得)
    # 他の操作は、イベント検索

    #メインループ
    root.mainloop()