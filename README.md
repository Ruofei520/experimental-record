# experimental-record
## 比赛信息：
参赛人员：杜建军、吴明言、吴卓。

队名：**CARC多媒体组**

比赛结束时间：9月11号

## 最终排名：
复现精度排名：第3

复现速度排名：第12

初赛排名：第8

## 消融实验：
|基础模型|DCN|Remote|
|----|
cascade rcnn+ResNext101+FPN+ROI Align(baseline)
## 

## B榜提交结果(只有两次提交机会)：
A榜排名第8

B榜排名第4

|模型|训练策略|评测结果|数据集使用|说明|
|----|-------|-------|----|-----|
|cascade|train_A_DCN_ep11+(在train_A_ep12的基础上)train_all_ep2|0.51654473|train_A_git_ep11_train_A_ep12_train_all_ep2|
|cascade|train_A_DCN_ep12+(在train_A_ep12的基础上)train_all_ep2|**0.51674725**|train_A_git_ep11_train_A_ep12_train_all_ep2|


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
- [x] 2k图和非2k图训练两个模型的专家系统，要调整下学习率，参考cascade。:在yolo上以尝试，但精度突破不了0.50，所以还是继续回头调cscade。
- [x] A榜test集伪标签：掉点
- [ ] A榜test集伪标签+B榜test集伪标签:未尝试，因为掉点
- [x] 用YOLOv5聚类分析得anchor来处理cascade:已实现，效果有提升，但精度和cascade相比还是要差一点。
- [x] DCN（可形变卷积）+ 随机90°旋转，效果不错，可以增强模型的泛化能力。
## 实验记录：
**实验主要由杜建军、吴明言完成并记录，吴卓师兄提供一些tricks和方法上的指导。**

train_A:官方给的所有训练数据，共6575张。图片尺寸：

{'2160\*3840': 2744, '405\*720': 3153, '1080\*1920': 596, '576\*704': 38, '480\*586': 44}

test-A（这次比赛的test-A的图片尺寸）:

{'2160\*3840': 1053, '405\*720': 52, '1080\*1920': 42 **'1440\*2560': 32, '1536\*2048': 21, 共53张2k图** }

test-B（这次比赛的test-B的图片尺寸）:

{'2160\*3840': 734, '405\*720': 100, '1080\*1920': 323, '1440\*2560': 25, '1536\*2048': 13, '480\*586': 2, '576\*704': 3,**共38张2k图**}

test-B-v1(上次比赛的test-B的图片尺寸,可以考虑用这个做伪标签):

{'2160\*3840': 934,  '405\*720': 119,  '1080\*1920': 72,  '576\*704': 3,  '480*586': 2 **'1440\*2560': 42,**  **'1536\*2048': 28,共72张2k图** }

train,val：官方给的训练数据集按照8:2划分的。

train_wmy和val_test2k_1200是wmy划分的数据集，val_test2k_1200加入了53张2k图，和测试集同分布，且与训练集没有交集

train_wmy:5428张，val_test2k_1200:1200。在wmy的容器中，是train、val



|模型|epoch |验证结果|A榜评测结果|训练集|验证集|备注|
|----|-----|---------|-----------------|------|----|---|
|cascade|train_epoch11|0.507|0.49029607|train_wmy|val_test2k_1200|epoch 11,训练集和验证集不相交，验证集是wmy按照A榜测试集的分布划分出来的|
|cascade|trian_epoch10|0.532|0.49245347|train|val|使用的是8:2划分的训练集和验证集|
|cascade|train_epoch11|0.534|0.49264280|train|val|使用的是8:2划分的训练集和验证集|
|cascade|train_A_epoch10||0.50237704|train_A|未验证，直接提交测试|
|cascade|train_A_epoch11||0.50403275|train_A|**未验证，直接提交测试，因为验证集也包括在训练数据中。**|**目前epoch11是cascade跑trian_A精度最高的**|
|cascade|train_A_epoch12||0.50280786|train_A|未验证，直接提交测试|
|cascade|train_A_ep11+test2k_ep2（test2k是指那53张2k图）||**0.51166442**|train_A_ep11+test2k_ep2|未验证，直接提交测试|**目前train_A_ep11+test2k_ep2是使用专家模型精度最高的**|
|cascade|train_A_ep11+test2k_ep3||0.51089619|train_A_ep11+test2k_ep3|未验证，直接提交测试|专家模型，跑test，epoch2好于epoch3|
|cascade|train_A_ep11+test2k_ep4||0.50999959|train_A_ep11+test2k_ep4|未验证，直接提交测试|专家模型，跑test，epoch2好于epoch4|
|yolov5|exp5_37/50|0.5068|0.46138582|train|val|1.使用的是8:2划分的训练集和验证集；2.train size:640,val size:640,test size:896，并使用了TTA|
|||||分割线：下面的train和val就是wmy划分的train和val，val是和测试集同分布的
|yolov5|exp23_14/20|0.4878||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_15/20|0.4819||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_16/20|0.489||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_17/20|0.4929||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_18/20|0.4938||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_20/20|0.4975|0.47900757|train_wmy|val_test2k_1200|train size:2048,val size:2048,test size:2656,TTA|
|yolov5|exp23_20/20|0.4975|0.30054438|train_wmy|val_test2k_1200|train size:2048,val size:2048,test size:2656,TTA,iou_thres=0.94,agnostic_nms=True|
|yolov5|exp28_24/30|0.4674||train_wmy|val_test2k_1200|train 640 val 640 batch_size 2 worker 2(原写的8，但跑的时候是2),共跑了9.137个小时 17min/epoch|
|yolov5|train_20/24|0.4691||train_wmy|val_test2k_1200|**结论:20个epoch是最合适的；3卡和4卡的训练速度更快** train 640 val 640 batch_size 8,在4卡上，共跑了5.65个小时|
|yolov5|train_A_15/15|0.5537||train_A|val_test2k_1200|15epoch欠拟合，在2卡上跑了1.34h|
|yolov5|train_A_24/24|0.5873||train_A|val_test2k_1200|24epoch应该是过拟合，在3卡上跑了5.63h|
|yolov5|exp65_train_12/15|0.4614|0.45826797|train_wmy|val_test2k_1200|12epoch并不是最佳epoch,欠拟合|
|yolov5|exp65_train_15/15|0.46|0.46128544|train_wmy|val_test2k_1200|15epoch也不是最佳epoch,欠拟合|
|yolov5|exp64_train_20/20|0.4691|0.46670005|train_wmy|val_test2k_1200|20epoch应该是yolo最佳epoch|


|模型|epoch |验证结果|A榜评测结果|训练集|验证集|备注|
|----|-----|---------|-----------------|------|----|---|
|cascade|epoch11|0.507|0.49029607|train_wmy|val_test2k_1200|epoch 11,训练集和验证集不相交，验证集是wmy按照A榜测试集的分布划分出来的|
|cascade|epoch10|0.532|0.49245347|train|val|使用的是8:2划分的训练集和验证集|
|cascade|epoch11|0.534|0.49264280|train|val|使用的是8:2划分的训练集和验证集|
|cascade|epoch11||0.50403275|train_A|未验证，直接提交测试|**目前epoch11是cascade跑trian_A精度最高的**|
|cascade|epoch12||0.50280786|train_A|未验证，直接提交测试|
|cascade|train_A_ep11+test2k_ep2（test2k是指那53张2k图）||**0.51166442**|train_A_ep11+test2k_ep2|未验证，直接提交测试|**目前train_A_ep11+test2k_ep2是使用专家模型精度最高的**|
|cascade|train_A_ep11+test2k_ep4||0.50999959|train_A_ep11+test2k_ep4|未验证，直接提交测试|专家模型，跑test，epoch2好于epoch4|
|yolov5|exp5_37/50|0.5068|0.46138582|train|val|1.使用的是8:2划分的训练集和验证集；2.train size:640,val size:640,test size:896，并使用了TTA|
|||||分割线：下面的train和val就是wmy划分的train和val，val是和测试集同分布的
|yolov5|exp23_14/20|0.4878||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_15/20|0.4819||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_16/20|0.489||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_17/20|0.4929||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_18/20|0.4938||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_20/20|0.4975|0.47900757|train_wmy|val_test2k_1200|train size:2048,val size:2048,test size:2656,TTA|
|yolov5|exp23_20/20|0.4975|0.30054438|train_wmy|val_test2k_1200|train size:2048,val size:2048,test size:2656,TTA,iou_thres=0.94,agnostic_nms=True|
|yolov5|exp28_24/30|0.4674||train_wmy|val_test2k_1200|train 640 val 640 batch_size 2 worker 2(原写的8，但跑的时候是2),共跑了9.137个小时 17min/epoch|
|yolov5|train_20/24|0.4691||train_wmy|val_test2k_1200|**结论:20个epoch是最合适的；3卡和4卡的训练速度更快** train 640 val 640 batch_size 8,在4卡上，共跑了5.65个小时|
|yolov5|train_A_15/15|0.5537||train_A|val_test2k_1200|15epoch欠拟合，在2卡上跑了1.34h|
|yolov5|train_A_24/24|0.5873||train_A|val_test2k_1200|24epoch应该是过拟合，在3卡上跑了5.63h|
|yolov5|exp65_train_12/15|0.4614|0.45826797|train_wmy|val_test2k_1200|12epoch并不是最佳epoch,欠拟合|
|yolov5|exp65_train_15/15|0.46|0.46128544|train_wmy|val_test2k_1200|15epoch也不是最佳epoch,欠拟合|
|yolov5|exp64_train_20/20|0.4691|0.46670005|train_wmy|val_test2k_1200|20epoch应该是yolo最佳epoch|

