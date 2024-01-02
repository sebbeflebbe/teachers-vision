import os
import base64
from pdf2image import convert_from_path
import requests
import openai

# Function to convert PDF to high-resolution images
def convert_pdf_to_images(pdf_path, dpi=300):
    return convert_from_path(pdf_path, dpi=dpi)

# Function to encode image to base64
def encode_image_to_base64(image):
    from io import BytesIO
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to analyze image with OpenAI
def analyze_image(base64_image, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Du är en AI assistent i bygglovsprocessen vars uppgift är att stötta handläggarnas utvärdering av bygghandlingar. Identifiera och beräkna det sammanlagda antalet fönster."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "max_tokens": 1000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

# Function to process all PDFs in a folder
def process_folder(folder_path, api_key):
    summaries = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.Pdf'):
            pdf_path = os.path.join(folder_path, filename)
            images = convert_pdf_to_images(pdf_path)
            for image in images:
                base64_image = encode_image_to_base64(image)
                result = analyze_image(base64_image, api_key)
                summaries.append(result)
    return summaries

# Main Execution
folder_path = './testfolder'  # Replace with the path to your folder containing PDFs
openai.api_key = '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'  # Replace with your API key
all_summaries = process_folder(folder_path, openai.api_key)

# Print or process the summaries as needed
for summary in all_summaries:
    print(summary)