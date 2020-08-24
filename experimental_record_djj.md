# experimental-record
|模型|epoch |验证结果|A榜评测结果|训练集|验证集|备注|
|----|-----|---------|-----------------|------|----|---|
|cascade|epoch11|0.507|0.49029607|train_wmy|val_test2k_1200|epoch 11,训练集和验证集不相交，验证集是wmy按照A榜测试集的分布划分出来的|
|cascade|epoch10|0.532|0.49245347|train|val|使用的是8:2划分的训练集和验证集|
|cascade|epoch11|0.534|0.49264280|train|val|使用的是8:2划分的训练集和验证集|
|yolov5|exp5_36/49|0.5068|0.46138582|train|val|1.使用的是8:2划分的训练集和验证集；2.train size:640,val size:640,test size:896，并使用了TTA|
