from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
import io
from PIL import Image

class AzureOCRService:
    def __init__(self, subscription_key: str, endpoint: str):
        self.client = ComputerVisionClient(
            endpoint=endpoint,
            credentials=CognitiveServicesCredentials(subscription_key)
        )

    async def read_text_from_url(self, image_url: str) -> str:
        try:
            # 呼叫 Azure OCR API
            read_response = self.client.read(image_url, raw=True)
            
            # 獲取操作位置
            operation_location = read_response.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]

            # 等待處理完成
            while True:
                read_result = self.client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)

            # 提取文字
            text_results = []
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        text_results.append(line.text)
            
            return "\n".join(text_results)

        except Exception as e:
            raise Exception(f"Azure OCR 處理失敗: {str(e)}") 

    async def read_text_from_image(self, image_file) -> str:
        try:
            # 先讀取文件內容
            content = image_file.read()
            
            # 使用 BytesIO 創建一個類文件對象
            image_bytes = io.BytesIO(content)
            
            # 使用 PIL 打開圖片
            image = Image.open(image_bytes)
            
            # 轉換為字節流
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format or 'PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # 呼叫 Azure OCR API
            read_response = self.client.read_in_stream(img_byte_arr, raw=True)
            
            # 獲取操作位置
            operation_location = read_response.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]

            # 等待處理完成
            while True:
                read_result = self.client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)

            # 提取文字
            text_results = []
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        text_results.append(line.text)
            
            return "\n".join(text_results)

        except Exception as e:
            raise Exception(f"Azure OCR 處理失敗: {str(e)}") 