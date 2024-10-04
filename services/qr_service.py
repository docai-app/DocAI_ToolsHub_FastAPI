from PIL import Image, ImageEnhance, ImageOps
import cv2
import numpy as np

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
