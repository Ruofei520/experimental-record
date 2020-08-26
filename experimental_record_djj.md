# experimental-record
|模型|epoch |验证结果|A榜评测结果|训练集|验证集|备注|
|----|-----|---------|-----------------|------|----|---|
|cascade|epoch11|0.507|0.49029607|train_wmy|val_test2k_1200|epoch 11,训练集和验证集不相交，验证集是wmy按照A榜测试集的分布划分出来的|
|cascade|epoch10|0.532|0.49245347|train|val|使用的是8:2划分的训练集和验证集|
|cascade|epoch11|0.534|0.49264280|train|val|使用的是8:2划分的训练集和验证集|
|yolov5|exp5_36/49|0.5068|0.46138582|train|val|1.使用的是8:2划分的训练集和验证集；2.train size:640,val size:640,test size:896，并使用了TTA|
|yolov5|exp23_14/19|0.4878||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_15/19|0.4819||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_16/19|0.489||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_17/19|0.4929||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_18/19|0.4938||train_wmy|val_test2k_1200|train size:2048,val size:2048|
|yolov5|exp23_19/19|0.4975|0.47900757|train_wmy|val_test2k_1200|train size:2048,val size:2048,test size:2656,TTA|
|yolov5|exp23_19/19|0.4975|0.30054438|train_wmy|val_test2k_1200|train size:2048,val size:2048,test size:2656,TTA,iou_thres=0.94,agnostic_nms=True|
|yolov5|exp28_24/30|0.4674|||train_wmy|val_test2k_1200|train 640 val 640 batch_size 2 worker 2(原写的8，但跑的时候是2),共跑了9.137个小时 17min/epoch|

