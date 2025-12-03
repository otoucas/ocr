import streamlit as st
from utils.ocr_utils import extract_text_from_zone
from utils.data_utils import clean_and_structure_data
from utils.excel_utils import export_to_excel
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import os
import tempfile

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

            # Enregistrer temporairement l'image
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                image.save(tmp_file, format="PNG")
                tmp_file_path = tmp_file.name

            # Utiliser le canvas pour dessiner des rectangles
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=2,
                stroke_color="orange",
                background_image=tmp_file_path,  # Utiliser le chemin du fichier temporaire
                height=image.height,
                width=image.width,
                drawing_mode="rect",
                key=f"canvas_{i}"
            )

            # Supprimer le fichier temporaire
            os.unlink(tmp_file_path)

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
