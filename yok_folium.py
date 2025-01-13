import os

import folium
import geopandas as gpd

# 横浜市の行政区画GeoJSONを国土数値情報からダウンロード
# この例では神奈川県全体のデータを取得して横浜市の区だけをフィルタリングします
url = "https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2022/N03-20220101_14_GML.zip"


def get_yokohama_wards():
    # GeoDataFrameを作成
    gdf = gpd.read_file(url)

    # 横浜市の区だけをフィルタリング
    yokohama_wards = gdf[
        (gdf['N03_001'] == '神奈川県') &
        (gdf['N03_003'] == '横浜市')
        ]

    return yokohama_wards


# 地図を作成
def create_yokohama_map(gdf):
    # 横浜市の中心座標
    center_lat = gdf.geometry.centroid.y.mean()
    center_lon = gdf.geometry.centroid.x.mean()

    # 地図を初期化
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11
    )

    # 区ごとに色分けして表示
    folium.GeoJson(
        gdf,
        name='横浜市行政区',
        style_function=lambda feature: {
            'fillColor': '#3288bd',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['N03_004'],  # 区の名前を表示
            aliases=['区名'],
            style='background-color: white; color: #333333;'
        )
    ).add_to(m)

    return m


try:
    # 横浜市の区データを取得
    yokohama_wards = get_yokohama_wards()

    # 地図を作成
    m = create_yokohama_map(yokohama_wards)

    # mkdir if not exists
    os.makedirs('results', exist_ok=True)

    # 地図を保存
    m.save('results/yokohama_wards.html')
    print("地図を 'results/yokohama_wards.html' として保存しました。")

    # 区の一覧を表示
    print("\n横浜市の区一覧:")
    for ward in sorted(yokohama_wards['N03_004'].unique()):
        print(f"- {ward}")

except Exception as e:
    print(f"エラーが発生しました: {e}")
