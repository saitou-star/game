import requests
import os

# クラス定義
class Pokemon:
    def _init_(
            self, ja_name="", en_name="", weight=0.0, height=0.0, flavor_text="", img=None
    ):
        # python は下記でプロパティが出来る
        self.ja_name = ja_name
        self.en_name = en_name
        self.weight = weight
        self.height = height
        self.flavor_text = flavor_text
        self.img = img


# 関数定義
# PokeApiからポケモンデータ取得
def get_pokemon(id):
    # returnするPokemonクラスのインスタンス生成
    pokemon = Pokemon()

    # PokeApiにリクエスト、レスポンスをjson形式で受け取る
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    pokeapi = response.json() # 上のURLの内容（response）をjson形式で受け取る

    species_url = pokeapi["species"]["url"] # 上のURLのspeciesのurlを取得する
    response = requests.get(species_url) # URL先の日本語表記を取得。日本語じゃないならいらない
    pokeapi_species = response.json()

    # 各種データをレスポンスから取得
    # 英語名、重さ、高さ、画像URL取得
    pokemon.en_name = pokeapi["name"]
    pokemon.weight = float(pokeapi["weight"]) / 10
    pokemon.height = float(pokeapi["height"]) / 10
    # spritesの中のotherの中の～という風に一個ずつ[]を下に掘り下げていくという意味
    pokemon.img = pokeapi["sprites"]["other"]["official-artwork"]["front_default"]

    #日本語の名前取得
    names = pokeapi_species["names"]
    for name in names:
        if name["language"]["name"] == "ja":
            pokemon.ja_name = name["name"]
            break

    # 日本語のフレーバーテキスト取得
    flavor_text_entries = pokeapi_species["flavor_text_entries"]
    for text in flavor_text_entries:
        if text["language"]["name"] == "ja":
            pokemon.flavor_text = text["flavor_text"]
            break

    # 画像をダウンロード、インスタンスのimg属性をダウンロードした画像ファイルのパスに変更
    download_img(pokemon)
    return pokemon


# 画像のパス取得、インスタンスに設定
def download_img(pokemon: Pokemon): # （～：～）一個目は仮引数、２個目でクラス名or型名を書いて、その型しか取得しないようにしている
    # 同じファイル名があるか確認、無ければPokeApiから画像ダウンロード
    current_dir = os.path.dirname(__file__) # osモジュールの～、、dirnameでフォルダの絶対パス、（特殊変数）アンダーバー二つで実行しているファイルの絶対パス
    img_path = f"{current_dir}/img/{pokemon.en_name}.png"
    # 同名の画像ファイルが無ければダウンロードして保存
    if not os.path.isfile(img_path): # 事前に取得したパスがなければ～??
        image = requests.get(pokemon.img).content
        with open(img_path, "wb") as f:
            f.write(image)
    else:
        print("既にダウンロード済みのポケモン画像です")

    # ローカルの画像パスを設定
    pokemon.img = img_path