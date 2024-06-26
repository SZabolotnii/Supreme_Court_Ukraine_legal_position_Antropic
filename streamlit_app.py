import streamlit as st
from anthropic import Anthropic
import os

# Налаштування Anthropic клієнта
antehropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Системний промпт
SYSTEM_PROMPT = """
You are a qualified lawyer tasked with creating a \"legal position\" based on a decision of the Supreme Court of Ukraine.
"""

# Приклад legal position
EXAMPLE_LEGAL_POSITION = """
Про умову для виникнення в особи права призначення пенсії за віком зі зниженням пенсійного віку на 6 років відповідно до вимог частини першої статті 55 Закону № 796.

Аналіз статті 55 Закону України «Про статус і соціальний захист громадян, які постраждали внаслідок Чорнобильської катастрофи» дає підстави для висновку, що умовою для виникнення в особи права на призначення пенсії зі зменшенням пенсійного віку відповідно до абзацу 5 пункту 2 частини першої статті 55 цього Закону є факт проживання та (або) праці такої особи у зоні гарантованого добровільного відселення протягом трьох років до 01 січня 1993 року. Початкова величина зменшення пенсійного віку (3 роки) встановлюється лише особам, які постійно проживали або постійно працювали у зазначених зонах з моменту аварії по 31 липня 1986 року незалежно від часу проживання або роботи в цей період. Додатково такі особи мають право на зменшення пенсійного віку на 1 рік за 2 роки проживання, роботи на відповідній місцевості. При цьому максимальна межа зниження пенсійного віку відповідно до положень абзацу 5 пункту 2 частини першої статті 55 Закону становить 6 років, незалежно від того застосовувалась початкова величина зменшення пенсійного віку до таких осіб чи ні.
"""

# Функція для отримання відповіді від API
def get_ai_response(supreme_court_decision):
    prompt = f"""
Here's an example of a legal position from another decision:

<example_legal_position>
{EXAMPLE_LEGAL_POSITION}
</example_legal_position>

Now, you will be given a Supreme Court decision. Your task is to create a legal position based on this decision:

<supreme_court_decision>
{supreme_court_decision}
</supreme_court_decision>

To create the legal position:
1. Carefully read and analyze the Supreme Court decision.
2. Identify the key legal principle or ruling established in the decision.
3. Summarize this principle concisely, focusing on its legal implications.
4. Ensure your summary is clear, precise, and uses appropriate legal terminology.

Format your legal position following these guidelines:
- Keep it brief, ideally no more than 3-4 sentences.
- Use the same style and tone as the example provided.
- Do not include any additional explanations or comments.
- Use the original language of the decision.

Write your legal position inside <legal_position> tags. Do not include any other text or explanations outside these tags.
"""

    message = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return message.content

# Налаштування сторінки
st.set_page_config(page_title="Legal Position Generator", page_icon="⚖️")

# Заголовок додатку
st.title("⚖️ Legal Position Generator")

# Текстове поле для вводу
SUPREME_COURT_DECISION = st.text_area("Введіть текст рішення Верховного Суду:", height=300)

# Кнопка для обробки
if st.button("Генерувати правову позицію"):
    if SUPREME_COURT_DECISION:
        with st.spinner('Аналіз рішення та генерація правової позиції ...'):
            try:
                response = get_ai_response(SUPREME_COURT_DECISION)
                st.subheader("Правова позиція:")
                st.write(response)
            except Exception as e:
                st.error(f"Виникла помилка при обробці запиту: {str(e)}")
    else:
        st.warning("Будь ласка, введіть текст рішення для аналізу.")

# Додаткова інформація
st.sidebar.header("Про додаток")
st.sidebar.info(
    "Цей додаток використовує AI для аналізу рішень Верховного Суду "
    "та генерації правових позицій на їх основі. Введіть текст рішення "
    "у поле вводу і натисніть 'Генерувати правову позицію', щоб отримати результат."
)

# Футер
st.sidebar.text("Розроблено з ❤️ за допомогою Streamlit")