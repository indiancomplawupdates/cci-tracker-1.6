from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils.scraper import check_for_updates
from utils.emailer import send_update_email, send_fortune_email
import uvicorn
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

SUBSCRIBERS_FILE = "data/subscribers.json"

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    with open(SUBSCRIBERS_FILE, "r") as f:
        subscribers = json.load(f)
    return templates.TemplateResponse("dashboard.html", {"request": request, "subscribers": subscribers})

@app.post("/add-subscriber")
async def add_subscriber(email: str = Form(...)):
    with open(SUBSCRIBERS_FILE, "r+") as f:
        data = json.load(f)
        if email not in data:
            data.append(email)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    return RedirectResponse("/", status_code=303)

@app.post("/check-updates")
async def manual_check():
    updates = check_for_updates()
    with open(SUBSCRIBERS_FILE, "r") as f:
        subscribers = json.load(f)
    if updates:
        for email in subscribers:
            send_update_email(email, updates)
    else:
        for email in subscribers:
            send_fortune_email(email)
    return RedirectResponse("/", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
