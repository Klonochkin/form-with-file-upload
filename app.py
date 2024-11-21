import os
import random
import string
from typing import Optional
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

alphabet = string.digits + string.ascii_lowercase

client = MongoClient("mongodb", 27017)
db = client.filesDB
# client.drop_database('filesDB')
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

@app.get("/data")
async def read_data(request: Request):
    all_posts = posts.find()
    posts_list = list(all_posts)

    for post in posts_list:
        post["_id"] = str(post["_id"]) 

    return JSONResponse(content=posts_list)
    


@app.post("/sendForm")
async def upload_files(request: Request):
    form_data = await request.form()
    all_keys = list(form_data.keys())
    n=posts.count_documents({})
    post = {
            "id": n+1,
        }
    print(type(post))
    fieldName = []
    for i in range(all_keys.__len__()):
        if not isinstance(form_data.get(all_keys[i]), str):
            fieldName.append(all_keys[i])
        else:
            post.update({all_keys[i]: form_data.get(all_keys[i])})


    

    if fieldName.__len__() > 0:
        print(fieldName)
        print(fieldName.__len__())
        for i in range(fieldName.__len__()):
            files = form_data.getlist(fieldName[i]) 
            file_name = []

            if files:
                for file in files:
                    res = await upload_file(file)
                    file_name.append({'filename': res['hash_name'], 'hash_name': res['file_name']})

            post.update({fieldName[i]: file_name})

    if( posts.count_documents({}) == n):
        posts.insert_one(post).inserted_id

    return {"message": "Запись успешно добавлена"} 

async def upload_file(file: UploadFile):
    new_name = "".join([alphabet[random.randint(0, len(alphabet) - 1)] for _ in range(60)])
    extension = f".{file.filename.rsplit('.', 1)[-1]}"
    hash_name = new_name + extension

    file_path = os.path.join("templates/static/files", hash_name)

    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    return {"hash_name": hash_name, "file_name": file.filename}