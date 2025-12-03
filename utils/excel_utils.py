import pandas as pd
import io

def export_to_excel(dataframes):
    """Exporter une liste de DataFrames en un seul fichier Excel."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for i, df in enumerate(dataframes):
            df.to_excel(writer, sheet_name=f"Zone_{i + 1}", index=False, header=False)
    return output.getvalue()
