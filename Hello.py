import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import random


#@st.cache_resource(ttl=600)
def get_data(t="ABC Inc.", n=15):
    points = np.random.randn(n+1, 2) / [50, 50] + [31.9591, 34.8021]
    sample = []
    for i in range(len(points)):
        point =  points[i].tolist()
        sample.append({'STORE': "{}".format(t),'RELEVANCE': random.randint(1, 100), 'LAT': point[0], 'LON': point[1]})
    return pd.DataFrame(sample)

def make_colors(rgb:str):
    color = []
    for i in (0, 2, 4):
        decimal = int(rgb[i:i+2], 16)
        color.append(decimal)
    start_color = color.copy()
    start_color.append(0)
    full_color= color.copy()
    full_color.append(255)
    return[start_color, full_color]


def make_layer(data, color):
    return pdk.Layer(
        "ScatterplotLayer",
        data,
        get_position=['LON', 'LAT'],
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=1,
        radius_max_pixels=100,
        get_fill_color=make_colors(color)[1],
        get_line_color=[0, 0, 0]
    )

st.markdown("# Golden Maps")
st.markdown("## The Money in a map.") 
st.markdown("### Here you can find where the real money is in your area.")
#st.map(get_stores_data(), size=.1)
gold_data = get_data(t="Gold Jewelry", n=7)
silver_data = get_data(t="Silver Market", n=3)
change_data = get_data(t="Currency Change", n=13)
clothing_data = get_data(t="Elegant Clothing", n=6)
watch_data = get_data(t="Luxury Watch Store", n=4)
bank_data = get_data(t="Bank Agency", n=7)
car_data = get_data(t="Car Seller", n=9)
sushi_data = get_data(t="Sushi Restaurant", n=7)

full_data = pd.concat([gold_data, silver_data, change_data, clothing_data, watch_data, bank_data, car_data, sushi_data])

gold_layer = make_layer(gold_data, "d3af37")
silver_layer = make_layer(silver_data, "c0c0c0")
change_layer = make_layer(change_data, "c0fa0")
clothing_layer = make_layer(clothing_data, "fac0c0")
watch_layer = make_layer(watch_data, "006039")
bank_layer = make_layer(bank_data, "79a471")
car_layer = make_layer(car_data, "c0c0fa")
sushi_layer = make_layer(sushi_data, "fa8072")
#get_radius
full_layer = pdk.Layer(
        "HeatmapLayer",
        full_data,
        get_position=['LON', 'LAT'],
        #aggregation=pdk.types.String("MEAN"),
        color_range=make_colors('fa1111'),
        get_weight="RELEVANCE",
    )

st.pydeck_chart(pdk.Deck(
    layers=[full_layer, gold_layer, silver_layer, change_layer, clothing_layer, watch_layer, bank_layer, car_layer, sushi_layer],
    initial_view_state=pdk.ViewState(
        latitude=31.9591,
        longitude=34.8021,
        zoom=11,
    ),
    tooltip={'text':'{STORE} #{RELEVANCE}'}
))
#st.dataframe(full_data)
st.markdown("[Desinged by Golden Cash in Israel](https://goldencash.co.il/)")