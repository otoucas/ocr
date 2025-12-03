import streamlit as st
from PIL import Image
import pandas as pd
import io
import easyocr

def extract_text_from_image(image):
    """Extraire le texte d'une image complète avec EasyOCR."""
    reader = easyocr.Reader(['fr'])  # Langue française
    result = reader.readtext(image, detail=0)
    text = '\n'.join(result)
    return text

def clean_and_structure_data(text):
    """Nettoyer et structurer le texte extrait en DataFrame."""
    lines = text.split('\n')
    data = []

    for line in lines:
        line = line.strip()
        if line:
            columns = line.split()
            data.append(columns)

    df = pd.DataFrame(data)
    return df

def main():
    st.title("Extraction de Texte depuis une Image")

    # Téléchargement d'une image
    uploaded_file = st.file_uploader(
        "Choisissez une image...",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        # Afficher l'image
        image = Image.open(uploaded_file)
        st.image(image, caption="Image téléversée", use_column_width=True)

        # Extraire le texte de l'image
        st.write("Extraction du texte en cours...")
        text = extract_text_from_image(image)

        # Afficher le texte extrait
        st.subheader("Texte extrait :")
        st.text(text)

        # Nettoyer et organiser les données
        df = clean_and_structure_data(text)

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

if __name__ == "__main__":
    main()
