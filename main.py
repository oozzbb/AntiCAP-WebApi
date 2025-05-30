import AntiCAP
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse


description = """
* 通过Http协议 跨语言调用AntiCAP

<img src="https://img.shields.io/badge/GitHub-ffffff"></a> <a href="https://github.com/81NewArk/AntiCAP"> <img src="https://img.shields.io/github/stars/81NewArk/AntiCAP?style=social"> <img src="https://badges.pufler.dev/visits/81NewArk/AntiCAP">

"""



app = FastAPI(title="AntiCAP - WebApi", description=description, version="1.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ModelImageIn(BaseModel):
    img_base64: str


class ModelOrderImageIn(BaseModel):
    order_img_base64: str
    target_img_base64:str



Atc = AntiCAP.AntiCAP(show_ad=False)



@app.get("/",summary="index.html",tags=["主页"])
async def read_root():
    return FileResponse("static/index.html")

@app.post("/ocr",summary="返回字符串",tags=["OCR识别"])
async def ocr(data: ModelImageIn):
    result = Atc.OCR(data.img_base64)
    return {"result": result }

@app.post("/math",summary="返回计算结果",tags=["计算识别"])
async def math(data: ModelImageIn):
    result = Atc.Math(data.img_base64)
    return {"result": result }

@app.post("/detection/icon",summary="检测图标,返回坐标",tags=["目标检测"])
async def detection(data: ModelImageIn):
    result = Atc.Detection_Icon(data.img_base64)
    return {"result": result }

@app.post("/detection/text",summary="按序文字,返回坐标",tags=["目标检测"])
async def detection(data: ModelImageIn):
    result = Atc.Detection_Text(data.img_base64)
    return {"result": result}

@app.post("/detection/icon/order",summary="按序返回图标的坐标",tags=["目标检测"])
async def detection(data: ModelOrderImageIn):
    result = Atc.ClickIcon_Order(order_img_base64=data.order_img_base64,target_img_base64=data.target_img_base64)
    return {"result": result }

@app.post("/detection/text/order",summary="按序返回文字的坐标",tags=["目标检测"])
async def detection(data: ModelOrderImageIn):
    result = Atc.ClickText_Order(order_img_base64=data.order_img_base64,target_img_base64=data.target_img_base64)
    return {"result": result }



if __name__ == '__main__':
    print('''
        -----------------------------------------------------------  
        |      _              _     _    ____      _      ____    |
        |     / \     _ __   | |_  (_)  / ___|    / \    |  _ \   |
        |    / _ \   | '_ \  | __| | | | |       / _ \   | |_) |  |
        |   / ___ \  | | | | | |_  | | | |___   / ___ \  |  __/   |
        |  /_/   \_\ |_| |_|  \__| |_|  \____| /_/   \_\ |_|      |                                                   
        -----------------------------------------------------------                                                       
        |         Github: https://github.com/81NewArk/AntiCAP     |
        |         Author: 81NewArk                                |
        |    Description: 开箱即用 对抗复杂验证码.                    |
        -----------------------------------------------------------                           
       ''')

    uvicorn.run(app, host="0.0.0.0", port=6688, access_log=True)

