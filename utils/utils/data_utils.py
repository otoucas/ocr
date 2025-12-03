import pandas as pd

def clean_and_structure_data(text):
    """Nettoyer et structurer le texte extrait en DataFrame."""
    lines = text.split('\n')
    data = []

    for line in lines:
        line = line.strip()
        if line:
            columns = [col.strip() for col in line.split('  ')]
            data.append(columns)

    return pd.DataFrame(data)
