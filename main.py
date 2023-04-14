from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import os
import json
import shutil
import numpy as np
from urllib.parse import urlparse, urlunparse


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/character-recognition", response_class=HTMLResponse)
async def read_character_recognition(request: Request):
    return templates.TemplateResponse("character_recognition.html", {"request": request})

@app.post("/character-recognition")
async def recognize_image(request: Request, file: UploadFile):
    # TODO check file size and file type
    filename = file.filename
    file_path = os.path.join('./static', filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        img = Image.open(file_path).convert('RGB')
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": "Invalid image format. Only PNG, JPEG, and JPG are supported."}
    ocr = PaddleOCR(use_angle_cls=True, lang='japan')
    img = np.array(img)
    result = ocr.ocr(img, cls=True)
    boxes = [char[0] for line in result for char in line]
    txts = [char[1][0] for line in result for char in line]
    scores = [char[1][1] for line in result for char in line]
    im_show = draw_ocr(img, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    result_path = 'result.jpg'
    im_show.save(os.path.join('./static', result_path))
    data = {"boxes": boxes, "txts": txts, "scores": scores}
    result_json_path = os.path.join('./static', 'result.json')
    with open(result_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    result_image_url = request.url_for('static', path=result_path)
    print(f"result_image_url: {result_image_url}")
    result_json_url = request.url_for('static', path='result.json')
    print(f"result_json_url: {result_json_url}")
    # return_data = {
    #     "result_image_path": result_path,
    #     "result_image_url": result_image_url,
    #     "result_json_path": result_json_path,
    #     "result_json_url": result_json_url,
    # }
    # return JSONResponse(content=return_data)
    return "Done"
    # return {"result_link": "/result.jpg", "result_json": "/result.json"}
  
@app.route("/delete-static")
async def delete_static(request: Request):
    try:
        # remove all files inside the static folder
        for filename in os.listdir("./static"):
            print(f"filename=====================: {filename}")
            file_path = os.path.join("./static", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return RedirectResponse(url="/character_recognition.html")
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": "An error occurred while refreshing the page."}


@app.get("/translate", response_class=HTMLResponse)
async def read_translate(request: Request):
    return templates.TemplateResponse("translate.html", {"request": request})

@app.get("/daily-news", response_class=HTMLResponse)
async def read_daily_news(request: Request):
    return templates.TemplateResponse("daily_news.html", {"request": request})

@app.get("/detection", response_class=HTMLResponse)
async def read_detection(request: Request):
    return templates.TemplateResponse("detection.html", {"request": request})

@app.get("/recommendation", response_class=HTMLResponse)
async def read_recommendation(request: Request):
    return templates.TemplateResponse("recommendation.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def read_contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})
