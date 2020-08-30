# experimental-record
## 文件说明
```experimental_record_djj.md```记录了djj跑的实验结果

```experimental_record_wmy.md```记录了wmy跑的实验结果

```detect.py``` mmdetection跑测试集，生成可提交的csv文件

```divide_train_val.py``` 划分验证集，训练集与验证集比例8：2

```img_size_info.py``` 统计训练集（测试集）图片尺寸分布，并绘制饼图

```txt2csv.py``` 将YOLOv2使用detect.py跑测试集生成的txt文件转为可提交的csv文件

```xml2json.py``` 将比赛给的XML数据转化为COCO数据的标注格式,给mmdetection使用

```xml2txt.py``` 将比赛给的XML数据转化为YOLOv5所需的txt格式

```generate_dataset.py``` 生成与测试集分布相同的验证集，生成伪标签数据

## 待尝试策略：
- [x] train_A:使用官方给的所有训练数据做训练，精度最高的，用的都是train_A。
- [x] 水草：在yolo上尝试有提升，涨0.11个点左右，还未在cascade上测试。
- [ ] 2k图和非2k图训练两个模型的专家系统，要调整下学习率，参考cascade。
- [ ] A榜test集伪标签：
- [ ] A榜test集伪标签+B榜test集伪标签
- [x] 用YOLOv5聚类分析得anchor来处理cascade:已实现，效果有提升，但精度和cascade相比还是要差一点。
