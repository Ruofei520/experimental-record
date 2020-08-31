# experimental-record
数据集说明：

train_A:官方给的所有训练数据，共6575张

train,val：官方给的训练数据集按照8:2划分的。

train_wmy和val_test2k_1200是wmy划分的数据集，val_test2k_1200加入了53张2k图，和测试集同分布，且与训练集没有交集

train_wmy:5428张，val_test2k_1200:1200。在wmy的容器中，是train、val

train_all:6628张，train_A+test2k=6575+53=6628张

|模型|epoch |验证结果|A榜评测结果|训练集|验证集|备注|
|----|-----|---------|-----------------|------|----|---|
|cascade|train_epoch11|0.507|0.49029607|train_wmy|val_test2k_1200|epoch 11,训练集和验证集不相交，验证集是wmy按照A榜测试集的分布划分出来的|
|cascade|trian_epoch10|0.532|0.49245347|train|val|使用的是8:2划分的训练集和验证集|
|cascade|train_epoch11|0.534|0.49264280|train|val|使用的是8:2划分的训练集和验证集|
|cascade|train_A_epoch10||0.50237704|train_A|未验证，直接提交测试|
|cascade|train_A_epoch11||0.50403275|train_A|**未验证，直接提交测试，因为验证集也包括在训练数据中。**|**目前epoch11是cascade跑trian_A精度最高的**|
|cascade|train_A_epoch12||0.50280786|train_A|未验证，直接提交测试|
|cascade|train_A+waterweeds_epoch11||0.50232164|train_A+waterweeds|未验证，直接提交测试||**trian_A中加了水草后，下降0.17个点**|
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
