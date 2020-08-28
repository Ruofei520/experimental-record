# experimental-record
|模型|epoch |验证结果|A榜评测结果|训练集|验证集|备注|
|----|-----|---------|-----------------|------|----|---|
|cascade|epoch11|0.507|0.49029607|train_wmy|val_test2k_1200|epoch 11,训练集和验证集不相交，验证集是wmy按照A榜测试集的分布划分出来的|
|cascade|epoch10|0.532|0.49245347|train|val|使用的是8:2划分的训练集和验证集|
|cascade|epoch11|0.534|0.49264280|train|val|使用的是8:2划分的训练集和验证集|
|yolov5|exp5_37/50|0.5068|0.46138582|train|val|1.使用的是8:2划分的训练集和验证集；2.train size:640,val size:640,test size:896，并使用了TTA|
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

