import geopandas as gpd
import matplotlib.pyplot as plt
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
