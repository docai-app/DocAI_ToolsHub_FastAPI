from pdf2image import convert_from_path
from fastapi import HTTPException

def convert_pdf_to_images(pdf_file_path: str):
    try:
        images = convert_from_path(pdf_file_path)
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting PDF to images: {str(e)}")