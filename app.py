import os
import random
import string
from typing import Optional
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

alphabet = string.digits + string.ascii_lowercase

client = MongoClient("mongodb", 27017)
db = client.filesDB
posts = db.posts

templates=Jinja2Templates(directory='templates')
app = FastAPI()

app.mount("/static", StaticFiles(directory="templates/static"), name="static")

@app.get('/')
async def welcome(request:Request):
    all_posts = posts.find()
    for post in all_posts:
        print(post)
        
    return templates.TemplateResponse(name='index.html',context={'request':request})


@app.post("/sendForm")
async def upload_files(first_name: str = Form(...),last_name: str = Form(...), files: Optional[list[UploadFile]] = File(None)):
    print(f"Имя: {first_name}")
    print(f"Фамлиия: {last_name}")

    if files:
        for file in files:
            await upload_file(file)
    
    return {"first_name": first_name, "last_name": last_name}

async def upload_file(file: UploadFile):
    new_name = "".join([alphabet[random.randint(0, len(alphabet) - 1)] for _ in range(60)])
    extension = f".{file.filename.rsplit('.', 1)[-1]}"
    temp_name = new_name + extension

    file_path = os.path.join("static/files", temp_name)

    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    
    n=posts.count_documents({})
    if( posts.count_documents({}) == n):
        post = {
            "id": n+1,
            "path": temp_name
        }
        posts.insert_one(post).inserted_id

    return temp_name