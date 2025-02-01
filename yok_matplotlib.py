"""横浜市の行政区域を静的地図として可視化するプログラム

このプログラムは、国土数値情報から横浜市の行政区域データを取得し、各区を異なる色で表現した
静的な地図を生成します。matplotlibを使用して、区ごとの境界を明確に示し、凡例付きの
見やすい地図を作成します。

プログラムの動作プロセス：
まず、国土数値情報から神奈川県全体の行政区域データを取得します。このデータには県内の
すべての市区町村の境界情報が含まれています。次に、データフィルタリングを行い、横浜市の
区のみを抽出します。最後に、matplotlibを使用して各区を異なる色で表現し、区名を凡例として
表示します。

地図の表示特徴：
- 15x15インチの大きなサイズで表示され、詳細な境界線が見やすくなっています
- 各区は自動的に異なる色が割り当てられ、視覚的な区別が容易です
- 黒い境界線（線幅1）により、区の境界が明確に表示されます
- 区名の凡例は地図の右側に配置され、各色と区名の対応が分かります

技術的な実装の詳細：
- GeoPandasのplot機能を使用して地理データを視覚化します
- 'N03_004'列（区名）を基準に自動的に色分けを行います
- 凡例は地図の右側（bbox_to_anchor=(1.3, 1)）に配置され、すべての区名が見やすく表示されます
- tight_layout()を使用して、凡例と地図が重ならないように自動調整されます

必要なライブラリ：
- geopandas: 地理空間データの処理と地図描画
- matplotlib: 描画のカスタマイズと全体レイアウトの調整
- matplotlib.font_manager: 日本語フォントの管理

入力データ：
国土数値情報の行政区域データ（N03-2022）
URL: https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2022/N03-20220101_14_GML.zip

出力：
matplotlibウィンドウに表示される静的な地図
- タイトル「横浜市行政区地図」
- 各区が異なる色で表示
- 区名を示す凡例付き

注意事項：
1. MS Gothicフォントを使用するため、Windows環境を前提としています
2. 他のOSで実行する場合は、適切な日本語フォントに設定を変更する必要があります
3. データのダウンロードには安定したインターネット接続が必要です
4. 凡例の位置は、ディスプレイのサイズや解像度によって調整が必要になる場合があります
"""
import geopandas as gpd
import matplotlib.pyplot as plt
# noinspection PyUnresolvedReferences
from matplotlib import font_manager

# 日本語フォント設定
plt.rcParams['font.family'] = 'MS Gothic'

# 神奈川県のデータを読み込み
url = "https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2022/N03-20220101_14_GML.zip"
gdf = gpd.read_file(url)

# 横浜市の区だけをフィルタリング
yokohama_wards = gdf[
    (gdf['N03_001'] == '神奈川県') &
    (gdf['N03_003'] == '横浜市')
    ]

# matplotlib で描画
fig, ax = plt.subplots(figsize=(15, 15))
yokohama_wards.plot(
    ax=ax,
    column='N03_004',  # 区名で色分け
    legend=True,
    legend_kwds={'bbox_to_anchor': (1.3, 1)},
    edgecolor='black',
    linewidth=1
)

# タイトルと軸ラベルを設定
plt.title('横浜市行政区地図', fontsize=16)
ax.axis('off')
plt.tight_layout()
plt.show()
