import streamlit as st
import requests
from PIL import Image
import pandas as pd
import io
import time
from streamlit_drawable_canvas import st_canvas

st.title("Extraction de Tableaux avec Sélection des Zones")

# Téléchargement des images
uploaded_files = st.file_uploader(
    "Choisissez une ou plusieurs images...",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    all_dataframes = []
    selected_zones = []  # Pour stocker les zones sélectionnées pour chaque image

    # Bouton pour valider les zones sélectionnées
    validate_zones = st.button("Valider les zones sélectionnées")

    for i, uploaded_file in enumerate(uploaded_files):
        st.subheader(f"Image {i + 1}")

        # Afficher l'image avec le canvas pour dessiner les zones
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Image {i + 1}", use_column_width=True)

        # Utiliser le canvas pour dessiner des rectangles
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=2,
            stroke_color="orange",
            background_image=image,
            height=image.height,
            width=image.width,
            drawing_mode="rect",
            key=f"canvas_{i}"
        )

        # Stocker les zones dessinées
        if canvas_result.json_data is not None:
            selected_zones.append(canvas_result.json_data["objects"])

    if validate_zones and selected_zones:
        # Barre de progression globale
        global_progress_bar = st.progress(0)
        global_status_text = st.empty()

        for i, uploaded_file in enumerate(uploaded_files):
            # Mettre à jour la barre de progression globale
            global_progress = int(((i + 1) / len(uploaded_files)) * 100)
            global_progress_bar.progress(global_progress)
            global_status_text.text(f"Traitement de l'image {i + 1}/{len(uploaded_files)}...")

            # Charger l'image
            image = Image.open(uploaded_file)

            # Extraire les zones sélectionnées
            zones = selected_zones[i]

            for zone in zones:
                # Coordonnées de la zone sélectionnée
                x1, y1 = zone["left"], zone["top"]
                x2, y2 = x1 + zone["width"], y1 + zone["height"]

                # Rogner l'image selon la zone sélectionnée
                cropped_image = image.crop((x1, y1, x2, y2))

                # Afficher l'image rognée
                st.image(cropped_image, caption=f"Zone sélectionnée {i + 1}", use_column_width=True)

                # Utiliser OCR.Space pour extraire le texte de la zone sélectionnée
                api_url = "https://api.ocr.space/parse/image"
                payload = {
                    'isOverlayRequired': False,
                    'apikey': 'helloworld',  # Clé API gratuite pour les tests
                    'language': 'fra',
                }

                # Convertir l'image rognée en bytes
                img_byte_arr = io.BytesIO()
                cropped_image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                files = {'file': img_byte_arr}
                response = requests.post(api_url, files=files, data=payload)
                result = response.json()

                # Afficher le texte extrait
                text = result.get('ParsedResults', [{}])[0].get('ParsedText', '')
                st.subheader(f"Texte extrait de la zone {i + 1} :")
                st.text(text)

                # Nettoyer et organiser les données
                lines = text.split('\n')
                data = []

                for line in lines:
                    line = line.strip()
                    if line:
                        columns = [col.strip() for col in line.split('  ')]
                        data.append(columns)

                # Créer un DataFrame
                df = pd.DataFrame(data)

                # Afficher le DataFrame
                st.subheader(f"Données structurées de la zone {i + 1} :")
                st.dataframe(df)

                all_dataframes.append(df)

        # Exporter tous les DataFrames en un seul fichier Excel
        st.subheader("Exporter en Excel")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for i, df in enumerate(all_dataframes):
                df.to_excel(writer, sheet_name=f"Zone_{i + 1}", index=False, header=False)

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
