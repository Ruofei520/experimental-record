import os
import xml.etree.ElementTree as ET


indir = '/root/python_project/underwater_detection/mmdetection/data/underwater/val/box'  # xml目录
outdir = '/root/python_project/underwater_detection/yolov5/data/underwater/val/labels'  # txt目录
def xml_to_txt(indir, outdir):

    for i, file in enumerate(os.listdir(indir)):

        file_save = file.split('.')[0] + '.txt'
        file_txt=os.path.join(outdir,file_save)

        f_w = open(file_txt, 'w')

        # actual parsing
        tree = ET.parse(os.path.join(indir,file))
        root = tree.getroot() # 获取根节点,<annotations>
        img_width=float(root.find('size').find('width').text)
        img_height=float(root.find('size').find('height').text)

        for obj in root.iter('object'):

            name = obj.find('name').text  # 这里获取多个框的名字，底下是获取每个框的位置

            if name=='holothurian':
                label=0
            elif name=='echinus':
                label=1
            elif name=='scallop':
                label=2
            elif name=='starfish':
                label=3
            else:
                continue #如果是其他object则跳过

            xmlbox = obj.find('bndbox')
            xmin = float(xmlbox.find('xmin').text)
            xmax = float(xmlbox.find('xmax').text)
            ymin = float(xmlbox.find('ymin').text)
            ymax = float(xmlbox.find('ymax').text)
            # print xn
            object_width=xmax-xmin
            object_height=ymax-ymin
            x_center=xmin+object_width/2
            y_center=ymin+object_height/2

            # 归一化,除以图片宽度，长度
            x_center=str(x_center/img_width)
            y_center=str(y_center/img_height)
            object_width=str(object_width/img_width)
            object_height=str(object_height/img_height)

            f_w.write(str(label) + ' ' + x_center + ' ' + y_center + ' ' + object_width + ' ' + object_height + '\n')

        f_w.close()
if __name__=='__main__':
    xml_to_txt(indir, outdir)