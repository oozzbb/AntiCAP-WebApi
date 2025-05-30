# AntiCAP WebApi

## 🌍环境说明
```
python 3.8 +
```

## 📁 安装
```

# git克隆仓库或手动下载
git clone https://github.com/81NewArk/AntiCAP-WebApi


# 进入项目目录
cd AntiCAP-WebApi


# 使用清华源下载项目所需依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# 运行main.py
python main.py


# 开发者文档 
http://127.0.0.1:6688/docs
http://localhost:6688/docs
# 服务器部署需要打开6688端口

```


## 📄 调用说明

### 1. 接口" /ocr " 通用识别

示例图片:

![](https://github.com/81NewArk/AntiCAP-WebApi/blob/main/Doc/DetText.jpg)


请求:
```
{
  "img_base64": "图片的Base64编码"
}
```

响应:
```
{
  "result": "jepv"
}
```



### 2. 接口" /math " 计算识别

示例图片:

![](https://github.com/81NewArk/AntiCAP-WebApi/blob/main/Doc/math.png)

请求:
```
{
  "img_base64": "图片的Base64编码"
}
```
响应:
```
{
  "result": "15"
}
```

### 3. 接口" /detection/text " 文字侦测

示例图片:

![](https://github.com/81NewArk/AntiCAP-WebApi/blob/main/Doc/DetText.jpg)

请求:
```
{
  "img_base64": "图片的Base64编码"
}
```
响应:
```
{
  "result": [
    {
      "text": "勘",
      "box": [
        5.96,
        30.02,
        44.06,
        65.98
      ]
    }......
}
```

### 4. 接口" /detection/text/order " 文字按序侦测

原图:

![](https://github.com/81NewArk/AntiCAP-WebApi/blob/main/Doc/DetText_Order_Raw.jpg)


需要自行裁剪

提示图：

![](https://github.com/81NewArk/AntiCAP-WebApi/blob/main/Doc/DetText_Order.jpg)


目标图：

![](https://github.com/81NewArk/AntiCAP-WebApi/blob/main/Doc/DetText_Order_Target.jpg)


请求:
```
{
  "order_img_base64": "提示图base64",
  "target_img_base64": "目标图base64"
}
```

响应:
```
{
  "result": [
    [
      148,
      71,
      212,
      131
    ]......
}
```


### 5.图标侦测和图标按序侦测同理 