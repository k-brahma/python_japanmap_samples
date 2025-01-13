import japanmap as jm
import matplotlib.pyplot as plt
import pandas as pd

# サンプルデータを作成（実際のデータに置き換えてください）
data = {
    '市区町村コード': ['13101', '13102', '13103'],  # 千代田区、中央区、港区
    '値': [100, 200, 300]
}
df = pd.DataFrame(data)

# 地図に色付け
plt.figure(figsize=(15, 15))
jm.draw_municipalities(data=dict(zip(df['市区町村コード'], df['値'])))
plt.colorbar()
plt.show()