import os
import jwt
import AntiCAP
import uvicorn

from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


SECRET_KEY = None
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1*60*24*60  # 60天
VALID_USERNAME = None
VALID_PASSWORD = None



description = """
* 通过Http协议 跨语言调用AntiCAP

<img src="https://img.shields.io/badge/GitHub-ffffff"></a> <a href="https://github.com/81NewArk/AntiCAP-WebApi"> <img src="https://img.shields.io/github/stars/81NewArk/AntiCAP-WebApi?style=social"> 

"""


app = FastAPI(title="AntiCAP - WebApi", description=description, version="1.0.3")


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


class SliderImageIn(BaseModel):
    target_base64: str
    background_base64:str



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
Atc = AntiCAP.AntiCAP(show_ad=False)



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)




@app.post("/api/login", summary="登录获取JWT", tags=["公共"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != VALID_USERNAME or form_data.password != VALID_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/ocr",summary="返回字符串",tags=["OCR识别"])
async def ocr(data: ModelImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.OCR(data.img_base64)
    return {"result": result }

@app.post("/math",summary="返回计算结果",tags=["计算识别"])
async def math(data: ModelImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.Math(data.img_base64)
    return {"result": result }

@app.post("/detection/icon",summary="检测图标,返回坐标",tags=["目标检测"])
async def detection_icon(data: ModelImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.Detection_Icon(data.img_base64)
    return {"result": result }

@app.post("/detection/text",summary="侦测文字,返回坐标",tags=["目标检测"])
async def detection_text(data: ModelImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.Detection_Text(data.img_base64)
    return {"result": result}

@app.post("/detection/icon/order",summary="按序返回图标的坐标",tags=["目标检测"])
async def detection_icon_order(data: ModelOrderImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.ClickIcon_Order(order_img_base64=data.order_img_base64,target_img_base64=data.target_img_base64)
    return {"result": result }

@app.post("/detection/text/order",summary="按序返回文字的坐标",tags=["目标检测"])
async def detection_text_order(data: ModelOrderImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.ClickText_Order(order_img_base64=data.order_img_base64,target_img_base64=data.target_img_base64)
    return {"result": result }

@app.post("/slider/match",summary="缺口滑块,返回坐标",tags=["滑块验证码"])
async def slider_match(data: SliderImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.Slider_Match(target_base64=data.target_base64,background_base64=data.background_base64)
    return {"result": result }

@app.post("/slider/comparison",summary="阴影滑块,返回坐标",tags=["滑块验证码"])
async def slider_comparison(data: SliderImageIn, current_user: str = Depends(get_current_user)):
    result = Atc.Slider_Comparison(target_base64=data.target_base64,background_base64=data.background_base64)
    return {"result": result }



app.mount("/", StaticFiles(directory="static", html=True), name="static")



if __name__ == '__main__':
    print('''
-----------------------------------------------------------
|      _              _     _    ____      _      ____    |
|     / \     _ __   | |_  (_)  / ___|    / \    |  _ \   |
|    / _ \   | '_ \  | __| | | | |       / _ \   | |_) |  |
|   / ___ \  | | | | | |_  | | | |___   / ___ \   |  __/  |
|  /_/   \_\ |_| |_|  \__| |_|  \____| /_/   \_\ |_|      |
-----------------------------------------------------------
|         Github: https://github.com/81NewArk/AntiCAP     |
|         Author: 81NewArk                                |
-----------------------------------------------------------''')

    VALID_USERNAME = input("Please enter username: ")

    VALID_PASSWORD = input("Please enter password: ")

    SECRET_KEY = os.urandom(32).hex()

    uvicorn.run(app, host="0.0.0.0", port=6688, access_log=True)