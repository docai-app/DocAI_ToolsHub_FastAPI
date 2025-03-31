from fastapi import APIRouter, HTTPException, UploadFile, File
from services.azure_ocr_service import AzureOCRService
from typing import List
import os
import io
from PIL import Image
from pydantic import BaseModel

router = APIRouter()

# 從環境變數或配置檔案中獲取這些值
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

print(AZURE_KEY, AZURE_ENDPOINT)

ocr_service = AzureOCRService(AZURE_KEY, AZURE_ENDPOINT)

class ImageUrlsRequest(BaseModel):
    image_urls: List[str]

@router.post("/read")
async def read_text(request: ImageUrlsRequest):
    try:
        results = []
        for url in request.image_urls:
            text = await ocr_service.read_text_from_url(url)
            results.append(text)
        
        return {
            "success": True,
            "data": {
                "text": "\n".join(results)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/read/upload")
async def read_text_from_upload(file: UploadFile = File(...)):
    try:
        # 直接傳遞文件對象給服務
        text = await ocr_service.read_text_from_image(file.file)
        
        return {
            "success": True,
            "data": {
                "text": text
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 