from PIL import Image, ImageEnhance, ImageOps
import cv2
import numpy as np
from pyzbar.pyzbar import decode

def preprocess_image(image):
    gray_image = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2.0)
    image_array = np.array(enhanced_image)
    return image_array

def decode_qrcode(image):
    processed_image = preprocess_image(image)
    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(processed_image)

    qrcodes = []
    for i, data in enumerate(decoded_info):
        if data:
            qrcodes.append(
                {
                    "type": "QRCODE",
                    "data": data,
                    "position": {
                        "points": points[i].tolist() if points is not None else []
                    },
                }
            )
    return qrcodes

def decode_qrcode_with_pyzbar(image):
    decoded_objects = decode(image)
    qrcodes = []
    for obj in decoded_objects:
        qrcodes.append({
            "type": obj.type,
            "data": obj.data.decode('utf-8'),
            "position": {
                "points": [point for point in obj.polygon]  # 使用 points 而不是 rect
            }
        })
    return qrcodes
