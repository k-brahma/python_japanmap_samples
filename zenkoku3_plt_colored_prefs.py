"""都道府県を異なる色で表示する日本地図生成プログラム

このプログラムは、japanmapライブラリを使用して日本の都道府県地図を生成し、各都道府県を
視覚的に区別しやすい異なる色で表示します。HSV色空間を活用することで、色相（Hue）を
均等に分配し、各都道府県を明確に識別できる配色を実現しています。

プログラムの主な特徴：
1. 色生成システム
  - HSV色空間を使用して47都道府県分の異なる色を生成
  - 彩度（Saturation）0.7と明度（Value）0.9に固定し、視認性を確保
  - 色相を0から1の間で均等に分配し、近隣の都道府県でも区別しやすい配色を実現

2. フォント設定
  - 日本語表示のためにMS Gothicフォントを使用（Windows環境向け）
  - プログラム実行環境に応じてフォント設定の調整が必要な場合があります

3. 地図生成と表示
  - japanmapライブラリのpicture関数を使用して地図データを生成
  - matplotlibを使用して15x15インチのサイズで表示
  - 軸を非表示にし、見やすい地図表示を実現

技術的な詳細：
generate_colors関数の仕組み:
- 入力値nに基づいて、n個の異なる色を生成
- 各色はHSV色空間でまず定義され、その後RGBに変換
- 出力は都道府県コード（1-47）をキーとする色コード（#RRGGBB形式）の辞書

必要なライブラリ：
- japanmap: 日本地図の基本データと描画機能
- matplotlib: 地図の表示とカスタマイズ
- colorsys: HSV-RGB色空間の変換
- matplotlib.font_manager: 日本語フォントの管理

出力：
- 47都道府県が異なる色で表示された日本地図
- タイトル「日本の都道府県地図」を含む
- ウィンドウサイズ15x15インチの図

注意事項：
1. フォント設定はWindowsを想定しています。他のOSでは適切なフォントに変更が必要です
2. 色の生成には決定論的なアルゴリズムを使用しているため、
  プログラムを実行するたびに同じ配色になります
3. 色覚多様性への配慮が必要な場合は、彩度や明度の調整を検討してください
"""
import japanmap as jm
import matplotlib.pyplot as plt
import colorsys
# noinspection PyUnresolvedReferences
from matplotlib import font_manager

# 日本語フォントの設定
plt.rcParams['font.family'] = 'MS Gothic'  # Windowsの場合

# 都道府県ごとに異なる色を生成
def generate_colors(n):
    colors = {}
    for i in range(n):
        hue = i / n
        rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        color = "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        colors[i + 1] = color
    return colors

# 都道府県コードと色の対応を作成
color_dict = generate_colors(47)

# 地図を生成
map_image = jm.picture(color_dict)

# 地図を描画
plt.figure(figsize=(15, 15))
plt.imshow(map_image)
plt.title("日本の都道府県地図", fontsize=16)
plt.axis('off')
plt.show()