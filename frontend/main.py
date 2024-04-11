import streamlit as st

PLACES_TO_VISIT = set()

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
from st_pages import Page, show_pages

show_pages(
    [
        Page("main.py", "Главная", "🏠"),
        Page("pages/photo2place.py", "Поиск достопримечательности по фотографии", "🖼️"),
        Page("pages/text2place.py", "Поиск достопримечательности по тексту", icon="🔎"),
        Page("pages/navigation.py", "Построение маршрута", icon="🌎")
    ]
)

st.sidebar.success("Выберите сценарий")

st.markdown(
    """
    # МИСИС прогрев градиентов
    ## Решение НТО Компьютерное зрение
    """
)

city = st.radio("Выберите город", ["Нижний Новгород", "Ярославль", "Владимир", "Екатеринбург"])

st.markdown("### Навигация")

st.page_link("main.py", label="Главная", icon="🏠")
st.page_link("pages/photo2place.py", label="Поиск достопримечательности по фотографии", icon="1️⃣")
st.page_link("pages/text2place.py", label="Поиск достопримечательности по тексту", icon="2️⃣", )
st.page_link("pages/navigation.py", label="Построение маршрута", icon="🌎")

if __name__=='__main__':
    CITY = {'Нижний Новгород': 'nizhniy_novgorod',
            'Ярославль': 'yaroslavl',
            'Владимир': 'vladimir',
            'Екатеринбург': 'ekatirinburg'
            }[city]
    open('city', 'w').write(CITY)
