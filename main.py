from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# serve templates from the "templates" directory
templates = Jinja2Templates(directory="templates")

# simple in‑memory view counter
view_count = 0

@app.get("/")
async def index(request: Request):
    global view_count
    view_count += 1
    return templates.TemplateResponse(
        "o.html",
        {
            "request": request,
            "views": view_count
        }
    )
