"""シェープファイルから日本の行政区域地図を生成・可視化するプログラム

このプログラムは、国土数値情報が提供する行政区域データ（シェープファイル）を読み込み、
日本地図を生成・可視化します。さらに、入力データをGeoJSON形式に変換して保存します。

主な機能：
1. 行政区域データの読み込みと基本構造の確認
  - シェープファイルからデータを読み込み
  - データフレームの列構造の表示
  - 先頭数行のデータ内容の確認

2. 地図の可視化
  - 都道府県レベルでのデータの集約（dissolveメソッドを使用）
  - 境界線と塗りつぶしの設定による視覚的な表現
  - タイトルの追加と軸の非表示化による見た目の調整

3. データの変換と保存
  - 読み込んだデータをGeoJSON形式に変換
  - 変換したデータの保存

技術的な詳細：
- データ集約: dissolveメソッドを使用して市区町村データを都道府県レベルに集約
- 描画設定:
 - 境界線: 黒色（black）、線の太さ0.5
 - 塗りつぶし: 薄いグレー（lightgray）
 - 図のサイズ: 15x15インチ

必要なライブラリ：
- geopandas: 地理空間データの処理と地図の描画
- matplotlib.pyplot: 描画機能の基本設定
- japanize_matplotlib: 日本語フォントのサポート

入力ファイル：
- 'geodata/N03-23_230101.shp': 令和5年1月1日時点の行政区域データ（シェープファイル）

出力ファイル：
- 'geodata/N03-23_230101.geojson': 変換後のGeoJSONファイル

注意事項：
- シェープファイルの読み込みには一定の処理時間が必要
- GeoJSONへの変換時にファイルサイズが大きくなる可能性あり
- 出力ファイルと同名のファイルが存在する場合は上書きされます

実行時の出力：
- データフレームの構造（列名）
- データの先頭数行
- 処理の進行状況
- 最終的な地図の表示
"""
import geopandas as gpd
# noinspection PyUnresolvedReferences
import japanize_matplotlib
import matplotlib.pyplot as plt

# シェープファイルを読み込みます
# GeoJSONとシェープファイルのどちらでも読み込めますが、シェープファイルの方が一般的に処理が速いです
gdf = gpd.read_file('geodata/N03-23_230101.shp')

# データの基本的な構造を確認します
print("データフレームの構造:")
print(gdf.columns)
print("\n最初の数行のデータ:")
print(gdf.head())

print("描画開始")

# シンプルな地図を描画します
fig, ax = plt.subplots(figsize=(15, 15))
print("描画中...")

# 都道府県ごとに色分けして描画
gdf.dissolve(by='N03_001').plot(
    ax=ax,
    edgecolor='black',  # 境界線の色
    linewidth=0.5,  # 境界線の太さ
    color='lightgray',  # 塗りつぶしの色
)
print("dispolve by N03_001")

# 見た目の調整
plt.title('日本地図（都道府県別）', pad=20, fontsize=16)
plt.axis('off')  # 軸を非表示に
print("title and axis off")

plt.show()
print("描画完了")

# results に保存します
gdf.to_file(
    'results/N03-23_230101.geojson',
    driver='GeoJSON',
    encoding='utf-8'  # エンコーディングを明示的に指定
)
print("GeoJSONファイルを保存しました")
