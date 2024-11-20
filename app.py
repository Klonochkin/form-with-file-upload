from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates=Jinja2Templates(directory='templates')
app = FastAPI()

app.mount("/static", StaticFiles(directory="templates/static"), name="static")

@app.get('/')
async def welcome(request:Request):
    return templates.TemplateResponse(name='index.html',context={'request':request})
