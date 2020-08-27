# experimental-record
|实验序号|模型|epoch|验证结果|A榜评测结果|训练集|验证集|策略|备注|
|---|---|---|-----|------|-----|----|------|----|
|1|yolov5|20/20|0.4868|0.47103806|train_without_2k_num5428|val_num1200(与测试集同分布)|2k图存在于验证集中而不出现在训练集|img_size train 1024 val 1344 test 1344   batch_size 8|
|2|yolov5|5/5 微调|0.4818|0.45999952|train_with_test_pseudo_labels_num6628|val_num1200(同上)|伪标签：**testA的数据**推理出标签后补充到训练集中|train 1024 val 1344 test 1344 batch_size 4 **conf 0.4**|
|3|yolov5|1/5 微调|0.4856|0.47495014|train_with_val_pseudo_labels_num6628|val_num1200(同上)|伪标签：**val的数据**推理出标签后补充到训练集中|train 1024 val 1344 test 1344 batch_size 4 **conf 0.4**|
|4|yolov5|29/30|0.4639||train_without_2k_num5428|val_num1200(同上)|**Baseline**|train 640 val 640 test 896 batch_size 16 约14min/epoch|
|5|yolov5|27/30|0.4759|0.46128412|train_without_2k_num5428|val_num1200(同上)|**Baseline**|train 640 val 640 test 896 batch_size 8 约15min/epoch|
|6|yolov5|28/30|0.4689||train_without_2k_num5428|val_num1200(同上)|**Baseline**|train 640 val 640 test 896 batch_size 4 约15min/epoch|
|7|yolov5|30/30|0.6474|**0.48234922**|train_all|val_num1200|全部已知标签的数据做训练集(包括2k图)|train 640 val 640 test 896 batch_size 8|
|8|yolov5|30/30|0.6064|0.46865816|train_A|val_num1200|官方发布的A榜训练集|train 640 val 640 test 896 batch_size 8|
|9|yolov5|30/30|0.6513|0.48108739|train_all|val_num1200|全部已知标签的数据做训练集(包括2k图) + **水草**|train 640 val 640 test 896 batch_size 8|
|10|yolov5|/15|||train_without_2k_num5428|val_num1200(与测试集同分布)|与实验1对比，验证epochs数目对结果的影响，并保存每个epoch的结果|img_size train 640 val 640 test 896  batch_size 8|
|11|yolov5|/20|||train_without_2k_num5428|val_num1200(与测试集同分布)|与实验1对比，验证epochs数目对结果的影响，并保存每个epoch的结果|img_size train 640 val 640 test 896  batch_size 8|

