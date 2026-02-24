
















import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# ==========================
# CONFIGURACIÓN INICIAL
# ==========================

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="🦉 Fukuro AI",
    page_icon="🦉",
    layout="centered"
)

st.title("🦉 Fukuro AI — Tu compañero inteligente de viajes")
st.markdown(
    "Hola ✨ Soy **Fukuro 🦉**, tu robot búho viajero.\n"
    "Contame qué tipo de viaje soñás y exploramos el mundo juntos 🌍"
)

# ==========================
# BOTÓN NUEVA CONVERSACIÓN
# ==========================

if st.button("🔄 Nueva conversación"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Eres Fukuro, un robot búho inteligente, tierno y sabio. "
                "Eres el compañero de viajes del usuario. "
                "Recomiendas destinos según presupuesto, temporada, estilo o vibe. "
                "Hablas con calidez, entusiasmo y cercanía. "
                "Para cada sugerencia incluye:\n"
                "- Destino\n"
                "- Por qué es ideal\n"
                "- 1 o 2 actividades clave\n"
                "Usa emojis ocasionalmente y mantén un tono amigable y aventurero."
            )
        }
    ]
    st.rerun()

# ==========================
# MEMORIA DE SESIÓN
# ==========================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Eres Fukuro, un robot búho inteligente, tierno y sabio. "
                "Eres el compañero de viajes del usuario. "
                "Recomiendas destinos según presupuesto, temporada, estilo o vibe. "
                "Hablas con calidez, entusiasmo y cercanía. "
                "Para cada sugerencia incluye:\n"
                "- Destino\n"
                "- Por qué es ideal\n"
                "- 1 o 2 actividades clave\n"
                "Usa emojis ocasionalmente y mantén un tono amigable y aventurero."
            )
        }
    ]

# ==========================
# MOSTRAR HISTORIAL
# ==========================

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================
# INPUT DEL USUARIO
# ==========================

if prompt := st.chat_input("¿A dónde querés viajar? ✈️"):

    # Guardar mensaje usuario
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamada a OpenAI
    limited_messages = [st.session_state.messages[0]] + st.session_state.messages[-6:]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # Guardar respuesta
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)

# ==========================
# BOTÓN GUARDAR HISTORIAL
# ==========================

if st.button("💾 Guardar conversación"):
    filename = f"historial_fukuro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)

    st.success(f"Conversación guardada como {filename}")
