from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio 
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
@app.get("/ping")
async def ping():
    return {"status": "alive"}


@app.on_event("startup")
async def schedule_ping_task():
    async def ping_loop():
        async with httpx.AsyncClient(timeout=5.0) as client:
            while True:
                try:
                    r = await client.get(f"{SERVICE_URL}/ping")
                    if r.status_code != 200:
                        print(f"[Ping] returned {r.status_code}")
                except Exception as e:
                    print(f"[PingError] {e!r}")
                await asyncio.sleep(10)
    asyncio.create_task(ping_loop())
