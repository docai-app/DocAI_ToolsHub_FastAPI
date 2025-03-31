from fastapi import APIRouter, HTTPException, UploadFile, File
from services.azure_ocr_service import AzureOCRService
from typing import List
import os
import io
from PIL import Image
import mimetypes
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
        print(f"處理上傳文件: {file.filename}, 內容類型: {file.content_type}")
        
        # 讀取文件內容
        contents = await file.read()
        print(f"已讀取文件，大小: {len(contents)} bytes")
        
        # 獲取文件MIME類型（優先使用內容類型，其次使用文件名檢測）
        mime_type = file.content_type
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(file.filename)
            print(f"根據文件名猜測的MIME類型: {mime_type}")
        
        # 調用 OCR 服務處理文件
        # 注意: 我們現在不再區分 PDF 和圖像，使用簡化的處理方法
        print(f"調用 OCR 服務處理文件...")
        text = await ocr_service.read_text_from_image(contents)
        print(f"OCR 處理完成，提取的文本長度: {len(text)}")
        
        return {
            "success": True,
            "data": {
                "text": text
            }
        }
    except Exception as e:
        # 記錄詳細錯誤信息
        error_msg = str(e)
        print(f"OCR 處理錯誤: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg) 