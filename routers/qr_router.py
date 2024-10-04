from fastapi import APIRouter, HTTPException, UploadFile, File
from services.qr_service import decode_qrcode
from PIL import Image

router = APIRouter()

@router.post("/info")
async def get_qrcode_info(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file)
        qrcodes = decode_qrcode(image)
        return {"success": True, "data": {"qrcodes": qrcodes}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
