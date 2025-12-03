import streamlit as st
import requests
from PIL import Image
import pandas as pd
import io
import time

st.title("Extraction de Tableaux depuis une Image")

# Téléchargement de l'image
uploaded_file = st.file_uploader("Choisissez une image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Afficher l'image
    image = Image.open(uploaded_file)
    st.image(image, caption="Image téléversée", use_column_width=True)

    # Barre de progression pour l'extraction du texte
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Simuler une progression (OCR.Space est généralement rapide, mais on ajoute une barre pour le confort utilisateur)
    for i in range(1, 101, 10):
        status_text.text(f"Extraction du texte en cours... {i}%")
        progress_bar.progress(i)
        time.sleep(0.1)  # Simuler un traitement

    # Utiliser OCR.Space pour extraire le texte
    status_text.text("Extraction du texte en cours...")
    api_url = "https://api.ocr.space/parse/image"
    payload = {
        'isOverlayRequired': False,
        'apikey': 'helloworld',  # Clé API gratuite pour les tests
        'language': 'fra',
    }
    files = {'file': uploaded_file.read()}
    response = requests.post(api_url, files=files, data=payload)
    result = response.json()

    # Mettre à jour la barre de progression
    progress_bar.progress(100)
    status_text.text("Extraction terminée !")

    # Afficher le texte extrait
    text = result.get('ParsedResults', [{}])[0].get('ParsedText', '')
    st.subheader("Texte extrait :")
    st.text(text)

    # Barre de progression pour la structuration des données
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(1, 101, 20):
        status_text.text(f"Structuration des données en cours... {i}%")
        progress_bar.progress(i)
        time.sleep(0.1)  # Simuler un traitement

    # Nettoyer et organiser les données
    lines = text.split('\n')
    data = []
    for line in lines:
        if line.strip():  # Ignorer les lignes vides
            data.append(line.split())  # Diviser chaque ligne en colonnes

    # Créer un DataFrame
    df = pd.DataFrame(data)

    # Mettre à jour la barre de progression
    progress_bar.progress(100)
    status_text.text("Structuration terminée !")

    # Afficher le DataFrame
    st.subheader("Données structurées :")
    st.dataframe(df)

    # Exporter en Excel
    st.subheader("Exporter en Excel")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, header=False)
    excel_data = output.getvalue()

    st.download_button(
        label="Télécharger le fichier Excel",
        data=excel_data,
        file_name="tableau_extrait.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
