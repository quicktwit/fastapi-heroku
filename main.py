from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
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
