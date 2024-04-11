from io import BytesIO

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from PIL import Image

import main


# Placeholder for your model (Replace this with your actual model)
def predict(bytes):
    # Example dictionary for prediction probabilities
    predictions = requests.post("http://158.160.138.228:8000/api/v1/classify-image", files={"image": bytes},
                                params={"city": open('city', 'r').read()}).json()
    predictions = pd.DataFrame(predictions['predicts'])
    predictions['longitude'] = predictions['coordinates'].apply(lambda x: x['longitude'])
    predictions['latitude'] = predictions['coordinates'].apply(lambda x: x['latitude'])
    return predictions


st.title('Предсказание достопримечательности по фото')

uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    if st.button('Predict'):
        # Download the image
        img_bytes = BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        st.download_button(label='Download Image', data=img_bytes, file_name='predicted_image.png', mime='image/png')

        predictions = predict(img_bytes)

        # Plot the prediction probabilities
        fig = px.bar(predictions, x='probability')
        st.write(fig)

        fig = px.scatter_mapbox(predictions,
                                lat='latitude',
                                lon='longitude',
                                size='probability',
                                zoom=10,
                                hover_name='name',
                                color='category')
        fig.update_layout(mapbox_style="open-street-map", height=800)
        st.plotly_chart(fig, use_container_width=True, height=800)
