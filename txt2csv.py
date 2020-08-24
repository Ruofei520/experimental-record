# 将YOLOv2使用detect.py跑测试集生成的txt文件转为可提交的csv文件
import os
import csv
from tqdm import tqdm
import cv2
txt_dir='/root/python_project/underwater_detection/yolov5/runs/exp5/detect_result_v2' # txt所在目录
csv_path='/root/python_project/underwater_detection/yolov5/runs/exp5/weights' # 生成的csv文件存放的根目录
csv_name='exp5_best.csv' # 生成的csv文件的名称
test_img_dir='/root/python_project/underwater_detection/mmdetection/data/underwater/test-A-image' # 测试集图片目录，
# 需要获取图片的height和width,进行反归一化。因为txt中的数据是label,confidence,center_x,center_y,width,height,且是归一化过的
def txt2csv(txt_dir,csv_path):
    csv_data=list()
    fileHeader = ['name', 'image_id', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']
    csv_data.append(fileHeader)
    for file in tqdm(os.listdir(txt_dir)):
        if file[-4:]!='.txt':
            continue
        else:
            img_name = file[:-4] + '.jpg'
            img = cv2.imread(os.path.join(test_img_dir, img_name))
            img_height = float(img.shape[0])
            img_width = float(img.shape[1])
            txt = open(os.path.join(txt_dir, file))
            for line in txt.readlines():
                bbox=[]
                line=line.split(' ')
                if line[0]==str(0):
                    bbox.append('holothurian')
                elif line[0]==str(1):
                    bbox.append('echinus')
                elif line[0]==str(2):
                    bbox.append('scallop')
                elif line[0]==str(3):
                    bbox.append('starfish')
                else:
                    assert line[0]<=3, ('index out of range ,index<4!')
                bbox.append(file[:-4]+'.xml')
                bbox.append(line[1])

                center_x=float(line[2])*img_width
                center_y=float(line[3])*img_height
                width=float(line[4])*img_width
                height=float(line[5])*img_height
                xmin=center_x-width/2
                ymin=center_y-height/2
                xmax=center_x+width/2
                ymax=center_y+height/2

                bbox.append(str(xmin))
                bbox.append(str(ymin))
                bbox.append(str(xmax))
                bbox.append(str(ymax))
                csv_data.append(bbox)
    csv_file=open(os.path.join(csv_path,csv_name),'w')
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)
    csv_file.close()



if __name__=='__main__':
    txt2csv(txt_dir,csv_path)
