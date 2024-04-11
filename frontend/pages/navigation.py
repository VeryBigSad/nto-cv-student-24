import json
import math
from itertools import permutations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from st_pages import Page, show_pages

import main

show_pages(
    [
        Page("main.py", "Главная", "🏠"),
        Page("pages/photo2place.py", "Поиск достопримечательности по фотографии", "🖼️"),
        Page("pages/text2place.py", "Поиск достопримечательности по тексту", icon="🔎"),
        Page("pages/navigation.py", "Построение маршрута", icon="🌎")
    ]
)


def distance(point1, point2):
    lat1, lon1 = point1['Lat'], point1['Lon']
    lat2, lon2 = point2['Lat'], point2['Lon']
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)


def total_distance(route, points):
    dist = 0
    for i in range(len(route) - 1):
        dist += distance(points[route[i]], points[route[i + 1]])
    return dist


def make_route(points):
    n = len(points)
    best_distance = float('inf')
    best_route = []

    for perm in permutations(range(n), n):
        route = list(perm)
        route.append(route[0])  # Return to the starting point
        current_distance = total_distance(route, points)

        if current_distance < best_distance:
            best_distance = current_distance
            best_route = route

    return [points[i] for i in best_route[:-1]][:5]


def make_payload(waypoints):
    payload = []
    for i, waypoint in enumerate(waypoints):
        # if i == 0:
        #     payload.append({
        #         'type': 'stop',
        #         # 'start': True,
        #         'lat': waypoint['Lat'],
        #         'lon': waypoint['Lon']
        #     })
        # elif i == len(waypoint):
        #     payload.append({
        #         'type': 'stop',
        #         'lat': waypoint['Lat'],
        #         'lon': waypoint['Lon']
        #     })
        #
        # else:
        payload.append({
            'type': 'stop',
            'lat': waypoint['Lat'],
            'lon': waypoint['Lon']
        })
    return payload


st.markdown('# Построение маршрута по выбранным местам')

if len(main.PLACES_TO_VISIT) == 0:
    st.write("Отметьте несколько мест для посещения")
elif len(main.PLACES_TO_VISIT) == 1:
    st.write('Отметьте еще несколько мест')
else:
    waypoints = []
    for place in main.PLACES_TO_VISIT:
        waypoints.append(requests.get(f'http://158.160.138.228:8000/api/v1/get-by-id/{place}').json())
        waypoints[-1].update({'xid': place})

    df = pd.DataFrame(waypoints)[['Name', 'xid']]
    df['images'] = df['xid'].apply(lambda xid: f"https://storage.yandexcloud.net/misis-progrev-gradientov/{xid}.jpg")

    table = st.data_editor(
        df,
        column_config={
            "Name": st.column_config.Column(
                "Выбранное место",
                width="medium",
                required=True,
            ),
            "images": st.column_config.ImageColumn(
                "Фотография"
            ),
        },
        hide_index=True,
    )

    waypoints = make_route(waypoints)
    print(len(waypoints))

    payload = json.dumps({
        "points": make_payload(waypoints),
        "transport": "pedestrian",
        "route_mode": "fastest"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    url = "http://routing.api.2gis.com/routing/7.0.0/global?key=554209b9-432a-4228-9c3e-dceb2e1c8a9f"

    response = requests.request("POST", url, headers=headers, data=payload).json()
    big_ass_string = ', '.join(
        [i['selection'][11:-1] for i in response['result'][0]['maneuvers'][0]['outcoming_path']['geometry']]
    )
    points = big_ass_string.split(', ')
    points = [tuple(float(j) for j in i.split()) for i in points]

    df = pd.DataFrame(points, columns=['Широта', 'Долгота'])

    fig = px.scatter_mapbox(df,
                            lon='Широта',
                            lat='Долгота',
                            zoom=15)
    for i, point in enumerate(points):
        lon, lat = point
        if i != 0:
            fig.add_trace(go.Scattermapbox(mode="lines",
                                           lon=[points[i - 1][0], points[i][0]],
                                           lat=[points[i - 1][1], points[i][1]],
                                           line_color='blue'))
    fig.update_layout(mapbox_style="open-street-map", height=800, showlegend=False)

    if st.button('Построить маршрут'):
        st.plotly_chart(fig, use_container_width=True, height=800)
        main.PLACES_TO_VISIT = set()
