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
    all_dataframes = []

    for i, uploaded_file in enumerate(uploaded_files):
        st.subheader(f"Traitement de l'image {i + 1}")

        # Afficher l'image
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Image {i + 1}", use_column_width=True)

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

        # Afficher le texte brut extrait
        text = result.get('ParsedResults', [{}])[0].get('ParsedText', '')
        st.subheader(f"Texte brut extrait de l'image {i + 1} :")
        st.text(text)

        # Nettoyer et organiser les données
        lines = text.split('\n')
        data = []

        for line in lines:
            line = line.strip()
            if line:
                columns = [col.strip() for col in line.split('  ')]  # Utilisez un séparateur approprié
                data.append(columns)

        # Créer un DataFrame
        df = pd.DataFrame(data)

        # Afficher le DataFrame
        st.subheader(f"Données structurées de l'image {i + 1} :")
        st.dataframe(df)

        all_dataframes.append(df)

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
