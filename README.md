# 增值税发票识别 
  识别type：增值税电子普通发票，增值税普通发票，增值税专用发票；识别字段为：发票代码、发票号码、开票日期、校验码、税后金额等
## 环境
   1. python3.5/3.6
   2. 依赖项安装：pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 
   3. 有GPU环境的可修改安装requirements.txt对应版本的tensorflow-gpu，config.py文件中控制GPU的开关
## 模型架构
    YOLOv3 + CRNN + CTC
   
## 模型
   1. 模型下载地址：链接：https://pan.baidu.com/s/1bjtd3ueiUj3rt16p2_YQ2w
   2. 将下载完毕的模型文件夹models放置于项目根目录下
## 服务启动
   1. python3 app.py
   2. 端口可自行修改
## 测试demo
   1. 测试工具：postman，可自行下载安装
   2. 增值税电子普票测试结果
   
![Image text](https://github.com/guanshuicheng/invoice/blob/master/test-invoice/%E7%94%B5%E5%AD%90%E5%8F%91%E7%A5%A8-test.png)
   
   3. 增值税专用普票测试结果
   
![Image text](https://github.com/guanshuicheng/invoice/blob/master/test-invoice/%E5%A2%9E%E5%80%BC%E7%A8%8E%E4%B8%93%E7%94%A8%E5%8F%91%E7%A5%A8-test.png)

   4. 增值税普通普票测试结果

![Image text](https://github.com/guanshuicheng/invoice/blob/master/test-invoice/%E5%A2%9E%E5%80%BC%E7%A8%8E%E6%99%AE%E9%80%9A%E5%8F%91%E7%A5%A8-test.jpg)
   

## 参考
chineseocr https://github.com/chineseocr/chineseocr
