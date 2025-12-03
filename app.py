import streamlit as st
from PIL import Image
import io
from utils.ocr_utils import extract_text_from_zone
from utils.data_utils import clean_and_structure_data
from utils.excel_utils import export_to_excel

def main():
    st.title("Extraction de Tableaux avec Sélection des Zones")

    # Téléchargement des images
    uploaded_files = st.file_uploader(
        "Choisissez une ou plusieurs images...",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files:
        all_dataframes = []
        selected_zones = []

        # Bouton pour valider les zones sélectionnées
        validate_zones = st.button("Valider les zones sélectionnées")

        for i, uploaded_file in enumerate(uploaded_files):
            st.subheader(f"Image {i + 1}")

            # Afficher l'image
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Image {i + 1}", use_column_width=True)

            # Saisie manuelle des coordonnées de la zone
            st.subheader("Sélectionnez les coordonnées de la zone à analyser")
            x1 = st.number_input(f"X1 (coin supérieur gauche) pour l'image {i + 1}", min_value=0, max_value=image.width, value=0, key=f"x1_{i}")
            y1 = st.number_input(f"Y1 (coin supérieur gauche) pour l'image {i + 1}", min_value=0, max_value=image.height, value=0, key=f"y1_{i}")
            x2 = st.number_input(f"X2 (coin inférieur droit) pour l'image {i + 1}", min_value=0, max_value=image.width, value=image.width, key=f"x2_{i}")
            y2 = st.number_input(f"Y2 (coin inférieur droit) pour l'image {i + 1}", min_value=0, max_value=image.height, value=image.height, key=f"y2_{i}")

            selected_zones.append((x1, y1, x2, y2))

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
                x1, y1, x2, y2 = selected_zones[i]

                # Rogner l'image selon la zone sélectionnée
                cropped_image = image.crop((x1, y1, x2, y2))

                # Afficher l'image rognée
                st.image(cropped_image, caption=f"Zone sélectionnée {i + 1}", use_column_width=True)

                # Extraire le texte de la zone sélectionnée
                text = extract_text_from_zone(cropped_image)

                # Afficher le texte extrait
                st.subheader(f"Texte extrait de la zone {i + 1} :")
                st.text(text)

                # Nettoyer et organiser les données
                df = clean_and_structure_data(text)

                # Afficher le DataFrame
                st.subheader(f"Données structurées de la zone {i + 1} :")
                st.dataframe(df)

                all_dataframes.append(df)

            # Exporter tous les DataFrames en un seul fichier Excel
            st.subheader("Exporter en Excel")
            excel_data = export_to_excel(all_dataframes)

            st.download_button(
                label="Télécharger le fichier Excel",
                data=excel_data,
                file_name="tableaux_extraits.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Mettre à jour la barre de progression globale
            global_progress_bar.progress(100)
            global_status_text.text("Tous les fichiers ont été traités !")

if __name__ == "__main__":
    main()
