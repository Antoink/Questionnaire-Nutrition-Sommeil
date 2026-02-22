import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Questionnaire", page_icon="logo_sdr.png", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stRadio > div { flex-direction: column; gap: 12px; align-items: center; justify-content: center; }
    div[data-testid="stRadio"] > div { background-color: #f4f4f4 !important; padding: 15px; border-radius: 12px; border: 2px solid #cccccc !important; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05); width: 100%; max-width: 400px; margin: auto; text-align: center; }
    div[data-testid="stRadio"] label[data-baseweb="radio"] { justify-content: center !important; width: 100%; padding: 8px 0; margin: auto !important; }
    div[data-testid="stRadio"] * { color: #000000 !important; font-size: 16px !important; font-weight: 600; }
    div[data-testid="stFormSubmitButton"] > button { height: 60px; border-radius: 12px; font-size: 20px !important; font-weight: bold; background-color: #d32f2f !important; border: 2px solid #b71c1c !important; box-shadow: 0px 4px 10px rgba(211, 47, 47, 0.3); transition: 0.3s; width: 100%; color: #ffffff !important; }
    div[data-testid="stFormSubmitButton"] > button *, div[data-testid="stFormSubmitButton"] > button p { color: #ffffff !important; }
    div[data-testid="stFormSubmitButton"] > button:hover { background-color: #b71c1c !important; border-color: #9b0000 !important; }
    div[data-testid="stDownloadButton"] > button, div[data-testid="stButton"] > button { height: 60px; border-radius: 12px; font-size: 20px !important; font-weight: bold; background-color: #000000 !important; border: 2px solid #000000 !important; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3); transition: 0.3s; width: 100%; color: #ffffff !important; }
    div[data-testid="stDownloadButton"] > button *, div[data-testid="stDownloadButton"] > button p, div[data-testid="stButton"] > button *, div[data-testid="stButton"] > button p { color: #ffffff !important; }
    h1, h2, h3, h4 { color: #d32f2f !important; font-weight: 800 !important; text-align: center; }
    p, label, .stSelectbox label { color: #000000 !important; font-weight: bold !important; text-align: center; }
    hr { border-bottom-color: #e0e0e0 !important; }
    </style>
""", unsafe_allow_html=True)

fichier_csv = "donnees_suivi.csv"

colonnes_csv = [
    "Date", "Joueur", 
    "S1_Duree", "S2_Qualite", "S3_Endormissement", "S4_Reveils", "S5_Fatigue", 
    "Score Sommeil", "Statut Sommeil", 
    "A1_Repas", "A2_Glucides", "A3_Proteines", "A4_FruitsLegumes", "A5_Hydratation", "A6_PostEntrainement", 
    "Score Alimentation", "Statut Alimentation"
]

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
    pd.DataFrame(columns=colonnes_csv).to_csv(fichier_csv, index=False)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if os.path.exists("logo_sdr.png"):
        st.image("logo_sdr.png", use_container_width=True)
    elif os.path.exists("logo_sdr.jpg"):
        st.image("logo_sdr.jpg", use_container_width=True)

st.markdown("<h1 style='text-align: center;'>Questionnaire Sommeil / Nutrition</h1>", unsafe_allow_html=True)
st.write("")

lang = st.selectbox("Langue / Language", ["FR", "EN"])
is_fr = lang == "FR"

st.write("")

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

def get_status_sleep(score):
    if score >= 8: return "Bon" if is_fr else "Good"
    if score >= 5: return "Moyen" if is_fr else "Average"
    return "Insuffisant" if is_fr else "Insufficient"

def get_status_nutri(score):
    if score >= 10: return "Bon" if is_fr else "Good"
    if score >= 6: return "Moyen" if is_fr else "Average"
    return "Insuffisant" if is_fr else "Insufficient"

with st.form("questionnaire_form"):
    joueur = st.selectbox("Joueur / Player", joueurs)
    date_eval = st.date_input("Date", date.today())
    st.divider()

    st.header("💤 Sommeil / Sleep")
    st.markdown("<p style='text-align: center; font-style: italic;'>Consigne : réponds selon ta moyenne des 7 derniers jours</p>" if is_fr else "<p style='text-align: center; font-style: italic;'>Instruction: answer based on your average over the last 7 days</p>", unsafe_allow_html=True)

    s1 = ask_q("Durée moyenne", "Sleep duration", "1. Quelle est ta durée moyenne de sommeil ?", "1. How many hours do you sleep on average?", ["≥ 8 h", "7–7h59", "< 7 h"], ["≥ 8 h", "7–7h59", "< 7 h"], "s1")
    s2 = ask_q("Qualité perçue", "Sleep quality", "2. Comment perçois-tu la qualité de ton sommeil ?", "2. How do you feel about your sleep quality?", ["Très bonne", "Moyenne", "Mauvaise"], ["Very good", "Average", "Bad"], "s2")
    s3 = ask_q("Endormissement", "Falling asleep", "3. Combien de temps mets-tu à t'endormir ?", "3. How long does it take you to fall asleep?", ["< 20 min", "20–40 min", "> 40 min"], ["< 20 min", "20–40 min", "> 40 min"], "s3")
    s4 = ask_q("Réveils nocturnes", "Waking up at night", "4. Combien de fois te réveilles-tu par nuit ?", "4. How many times do you wake up during the night?", ["0–1", "2–3", "≥ 4"], ["0–1", "2–3", "≥ 4"], "s4")
    s5 = ask_q("Fatigue au réveil", "Morning fatigue", "5. Quel est ton niveau de fatigue au réveil ?", "5. How tired are you when you wake up in the morning?", ["Pas fatigué", "Moyen", "Très fatigué"], ["Not tired", "Average", "Very tired"], "s5")

    st.divider()

    st.header("🥗 Alimentation / Nutrition")
    st.markdown("<p style='text-align: center; font-style: italic;'>Consigne : réponds selon ta semaine type d’entraînement</p>" if is_fr else "<p style='text-align: center; font-style: italic;'>Instruction: answer based on your typical training week</p>", unsafe_allow_html=True)

    a1 = ask_q("Repas structurés / jour", "Meals per day", "1. Quel est ton nombre de repas structurés par jour ?", "1. How many full meals do you eat every day?", ["≥ 3", "2", "≤ 1"], ["≥ 3", "2", "≤ 1"], "a1")
    a2 = ask_q("Apport glucidique / repas", "Carbs intake", "2. As-tu un apport en glucides à chaque repas ? (Pâtes, riz, pommes de terre, pain...)", "2. Do you eat carbs at every meal? (Pasta, rice, potatoes, bread...)", ["Oui", "Parfois", "Non"], ["Yes", "Sometimes", "No"], "a2")
    a3 = ask_q("Apport protéique / repas", "Protein intake", "3. As-tu un apport protéique à chaque repas ? (Viande, poisson, œufs, lentilles, tofu...)", "3. Do you eat protein at every meal? (Meat, fish, eggs...)", ["Oui", "Parfois", "Non"], ["Yes", "Sometimes", "No"], "a3")
    a4 = ask_q("Fruits & légumes / jour", "Fruits and vegetables", "4. Combien de portions de fruits & légumes manges-tu par jour ?", "4. How many portions of fruits and vegetables do you eat per day?", ["≥ 5", "3–4", "≤ 2"], ["≥ 5", "3–4", "≤ 2"], "a4")
    a5 = ask_q("Hydratation", "Hydration", "5. Ton hydratation est-elle suffisante (urines claires) ?", "5. Do you drink enough water every day? (Clear urine)", ["Oui", "Moyen", "Non"], ["Yes", "Average", "No"], "a5")
    a6 = ask_q("Alimentation post-entraînement", "Recovery food", "6. Prends-tu une alimentation/collation post-entraînement ?", "6. Do you eat food or a snack after training?", ["Oui", "Moyen", "Non"], ["Yes", "Average", "No"], "a6")

    st.divider()

    submitted = st.form_submit_button("Sauvegarder / Save", use_container_width=True)

    if submitted:
        score_s = sum([2 - i for i in [s1, s2, s3, s4, s5]])
        score_a = sum([2 - i for i in [a1, a2, a3, a4, a5, a6]])
        
        df = pd.read_csv(fichier_csv)
        new_data = pd.DataFrame([{
            "Date": date_eval, 
            "Joueur": joueur,
            "S1_Duree": ["≥ 8 h", "7–7h59", "< 7 h"][s1],
            "S2_Qualite": ["Très bonne", "Moyenne", "Mauvaise"][s2],
            "S3_Endormissement": ["< 20 min", "20–40 min", "> 40 min"][s3],
            "S4_Reveils": ["0–1", "2–3", "≥ 4"][s4],
            "S5_Fatigue": ["Pas fatigué", "Moyen", "Très fatigué"][s5],
            "Score Sommeil": score_s, 
            "Statut Sommeil": get_status_sleep(score_s),
            "A1_Repas": ["≥ 3", "2", "≤ 1"][a1],
            "A2_Glucides": ["Oui", "Parfois", "Non"][a2],
            "A3_Proteines": ["Oui", "Parfois", "Non"][a3],
            "A4_FruitsLegumes": ["≥ 5", "3–4", "≤ 2"][a4],
            "A5_Hydratation": ["Oui", "Moyen", "Non"][a5],
            "A6_PostEntrainement": ["Oui", "Moyen", "Non"][a6],
            "Score Alimentation": score_a, 
            "Statut Alimentation": get_status_nutri(score_a)
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(fichier_csv, index=False)
        st.success("Données sauvegardées en détail ! / Detailed data saved!")

with st.expander("Voir les données enregistrées (Aperçu) / View saved data"):
    if os.path.exists(fichier_csv):
        df_preview = pd.read_csv(fichier_csv)
        if not df_preview.empty:
            df_preview = df_preview.sort_index(ascending=False)
        st.dataframe(df_preview, use_container_width=True)
    else:
        st.info("Aucune donnée pour le moment.")

    st.write("")
    if st.button(" Vider les données / Clear Data", use_container_width=True, key="clear_btn"):
        pd.DataFrame(columns=colonnes_csv).to_csv(fichier_csv, index=False)
        st.rerun()

if os.path.exists(fichier_csv):
    with open(fichier_csv, "rb") as f:
        st.download_button("Télécharger CSV / Download CSV", f, file_name="export_suivi.csv", use_container_width=True)

st.markdown("""
    <br><br>
    <div style='text-align: center; color: #888888; font-size: 12px;'>
        <em>Développé par Antoine Kaczmarek - DÉPARTEMENT PERFORMANCE - Stade de Reims</em>
    </div>
""", unsafe_allow_html=True)
# streamlit run Score.py