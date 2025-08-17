import streamlit as st

# Настройка страницы
st.set_page_config(page_title="Расчет почек", page_icon="🩺")
st.title("🩺 Калькулятор почечных показателей")


# Функция для клиренса креатинина
def calculate_clearance(age, weight, creatinine, is_male):
    if is_male:
        return (140 - age) * weight / (creatinine * 0.81)
    else:
        return (140 - age) * weight / (creatinine * 0.85)


# Функция для СКФ
def calculate_gfr(age, creatinine, is_male, is_black):
    k = 0.7 if not is_male else 0.9
    a = -0.329 if not is_male else -0.411
    race = 1.159 if is_black else 1.0
    cr_mgdl = creatinine / 88.4
    return 141 * race * (min(cr_mgdl / k, 1) ** a) * (max(cr_mgdl / k, 1) ** -1.209) * (0.993 ** age)


# Вкладки
tab1, tab2 = st.tabs(["Клиренс креатинина", "СКФ"])

# Вкладка клиренса
with tab1:
    st.write("### Расчет клиренса креатинина")

    age = st.number_input("Возраст (лет)", 18, 120, 50)
    weight = st.number_input("Вес (кг)", 30, 200, 70)
    creatinine = st.number_input("Креатинин (мкмоль/л)", 20, 2000, 80)
    is_male = st.radio("Пол", ["Мужской", "Женский"]) == "Мужской"

    if st.button("Рассчитать клиренс"):
        result = calculate_clearance(age, weight, creatinine, is_male)
        st.success(f"Клиренс креатинина: {result:.1f} мл/мин")

# Вкладка СКФ
with tab2:
    st.write("### Расчет СКФ (CKD-EPI)")

    age = st.number_input("Возраст", 18, 120, 50)
    creatinine = st.number_input("Креатинин", 20, 2000, 80)
    is_male = st.radio("Пол ", ["Мужской", "Женский"]) == "Мужской"
    is_black = st.radio("Раса", ["Европеоидная", "Негроидная"]) == "Негроидная"

    if st.button("Рассчитать СКФ"):
        result = calculate_gfr(age, creatinine, is_male, is_black)
        st.success(f"СКФ: {result:.1f} мл/мин/1.73м²")
