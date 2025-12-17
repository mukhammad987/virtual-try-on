import streamlit as st
import replicate

st.title("Виртуальная примерка одежды")

# Ввод API-токена
api_token = st.text_input("Введите ваш Replicate API Token", type="password")
if not api_token:
    st.warning("Введите API-токен для работы с Replicate.")
else:
    client = replicate.Client(api_token=api_token)

    # Загрузка фото
    human_file = st.file_uploader("Загрузите фото человека", type=["jpg", "png", "jpeg"])
    garment_file = st.file_uploader("Загрузите фото одежды", type=["jpg", "png", "jpeg"])

    # Дополнительные параметры
    description = st.text_input("Описание одежды (например, 'белая блузка')", value="a model wearing the garment")
    category = st.selectbox("Категория одежды", options=["upper_body", "lower_body", "dresses"])

    if human_file and garment_file:
        if st.button("Примерить"):
            with st.spinner("Генерация изображения... (это может занять 20-60 секунд)"):
                try:
                    # Параметры для модели (основаны на документации IDM-VTON)
                    input_dict = {
                        "human_img": human_file,      # Фото человека
                        "garm_img": garment_file,     # Фото одежды
                        "mask_img": None,             # Маска (автогенерация, если None)
                        "garment_des": description,   # Описание одежды
                        "category": category,         # Категория
                        "crop": False,                # Обрезать ли изображения
                        "steps": 30,                  # Количество шагов диффузии
                        "seed": -1                    # Сид (-1 для случайного)
                    }

                    # Запуск модели
                    output = client.run(
                        "cuuupid/idm-vton:0aee68c6e6753e4722d362678c927ff91e2e5a7fe7312dc87fb5b2ccc35b277d",
                        input=input_dict
                    )

                    # Вывод результата (модель возвращает URL изображения)
                    if isinstance(output, str):
                        st.image(output, caption="Результат примерки")
                    elif isinstance(output, list) and output:
                        st.image(output[0], caption="Результат примерки")
                    else:
                        st.error("Неожиданный формат вывода. Проверьте результат: " + str(output))
                except Exception as e:
                    st.error(f"Ошибка при генерации: {str(e)}. Проверьте токен, параметры или кредиты на Replicate.")
    else:
        st.info("Загрузите оба фото, чтобы появилась кнопка 'Примерить'.")
