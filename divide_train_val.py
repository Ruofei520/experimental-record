#划分验证集
#训练集与验证集比例8：2
#划分方法，每10个样本随机取2个作为验证集
import os
import random
path_train = "/root/python_project/underwater_detection/mmdetection/data/underwater_v2/UnderwaterDetection_roundA/train"#train文件夹的绝对路径，里面包含box与image两个文件夹
path_val = "/root/python_project/underwater_detection/mmdetection/data/underwater_v2/UnderwaterDetection_roundA/val"#val文件夹绝对路径，下有box与image两个文件夹，需要提前创建好

val = []
for i, box in enumerate(os.listdir(path_train+"/box"), 1):
    val.append(box[0:-4]) #保存10个样本
    if (i%10 == 0):
        val = random.sample(val, 2)#随机生生成2个作为val
        #将box移动到val/box文件夹
        os.rename(path_train+"/box/"+val[0]+".xml", path_val+"/box/"+val[0]+".xml")
        os.rename(path_train+"/box/"+val[1]+".xml", path_val+"/box/"+val[1]+".xml")
        #将image移动到val/image文件夹
        os.rename(path_train+"/image/"+val[0]+".jpg", path_val+"/image/"+val[0]+".jpg")
        os.rename(path_train+"/image/"+val[1]+".jpg", path_val+"/image/"+val[1]+".jpg")
        #重置val
        val = []




