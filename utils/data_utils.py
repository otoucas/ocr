import pandas as pd

def clean_and_structure_data(text):
    """Nettoyer et structurer le texte extrait en DataFrame."""
    lines = text.split('\n')
    data = []

    for line in lines:
        line = line.strip()
        if line:
            # Remplacer les espaces multiples par un seul espace
            line = ' '.join(line.split())
            # Diviser la ligne en colonnes (par exemple, en utilisant des espaces ou des tabulations)
            columns = line.split()
            data.append(columns)

    # Créer un DataFrame
    df = pd.DataFrame(data)
    return df
