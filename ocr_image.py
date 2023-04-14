from PIL import Image
from tempfile import NamedTemporaryFile
from paddleocr import PaddleOCR, draw_ocr
import json


def recognize_character(image_bytes):
    # Save the uploaded bytes to a temporary file
    with NamedTemporaryFile(delete=False, suffix=".jpg") as f:
        f.write(image_bytes)
        filename = f.name
    try:
        img = Image.open(filename)
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": "Invalid image format. Only PNG, JPEG, and JPG are supported."}
    ocr = PaddleOCR(use_angle_cls=True, lang='japan')
    result = ocr.ocr(img, cls=True)
    boxes = [line[0] for res in result for line in res]
    txts = [line[1][0] for res in result for line in res for line in res]
    scores = [line[1][1] for res in result for line in res for line in res]
    im_show = draw_ocr(img, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    with NamedTemporaryFile(delete=False, suffix=".jpg") as f:
        im_show.save(f, format='JPEG')
        result_filename = f.name
    data = {"boxes": boxes, "txts": txts, "scores": scores}
    with open('result.json', 'w') as f:
        json.dump(data, f)
    return {"result_link": f"/{result_filename}", "result_json": "/result.json"}
