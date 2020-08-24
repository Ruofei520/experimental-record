# experimental-record
|模型|epoch|验证结果|A榜评测结果|训练集|验证集|策略|备注|
|---|------|-------|----------|------|-----|----|
|yolov5|20|0.4868|0.47103806|train_without_2k_num5428|val_num1200|2k图存在于验证集中而不出现在训练集|img_size train 1024 val 1344 test 1344   batch_size 8|
|yolov5|4|0.4818|0.45999952|train_with_pesudo_labels_num6628|val_num1200|testA中数据推理出标签后将这部分数据补充到训练集中|train 1024 val 1344 test 1344 batch_size 4 conf 0.4 batch_size 4|
