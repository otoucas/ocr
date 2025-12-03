import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import io

# Configuration de Tesseract (à adapter selon votre installation locale)
# Exemple pour Windows :
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.title("Extraction de Tableaux depuis une Image")

# Téléchargement de l'image
uploaded_file = st.file_uploader("Choisissez une image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Afficher l'image
    image = Image.open(uploaded_file)
    st.image(image, caption="Image téléversée", use_column_width=True)

    # Extraire le texte
    st.write("Extraction du texte en cours...")
    text = pytesseract.image_to_string(image)

    # Afficher le texte extrait
    st.subheader("Texte extrait :")
    st.text(text)

    # Nettoyer et organiser les données (exemple basique)
    lines = text.split('\n')
    data = []
    for line in lines:
        if line.strip():  # Ignorer les lignes vides
            data.append(line.split())  # Diviser chaque ligne en colonnes

    # Créer un DataFrame
    df = pd.DataFrame(data)

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
