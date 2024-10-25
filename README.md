# FastAPI Project

這是一個使用FastAPI構建的API服務，提供了arXiv論文搜索和QR碼信息提取的功能。

## 目錄結構

```
.
├── app.py
├── routers
│   ├── arxiv_router.py
│   └── qr_router.py
├── services
│   ├── arxiv_service.py
│   └── qr_service.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## 環境設置

### 先決條件

- Python 3.12
- Docker（可選）

### 安裝依賴

使用以下命令安裝所需的Python包：

```bash
pip install -r requirements.txt
```

## 運行服務

### 使用Uvicorn

你可以使用Uvicorn來運行FastAPI應用：

```bash
uvicorn app:app --host 0.0.0.0 --port 8890
```

### 使用Docker

你也可以使用Docker來運行應用：

```bash
docker-compose up --build
```

## API端點

### arXiv API

- **GET /api/v1/arxiv/search**: 搜索arXiv論文。
  - 查詢參數：
    - `query`: 搜索關鍵字。
    - `max_results`: 返回的最大結果數。

### QR Code API

- **POST /api/v1/qrcode/info**: 提取QR碼信息。
  - 請求體：包含一個名為`file`的圖像文件。

- **POST /api/v1/qrcode/info/pyzbar**: 使用pyzbar提取QR碼信息。
  - 請求體：包含一個名為`file`的圖像文件。

## 代碼參考

- `routers/arxiv_router.py`: 定義arXiv API的路由。
- `routers/qr_router.py`: 定義QR Code API的路由。
- `services/arxiv_service.py`: 包含arXiv搜索的業務邏輯。
- `services/qr_service.py`: 包含QR碼處理的業務邏輯。

## 貢獻

歡迎提交問題和請求合併。請確保在提交之前運行所有測試。

## 授權

此項目使用MIT許可證。詳情請參閱LICENSE文件。
