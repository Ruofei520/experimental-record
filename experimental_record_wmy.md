# experimental-record
|模型|epoch|验证结果|A榜评测结果|训练集|验证集|策略|备注|
|---|------|-------|----------|------|-----|----|---|
|yolov5|20/20|0.4868|0.47103806|train_without_2k_num5428|val_num1200(与测试集同分布)|2k图存在于验证集中而不出现在训练集|img_size train 1024 val 1344 test 1344   batch_size 8|
|yolov5|5/20|0.4818|0.45999952|train_with_test_pseudo_labels_num6628|val_num1200(同上)|伪标签：**testA的数据**推理出标签后补充到训练集中|train 1024 val 1344 test 1344 batch_size 4 **conf 0.4**|
|yolov5|1/20|0.4856|0.47495014|train_with_val_pseudo_labels_num6628|val_num1200(同上)|伪标签：**val的数据**推理出标签后补充到训练集中|train 1024 val 1344 test 1344 batch_size 4 **conf 0.4**|
|yolov5|29/30|0.4639||train_without_2k_num5428|val_num1200(同上)|**Baseline**|train 640 val 640 batch_size 16 约14min/epoch|
|yolov5|27/30|0.4759||train_without_2k_num5428|val_num1200(同上)|**Baseline**|train 640 val 640 batch_size 8 约15min/epoch|
|yolov5|28/30|0.4689||train_without_2k_num5428|val_num1200(同上)|**Baseline**|train 640 val 640 batch_size 4 约15min/epoch|
|yolov5||||train_all|val_num1200|所有已知标签的数据全部做训练集(包括2k图)|train 640 val 640 batch_size 8|
|yolov5||||train_A|val_num1200|官方发布的A榜训练集|train 640 val 640 batch_size 8|
|yolov5||||train_all|val_num1200|全部已知标签的数据(包括2k图) + **水草**|train 640 val 640 batch_size 8|

