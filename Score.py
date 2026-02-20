import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Questionnaire", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    
    /* Style des boîtes de sélection (Radio) avec un fond gris très clair pour le contraste */
    .stRadio > div {flex-direction: column; gap: 12px;}
    div[data-testid="stRadio"] > div {
        background-color: #f4f4f4 !important; 
        padding: 15px; 
        border-radius: 12px; 
        border: 2px solid #cccccc !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
    }
    /* Texte des choix forcé en NOIR */
    div[data-testid="stRadio"] * {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: 600;
    }
    
    /* Bouton Sauvegarder (Fond rouge, police blanche) */
    div[data-testid="stButton"] > button {
        height: 60px; 
        border-radius: 12px; 
        font-size: 20px !important; 
        font-weight: bold; 
        background-color: #d32f2f !important; 
        border: 2px solid #b71c1c !important;
        box-shadow: 0px 4px 10px rgba(211, 47, 47, 0.3);
        transition: 0.3s;
        width: 100%;
    }
    div[data-testid="stButton"] > button, 
    div[data-testid="stButton"] > button *, 
    div[data-testid="stButton"] > button p {
        color: #ffffff !important;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #b71c1c !important;
        border-color: #9b0000 !important;
    }
    
    /* Bouton Télécharger (Fond noir, police blanche) */
    div[data-testid="stDownloadButton"] > button {
        height: 60px; 
        border-radius: 12px; 
        font-size: 20px !important; 
        font-weight: bold; 
        background-color: #000000 !important; 
        border: 2px solid #000000 !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        transition: 0.3s;
        width: 100%;
    }
    div[data-testid="stDownloadButton"] > button, 
    div[data-testid="stDownloadButton"] > button *, 
    div[data-testid="stDownloadButton"] > button p {
        color: #ffffff !important;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background-color: #333333 !important;
        border-color: #333333 !important;
    }
    
    h1, h2, h3, h4 {
        color: #d32f2f !important;
        font-weight: 800 !important;
    }
    p, label, .stSelectbox label {
        color: #000000 !important;
        font-weight: bold !important;
    }
    hr {
        border-bottom-color: #e0e0e0 !important;
    }
    </style>
""", unsafe_allow_html=True)

fichier_csv = "donnees_suivi.csv"

joueurs = [
    "Abdoul KONE", "Adama BOJANG", "Alexandre OLLIERO", "Amine SALAMA", 
    "Antoine LEAUTEY", "Elie NTAMON", "Ewen JAOUEN", "Hafiz IBRAHIM", 
    "Hiroki SEKINE", "John PATRICK", "Joseph OKUMU", "Keito NAKAMURA", 
    "Martial TIA", "Maxime BUSI", "Mohamed DARAMY", "Mory GBANE", 
    "Nicolas PALLOIS", "Norman BASSETTE", "Patrick GUEU", "Sergio AKIEME", 
    "Soumaila SYLLA", "Teddy TEUMA", "Theo LEONI", "Thiemoko DIARRA", 
    "Yaya FOFANA", "Yohan DEMONCY", "Samuel KOTTO", "Yassine BENHATTAB", 
    "Tidiane DIARRASSOUBA", "Arone GADOU", "Lenny SYLLA"
]

if not os.path.exists(fichier_csv):
    pd.DataFrame(columns=[
        "Date", "Joueur", "Score Sommeil", "Statut Sommeil", 
        "Score Alimentation", "Statut Alimentation"
    ]).to_csv(fichier_csv, index=False)

# Logo centré
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if os.path.exists("logo_sdr.png"):
        st.image("logo_sdr.png", use_container_width=True)
    elif os.path.exists("logo_sdr.jpg"):
        st.image("logo_sdr.jpg", use_container_width=True)

# Titre principal centré
st.markdown("<h1 style='text-align: center;'>Questionnaire Sommeil / Nutrition</h1>", unsafe_allow_html=True)
st.write("")

# Choix de la langue au-dessus
lang = st.selectbox("Langue / Language", ["FR", "EN"])
is_fr = lang == "FR"

st.write("")

# Sélection Joueur et Date
joueur = st.selectbox("Joueur / Player", joueurs)
date_eval = st.date_input(" Date", date.today())
st.divider()

def ask_q(title_fr, title_en, q_fr, q_en, opts_fr, opts_en, key):
    st.markdown(f"<h4 style='color:#d32f2f !important; margin-bottom: 2px;'>{title_fr if is_fr else title_en}</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 16px; margin-bottom: 10px; font-weight: bold; color:#000000 !important;'>{q_fr if is_fr else q_en}</p>", unsafe_allow_html=True)
    ans = st.radio(
        key, 
        [0, 1, 2], 
        format_func=lambda x: opts_fr[x] if is_fr else opts_en[x],
        label_visibility="collapsed", 
        key=key
    )
    st.write("")
    return ans

# SECTION SOMMEIL
st.header("💤 Sommeil / Sleep")
st.markdown("*(Consigne : réponds selon ta moyenne des 7 derniers jours)*" if is_fr else "*(Instruction: answer based on your average over the last 7 days)*")

s1 = ask_q("Durée moyenne", "Average duration", "1. Quelle est ta durée moyenne de sommeil ?", "1. What is your average sleep duration?", ["> 8 h", "6–8 h", "< 6 h"], ["> 8 h", "6–8 h", "< 6 h"], "s1")
s2 = ask_q("Qualité perçue", "Perceived quality", "2. Comment perçois-tu la qualité de ton sommeil ?", "2. How do you perceive your sleep quality?", ["Très bonne", "Moyenne", "Mauvaise"], ["Very good", "Average", "Bad"], "s2")
s3 = ask_q("Endormissement", "Time to fall asleep", "3. Combien de temps mets-tu à t'endormir ?", "3. How long does it take you to fall asleep?", ["< 20 min", "20–40 min", "> 40 min"], ["< 20 min", "20–40 min", "> 40 min"], "s3")
s4 = ask_q("Réveils nocturnes", "Nighttime awakenings", "4. Combien de fois te réveilles-tu par nuit ?", "4. How many nighttime awakenings do you have?", ["0–1", "2–3", "≥ 4"], ["0–1", "2–3", "≥ 4"], "s4")
s5 = ask_q("Fatigue au réveil", "Fatigue upon waking", "5. Quel est ton niveau de fatigue au réveil ?", "5. What is your fatigue level upon waking?", ["Pas fatigué", "Moyen", "Très fatigué"], ["Not tired", "Average", "Very tired"], "s5")

st.divider()

# SECTION ALIMENTATION (Numérotation et libellés corrigés)
st.header("🥗 Alimentation / Nutrition")
st.markdown("*(Consigne : réponds selon ta semaine type d’entraînement)*" if is_fr else "*(Instruction: answer based on your typical training week)*")

a1 = ask_q("Repas structurés / jour", "Structured meals / day", "1. Quel est ton nombre de repas structurés par jour ?", "1. What is your number of structured meals per day?", ["≥ 3", "2", "≤ 1"], ["≥ 3", "2", "≤ 1"], "a1")
a2 = ask_q("Apport glucidique / repas", "Carbohydrate intake / meal", "2. As-tu un apport en glucides à chaque repas ? (Pâtes, riz, pommes de terre, pain...)", "2. Do you have carbohydrate intake at each meal? (Pasta, rice, potatoes, bread...)", ["Oui", "Parfois", "Non"], ["Yes", "Sometimes", "No"], "a2")
a3 = ask_q("Apport protéique / repas", "Protein intake / meal", "3. As-tu un apport protéique à chaque repas ? (Viande, poisson, œufs, lentilles, tofu...)", "3. Do you have protein intake at each meal? (Meat, fish, eggs, lentils, tofu...)", ["Oui", "Parfois", "Non"], ["Yes", "Sometimes", "No"], "a3")
a4 = ask_q("Fruits & légumes / jour", "Fruits & vegetables / day", "4. Combien de portions de fruits & légumes manges-tu par jour ?", "4. How many portions of fruits & vegetables do you eat per day?", ["≥ 5", "3–4", "≤ 2"], ["≥ 5", "3–4", "≤ 2"], "a4")
a5 = ask_q("Hydratation", "Hydration", "5. Ton hydratation est-elle suffisante (urines claires) ?", "5. Is your hydration sufficient (clear urine)?", ["Oui", "Moyen", "Non"], ["Yes", "Average", "No"], "a5")
a6 = ask_q("Alimentation post-entraînement", "Post-training nutrition", "6. Prends-tu une alimentation/collation post-entraînement ?", "6. Do you consume post-training nutrition/snacks?", ["Oui", "Moyen", "Non"], ["Yes", "Average", "No"], "a6")

st.divider()

# Logique de statut adaptée selon le score max
def get_status_sleep(score):
    if score >= 8: return "Bon" if is_fr else "Good"
    if score >= 5: return "Moyen" if is_fr else "Average"
    return "Insuffisant" if is_fr else "Insufficient"

def get_status_nutri(score):
    if score >= 10: return "Bon" if is_fr else "Good" # Seuil relevé car score max est 12
    if score >= 6: return "Moyen" if is_fr else "Average"
    return "Insuffisant" if is_fr else "Insufficient"

# BOUTON SAUVEGARDER
if st.button("Sauvegarder / Save", use_container_width=True):
    score_s = sum([2 - i for i in [s1, s2, s3, s4, s5]])
    score_a = sum([2 - i for i in [a1, a2, a3, a4, a5, a6]])
    
    df = pd.read_csv(fichier_csv)
    df = pd.concat([df, pd.DataFrame([{
        "Date": date_eval, 
        "Joueur": joueur,
        "Score Sommeil": score_s, 
        "Statut Sommeil": get_status_sleep(score_s),
        "Score Alimentation": score_a, 
        "Statut Alimentation": get_status_nutri(score_a)
    }])], ignore_index=True)
    df.to_csv(fichier_csv, index=False)
    st.success("Données sauvegardées ! / Data saved!")

st.write("")

# BOUTON TELECHARGER
if os.path.exists(fichier_csv):
    with open(fichier_csv, "rb") as f:
        st.download_button("Télécharger CSV / Download CSV", f, file_name="export_suivi.csv", use_container_width=True)

# streamlit run Score.py