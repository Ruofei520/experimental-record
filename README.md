# experimental-record
## 文件说明
```experimental_record_djj.md```记录了djj跑的实验结果

```experimental_record_wmy.md```记录了wmy跑的实验结果

```detect.py``` mmdetection跑测试集，生成可提交的csv文件

```divide_train_val.py``` 划分验证集，训练集与验证集比例8：2

```img_size_info.py``` 统计训练集（测试集）图片尺寸分布，并绘制饼图

```txt2csv.py``` 将YOLOv2使用detect.py跑测试集生成的txt文件转为可提交的csv文件

```xml2json.py``` 将比赛给的XML数据转化为COCO数据的标注格式,给mmdetection使用

```xml2json.py``` 将比赛给的XML数据转化为YOLOv5所需的txt格式
