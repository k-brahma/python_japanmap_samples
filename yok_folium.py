"""横浜市の行政区域を可視化するインタラクティブ地図生成プログラム

このプログラムは国土数値情報から横浜市の行政区域データを取得し、インタラクティブな
Web地図を生成します。各区域はマウスオーバーで区名を確認できる形式で表示され、
結果はHTML形式で保存されます。

プログラムの動作の詳細:
1. データ取得とフィルタリング
  まず神奈川県全体の行政区域データを取得し、その中から横浜市の区だけを
  抽出します。これにより、横浜市18区の境界データを得ることができます。

2. 地図生成
  抽出したデータを基に、Foliumライブラリを使用してインタラクティブな地図を
  生成します。地図は以下の特徴を持ちます：
  - 横浜市の区域の重心を中心に表示
  - 各区は青色で塗りつぶされ、黒い境界線で区切られます
  - マウスオーバーで区名がポップアップ表示されます

3. 結果の出力
  - 生成した地図はHTML形式で保存されます
  - コンソールには横浜市の全区のリストが表示されます

技術的な実装詳細：
get_yokohama_wards関数:
   神奈川県の行政区域データから横浜市の区のみを抽出します。
   GeoPandasを使用してデータの読み込みとフィルタリングを行います。

create_yokohama_map関数:
   Foliumを使用してインタラクティブ地図を生成します。
   地図のスタイル設定や、ツールチップの設定を行います。

必要なライブラリ：
- os: ディレクトリ操作用
- folium: インタラクティブ地図の生成
- geopandas: 地理空間データの処理

入力データ：
- 国土数値情報の行政区域データ（N03-2022）
 URL: https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2022/N03-20220101_14_GML.zip

出力：
1. results/yokohama_wards.html
  - インタラクティブな地図を含むHTMLファイル
  - 青色で塗りつぶされた区域と区名のポップアップを含む
2. コンソール出力
  - 処理状況のメッセージ
  - 横浜市の区の一覧（五十音順）

注意事項：
1. プログラムの実行には安定したインターネット接続が必要です
2. 国土数値情報のデータ構造が変更された場合、フィルタリング条件の
  調整が必要になる可能性があります
3. resultsディレクトリが存在しない場合は自動的に作成されます
4. 実行時にはある程度の処理時間が必要です

エラーハンドリング：
- データ取得や地図生成時のエラーをtry-except文で捕捉
- エラーメッセージを具体的に表示し、デバッグを容易にします
"""
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
