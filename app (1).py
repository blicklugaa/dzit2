import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Фоторедактор", page_icon="🎨")
st.title("Фоторедактор")

uploaded = st.file_uploader("Завантаж фото", type=["jpg", "jpeg", "png"])

options = [
    "Оригінал",
    "Чорно-біле",
    "Розмиття",
    "Контури",
    "Сепія",
    "Віддзеркалення",
    "Налаштування яскравості",
    "Налаштування контрасту",
    "Колірний сплеск",
]
filter_option = st.sidebar.selectbox("Обери фільтр", options)

if uploaded is not None:
    img_array = np.array(Image.open(uploaded).convert("RGB"))
    result = img_array

    if filter_option == "Чорно-біле":
        result = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    elif filter_option == "Розмиття":
        result = cv2.GaussianBlur(img_array, (15, 15), 0)

    elif filter_option == "Контури":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        result = cv2.Canny(gray, 100, 200)

    elif filter_option == "Сепія":
        kernel = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131],
        ])
        result = np.clip(cv2.transform(img_array, kernel), 0, 255).astype(np.uint8)

    elif filter_option == "Віддзеркалення":
        result = cv2.flip(img_array, 1)

    elif filter_option == "Налаштування яскравості":
        brightness_val = st.sidebar.slider("Рівень яскравості", -100, 100, 0)
        result = cv2.convertScaleAbs(img_array, alpha=1.0, beta=brightness_val)

    elif filter_option == "Налаштування контрасту":
        contrast_val = st.sidebar.slider("Рівень контрасту", 0.5, 3.0, 1.0, step=0.1)
        result = cv2.convertScaleAbs(img_array, alpha=contrast_val, beta=0)

    elif filter_option == "Колірний сплеск":
        color = st.sidebar.selectbox("Колір, який залишити", ["Червоний", "Зелений", "Синій"])
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

        if color == "Червоний":
            mask1 = cv2.inRange(hsv, np.array([0, 50, 50]), np.array([10, 255, 255]))
            mask2 = cv2.inRange(hsv, np.array([170, 50, 50]), np.array([180, 255, 255]))
            mask = cv2.bitwise_or(mask1, mask2)
        elif color == "Зелений":
            mask = cv2.inRange(hsv, np.array([35, 50, 50]), np.array([85, 255, 255]))
        else:
            mask = cv2.inRange(hsv, np.array([100, 50, 50]), np.array([130, 255, 255]))

        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        result = np.where(mask[:, :, None] > 0, img_array, gray_rgb)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Оригінал")
        st.image(img_array, use_container_width=True)
    with col2:
        st.subheader("Результат")
        st.image(result, use_container_width=True)
else:
    st.info("Завантаж фото, щоб почати")
