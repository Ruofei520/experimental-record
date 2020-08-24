import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

# 统计训练集（测试集）图片尺寸分布，并绘制饼图
img_dir='/root/python_project/underwater_detection/mmdetection/data/underwater/train_all/image' # 存放图片的文件夹
result_path='/root/python_project/underwater_detection/mmdetection/underwater_related_v2/my_tools/result' # 存放绘图结果的文件夹
pie_title='train_all' # 绘制出来的饼图名称
# 画扇形统计图
def draw_pie(img_size_info):
    img_size = list()
    img_size_number = list()
    for k, v in img_size_info.items():
        img_size.append(k)
        img_size_number.append(v)
    #fig=plt.figure()
    plt.pie(img_size_number,labels=img_size,autopct='%1.2f%%') # 画饼图（数据，数据对应的标签，百分数保留两位小数点）
    plt.title(pie_title+'_img_size_info,total number: '+str(sum(img_size_number))+' images.')
    plt.savefig(os.path.join(result_path,pie_title+'_img_size_info'))
# 取数据,统计每个图片尺寸出现的次数
def img_size_info(img_dir):
    img_size_info=dict() #{'image_size':num}
    for i in tqdm(os.listdir(img_dir)):
        img=cv2.imread(os.path.join(img_dir,i))
        shape=str(img.shape[0])+'*'+str(img.shape[1])
        number=img_size_info.get(shape,0)
        if number==0:
            img_size_info[shape]=1
        else:
            img_size_info[shape]+=1
    print(img_size_info)
    return img_size_info

if __name__=='__main__':
    draw_pie(img_size_info(img_dir))
