""" 日本地図上で都道府県間の関係性を可視化するプログラム

注: 正しく動作していません

このプログラムは、GeoPandasとjapanmapライブラリを使用して、以下の地理的関係性を視覚化します：
1. 東京都の位置（赤色で強調表示）
2. 東京都に隣接する都道府県（水色で表示）
3. 海岸線を持つ都道府県（緑色の境界線で強調）

処理の流れ：
1. 市区町村レベルの地理データ（シェープファイル）を読み込み
2. 都道府県レベルにデータを集約
3. 基本地図の描画（すべての都道府県を淡いグレーで表示）
4. 特定の関係性（隣接、海岸線の有無）に基づいて都道府県を色分け
5. 凡例とタイトルの追加

必要なライブラリ：
- geopandas: 地理データの処理と描画
- japanmap: 都道府県間の関係性（隣接、海岸線）の取得
- matplotlib: 描画の基本機能と凡例の作成
- japanize_matplotlib: 日本語フォントのサポート

入力データ：
- 'geodata/N03-23_230101.shp': 市区町村レベルの地理データを含むシェープファイル
  （国土数値情報の行政区域データ、令和5年1月1日時点）
  以下のサイトで取得してください。
  https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_1.html

出力：
- 都道府県の関係性を視覚化した日本地図
- 処理の各段階における進捗状況のコンソール出力

注意：
- シェープファイルの読み込みには一定の時間がかかる場合があります
- メモリ使用量が大きくなる可能性があるため、十分なリソースが必要です
- 地図の投影法は入力シェープファイルの設定に依存します
"""
import geopandas as gpd
import japanmap as jm
import matplotlib.pyplot as plt
# noinspection PyUnresolvedReferences
import japanize_matplotlib

print("データの読み込みを開始します...")
gdf = gpd.read_file('geodata/N03-23_230101.shp')
print("シェープファイルの読み込みが完了しました。データサイズ:", len(gdf))

print("\n投影法の設定を行います...")
gdf = gdf.to_crs(epsg=6677)
print("投影法の設定が完了しました")

print("\n描画の準備を開始します...")
fig, ax = plt.subplots(figsize=(15, 15))
ax.set_aspect('equal')
print("描画キャンバスを作成しました")

print("\n基本地図の描画を開始します...")
# 各都道府県を個別に処理して描画します
for pref_name in gdf['N03_001'].unique():
    mask = gdf['N03_001'] == pref_name
    # デフォルトは淡いグレー
    color = 'lightgray'

    # 東京都の場合は赤色
    if pref_name == '東京都':
        color = 'red'
    # 東京都の隣接県の場合は水色
    elif pref_name in [jm.pref_names[code] for code in jm.adjacent(13)]:
        color = 'skyblue'

    # 都道府県を描画
    gdf[mask].plot(
        ax=ax,
        color=color,
        edgecolor='white',
        linewidth=0.5
    )
print("基本地図の描画が完了しました")

print("\n海岸線を持つ都道府県の処理を開始します...")
sea_facing_count = 0
for code in range(1, 48):
    if jm.is_faced2sea(code):
        sea_facing_count += 1
        pref_name = jm.pref_names[code]
        mask = gdf['N03_001'] == pref_name
        gdf[mask].plot(ax=ax, facecolor='none', edgecolor='green', linewidth=1.5)
print(f"海岸線を持つ都道府県の処理が完了しました（該当都道府県数: {sea_facing_count}）")

print("\n凡例の追加を開始します...")
# 凡例を追加
from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor='red', edgecolor='white', label='東京都'),
    Patch(facecolor='skyblue', edgecolor='white', label='東京都に隣接'),
    Patch(facecolor='lightgray', edgecolor='green', linewidth=1.5, label='海に面している'),
    Patch(facecolor='lightgray', edgecolor='white', label='その他の都道府県')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=12)
print("凡例の追加が完了しました")

print("\n最終的な描画設定を行います...")
# タイトルの設定
plt.title('都道府県の関係性マップ\n(東京都の隣接県と海岸線を持つ都道府県)', pad=20, fontsize=16)
# 軸を非表示に
plt.axis('off')

print("\n地図の表示を開始します...")
plt.show()
print("処理が完了しました")