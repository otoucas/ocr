import streamlit as st
import requests
from PIL import Image
import pandas as pd
import io
import time

st.title("Extraction de Tableaux depuis Plusieurs Images")

# Téléchargement des images
uploaded_files = st.file_uploader(
    "Choisissez une ou plusieurs images...",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    # Barre de progression globale
    global_progress_bar = st.progress(0)
    global_status_text = st.empty()

    all_dataframes = []  # Pour stocker les DataFrames de chaque image

    # Traiter chaque image
    for i, uploaded_file in enumerate(uploaded_files):
        # Mettre à jour la barre de progression globale
        global_progress = int(((i + 1) / len(uploaded_files)) * 100)
        global_progress_bar.progress(global_progress)
        global_status_text.text(f"Traitement de l'image {i + 1}/{len(uploaded_files)}...")

        # Afficher l'image
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Image {i + 1}", use_column_width=True)

        # Barre de progression pour l'extraction du texte
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Simuler une progression pour l'extraction
        for progress in range(1, 101, 10):
            status_text.text(f"Extraction du texte en cours... {progress}%")
            progress_bar.progress(progress)
            time.sleep(0.05)  # Simuler un traitement

        # Utiliser OCR.Space pour extraire le texte
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
        st.subheader(f"Texte extrait de l'image {i + 1} :")
        st.text(text)

        # Barre de progression pour la structuration des données
        progress_bar = st.progress(0)
        status_text = st.empty()

        for progress in range(1, 101, 20):
            status_text.text(f"Structuration des données en cours... {progress}%")
            progress_bar.progress(progress)
            time.sleep(0.05)  # Simuler un traitement

        # Nettoyer et organiser les données
        lines = text.split('\n')
        data = []
        for line in lines:
            if line.strip():  # Ignorer les lignes vides
                data.append(line.split())  # Diviser chaque ligne en colonnes

        # Créer un DataFrame
        df = pd.DataFrame(data)
        all_dataframes.append(df)

        # Mettre à jour la barre de progression
        progress_bar.progress(100)
        status_text.text("Structuration terminée !")

        # Afficher le DataFrame
        st.subheader(f"Données structurées de l'image {i + 1} :")
        st.dataframe(df)

    # Exporter tous les DataFrames en un seul fichier Excel
    st.subheader("Exporter en Excel")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for i, df in enumerate(all_dataframes):
            df.to_excel(writer, sheet_name=f"Image_{i + 1}", index=False, header=False)

    excel_data = output.getvalue()

    st.download_button(
        label="Télécharger le fichier Excel",
        data=excel_data,
        file_name="tableaux_extraits.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Mettre à jour la barre de progression globale
    global_progress_bar.progress(100)
    global_status_text.text("Tous les fichiers ont été traités !")
