import pandas as pd
import folium
from folium import plugins

# マーカープロット
RADIUS = 3

df = pd.read_csv('./2019/data/honhyo_2019.csv', encoding="cp932", index_col=0)
df = df[df['都道府県コード'].isin([30, 40, 41, 42, 43, 44, 45])]  # 千葉県

# df = df.astype({"発生日時　　年": str, "発生日時　　月": str, "発生日時　　日": str, "発生日時　　時": str, "発生日時　　分": str,})
# df["Datetime"] = pd.to_datetime(df["発生日時　　年"]+"-"+df["発生日時　　月"]+"-"+df["発生日時　　日"]+"T"+df["発生日時　　時"]+":"+df["発生日時　　分"])


def dms2deg(df, col):
    df2 = df.copy()
    df2["d"], df2["t"] = df2[col].divmod(10000000)
    df2["m"], df2["s"] = df2['t'].divmod(100000)
    converted = df2["d"] + (df2["m"] / 60.0) + (df2["s"] / 1000.0 / 3600.0)
    return converted


df['lat'] = 0
df['lon'] = 0

df['lat'] = dms2deg(df, '地点　緯度（北緯）')
df['lon'] = dms2deg(df, '地点　経度（東経）')

m = folium.Map(
        tiles="cartodb positron",
        location=[35.6807825, 139.7646601],
        zoom_start=10
    )

map = folium.Map(
        tiles="cartodb positron",
        location=[35.6807825, 139.7646601],
        zoom_start=10
    )

ys = [ys for ys in df["lat"]]
xs = [xs for xs in df["lon"]]

zipped = zip(ys, xs)
heat_data = [list(i) for i in list(zipped)]

folium.plugins.HeatMap(
    data=heat_data,
    radius=25,
    blur=25,
    max_opacity=1
).add_to(map)

map.save("./2019/map/heat_map_2019.html")

for i, row in df.iterrows():
    if row["地点　経度（東経）"] != "0000000000":

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            popup=[row["lat"], row["lon"]],
            radius=RADIUS,
            color="red",
            stroke=False,
            fill=True,
            fill_opacity=0.75,
            opacity=1,
            # tooltip="accident",
        ).add_to(m)

m.save("./2019/map/map_2019.html")
