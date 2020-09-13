import flaski.database
import http.client, urllib.request, urllib.parse, urllib.error, base64
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import requests
import json
import os


base_url = '<API URL>'
prediction_key = '<Key>'
POKEMON_FOLDER =  './static/images/pokemon/'

# 予測確率のしきい値（パーセント）
threshold = 60

# ポケモン情報をDBから取得し辞書型で返す
def get_pokemon_data(pokemonname):
    ses = flaski.database.db_session()
    pokemon = flaski.database.Pokemon
    pokemon_data = ses.query(pokemon).filter(pokemon.pokemon_name == pokemonname).first()

    pokemon_data_dict = {}
    if not pokemon_data is None:
        pokemon_data_dict['pokemon_name'] = pokemon_data.pokemon_name
        pokemon_data_dict['type']     = pokemon_data.type
        pokemon_data_dict['wiki_url']        = pokemon_data.wiki_url
        pokemon_data_dict['picture_path']    = os.path.join(POKEMON_FOLDER, pokemon_data.pokemon_name + '.png')

    return pokemon_data_dict

# モデルAPIの呼び出し
def callAPI(uploadFile):
    # 予測実行
    headers = {
        'Content-Type': 'application/json',
        'Prediction-Key': prediction_key
    }
    params = {}
    predicts = {}
    data = open(uploadFile, 'rb').read()
    response = requests.post(base_url, headers=headers, params=params, data=data)
    response_list = json.loads(response.text)
    result = []

    try:
        # 予測結果のタグの数だけループ　…③
        for prediction in response_list['predictions']:
            if len(get_pokemon_data(prediction['tagName'])) != 0:
            # 確率がしきい値より大きいものを採用する
                if prediction['probability'] * 100 > threshold:
                    result.append(get_pokemon_data(prediction['tagName']))
        return result

    #画像サイズ > 6MB だとCustom Vision の制限にひっりエラーが出るまで握り潰し
    except KeyError:
        return result


