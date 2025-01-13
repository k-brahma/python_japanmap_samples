import japanmap as jm
import matplotlib.pyplot as plt
import colorsys
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