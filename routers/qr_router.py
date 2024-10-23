from fastapi import APIRouter, HTTPException, UploadFile, File
from services.qr_service import decode_qrcode, decode_qrcode_with_pyzbar
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

@router.post("/info/pyzbar")
async def get_qrcode_info_pyzbar(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file)
        qrcodes = decode_qrcode_with_pyzbar(image)
        return {"success": True, "data": {"qrcodes": qrcodes}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
