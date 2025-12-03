import requests
import io

def extract_text_from_image(image):
    """Extraire le texte d'une image complète."""
    api_url = "https://api.ocr.space/parse/image"
    payload = {
        'isOverlayRequired': False,
        'apikey': 'helloworld',  # Clé API gratuite pour les tests
        'language': 'fra',
    }

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    files = {'file': img_byte_arr}
    response = requests.post(api_url, files=files, data=payload)
    result = response.json()

    return result.get('ParsedResults', [{}])[0].get('ParsedText', '')

def extract_text_from_zone(cropped_image):
    """Extraire le texte d'une zone spécifique d'une image."""
    return extract_text_from_image(cropped_image)
