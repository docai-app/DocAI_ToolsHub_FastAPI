from fastapi import APIRouter, UploadFile, File, HTTPException
from services.pdf_service import convert_pdf_to_images
from PIL import Image
import io
import base64

router = APIRouter()

@router.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    try:
        # Save the uploaded PDF file to a temporary location
        pdf_file_path = f"/tmp/{file.filename}"
        with open(pdf_file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Convert PDF to images
        images = convert_pdf_to_images(pdf_file_path)

        # Convert images to Base64 encoded strings
        image_base64_strings = []
        for image in images:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            image_base64_strings.append(img_base64)

        return {"success": True, "images": image_base64_strings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))