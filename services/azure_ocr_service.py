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

    async def read_text_from_image(self, image_file, is_pdf=False) -> str:
        try:
            # 檢查是否已經是 bytes 對象
            if isinstance(image_file, bytes):
                # 將 bytes 轉換為 BytesIO 對象 (類文件對象)
                content = io.BytesIO(image_file)
            else:
                try:
                    # 嘗試讀取文件內容
                    file_bytes = image_file.read()
                    # 將讀取的內容轉換為 BytesIO 對象
                    content = io.BytesIO(file_bytes)
                except Exception as read_error:
                    print(f"讀取文件錯誤: {str(read_error)}")
                    # 如果不能讀取，假設已經是內容
                    if isinstance(image_file, bytes):
                        content = io.BytesIO(image_file)
                    else:
                        content = image_file
            
            # 確保內容是一個類文件對象
            print(f"內容類型: {type(content)}")
            
            try:
                # 呼叫 Azure OCR API 處理類文件對象
                read_response = self.client.read_in_stream(content, raw=True)
                
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
                
            except Exception as api_error:
                print(f"API 呼叫錯誤: {str(api_error)}")
                raise Exception(f"Azure OCR API 處理失敗: {str(api_error)}")

        except Exception as e:
            # 記錄詳細錯誤
            print(f"整體處理錯誤: {str(e)}")
            raise Exception(f"Azure OCR 處理失敗: {str(e)}") 