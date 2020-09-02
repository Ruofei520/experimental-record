import os
import cv2
import random
import pandas as pd
import xml.etree.ElementTree as ET

def mytest():
    a = [i for i in range(10)]
    random.shuffle(a)
    print(a)
    b = (1024, 2048)
    if isinstance(b, int):
        print("hh")


def read_dict(filepath):
    f = open(filepath, 'r', )
    a = f.read()
    # 读成字典格式
    dict_data = eval(a)
    # print(dict_data)
    f.close()
    return dict_data


def write_dict(filepath, dict_data):
    f = open(filepath, 'w')
    f.write(str(dict_data))
    f.close()


def fuse_2k_into_train_all():
    """生成各尺寸图片数目与测试集相同的验证集"""
    # 2k图先加入到全部训练集中  图片数目 6575 + 53
    train_all_img_path = 'underwater/train_all/image'
    train_all_box_path = 'underwater/train_all/box'
    img_2k_path = 'test_2k/image'
    box_2k_path = 'test_2k/box'
    # imgs = os.listdir(img_2k_path)
    # boxs = os.listdir(box_2k_path)
    # imgs.sort()
    # boxs.sort()
    # # 加进去的图像从006576.jpg开始命名
    # index = 6576
    # # 加入图片
    # for img in imgs:
    #     im = cv2.imread(os.path.join(img_2k_path, img))
    #     im_target_name = "00" + str(index) + ".jpg"
    #     cv2.imwrite(os.path.join(train_all_img_path, im_target_name), im)
    #     index += 1
    #
    # index = 6576
    # # 加入box
    # # box从006576.xml开始命名
    # for box in boxs:
    #     bo = open(os.path.join(box_2k_path, box), 'r').readlines()
    #     bo_target_name = "00" + str(index) + ".xml"
    #     f = open(os.path.join(train_all_box_path, bo_target_name), 'w')
    #     f.writelines(bo)
    #     index += 1
    # # 加入之后总图片数目
    # img_cnt = len(os.listdir(train_all_img_path))
    # box_cnt = len(os.listdir(train_all_box_path))
    # print(img_cnt, box_cnt)
    # 按尺寸进行归类
    shape_dict = {}
    train = []
    val = []
    num_2k = {'1440*2560': 32, '1536*2048': 21}
    # 验证集中每种尺寸需要的数量
    nums = {'2160*3840': 1053, '405*720': 52, '1080*1920': 42}
    for ind, img in enumerate(os.listdir(train_all_img_path)):
        print("处理到第{}张图片".format(ind + 1))
        im = cv2.imread(os.path.join(train_all_img_path, img))
        # 以图像的高、宽拼接成的字符串做key
        size = str(im.shape[0]) + '*' + str(im.shape[1])
        # 2k图直接加入验证集 不放入训练集 保证数据不重叠
        if size in num_2k.keys():
            # train.append(img)
            val.append(img)
            continue
        if size not in nums:
            train.append(img)
            continue
        if size not in shape_dict.keys():
            shape_dict[size] = []
        shape_dict[size].append(img)

    print("不同尺寸进行归类...")

    # 每种尺寸均随机划分
    random.seed(7)
    for key in nums.keys():
        data = shape_dict[key]
        ids = [i for i in range(len(data))]
        random.shuffle(ids)
        num = nums[key]
        # 前num张加到验证集 其余为训练集
        for i in range(num):
            val.append(data[ids[i]])
        for j in range(num, len(data)):
            train.append(data[ids[j]])
    # 保存到文件
    write_dict("train.txt", train)
    write_dict("val.txt", val)
    print("归类结果已保存到文件")


def split_into_train_val():
    """
    从保存的txt中生成相应的训练集和测试集
    :return:
    """
    train = read_dict('train.txt')
    val = read_dict('val.txt')
    print(len(train))  # 5481
    print(len(val))  # 1200
    train_all_img_path = 'underwater/train_all/image'
    train_all_box_path = 'underwater/train_all/box'
    train_dir = "train_0"
    val_dir = "val_0"
    print("开始划分训练集和验证集...")
    # 划分出训练集和验证集
    for idx, item in enumerate(train):
        print("正在生成训练集第{}张图片".format(idx + 1))
        im = cv2.imread(os.path.join(train_all_img_path, item))
        cv2.imwrite(os.path.join(train_dir, "image", item), im)
        box_name = item[:-4] + ".xml"
        bo = open(os.path.join(train_all_box_path, box_name), 'r').readlines()
        f = open(os.path.join(train_dir, "box", box_name), 'w')
        f.writelines(bo)
    for idx, item in enumerate(val):
        print("正在生成验证集第{}张图片".format(idx + 1))
        im = cv2.imread(os.path.join(train_all_img_path, item))
        cv2.imwrite(os.path.join(val_dir, "image", item), im)
        box_name = item[:-4] + ".xml"
        bo = open(os.path.join(train_all_box_path, box_name), 'r').readlines()
        f = open(os.path.join(val_dir, "box", box_name), "w")
        f.writelines(bo)
    print('划分完成')


def yolov5_add_pseudo_labels():
    """
    利用yolov5推理结果（txt）制作带有伪标签的新训练集
    :return:
    """
    # 伪标签加入的数据从007000.jpg开始命名
    index = 7000
    data_source_path = '/home/underwater/yolov5/data/images/val'
    label_source_path = '/home/underwater/yolov5/inference/pseudo_val_labels_conf0.4'
    dest_image_path = '/home/underwater/yolov5/data_pseudo_labels/images/train'
    dest_label_path = '/home/underwater/yolov5/data_pseudo_labels/labels/train'
    images = os.listdir(data_source_path)
    for ids, image in enumerate(images):
        print("正在生成第{}个伪标签数据".format(ids + 1))
        name = image.split('.')[0]
        im = cv2.imread(os.path.join(data_source_path, image))
        cv2.imwrite(os.path.join(dest_image_path, "00" + str(index) + ".jpg"), im)
        # 由于置信度阈值设置较高 有的数据点没有检测结果输出 需要生成一个空目标文件
        try:
            label = open(os.path.join(label_source_path, name + ".txt"), 'r').readlines()
            f = open(os.path.join(dest_label_path, "00" + str(index) + ".txt"), 'w')
            f.writelines(label)
        except:
            # 写一个空文件
            f = open(os.path.join(dest_label_path, "00" + str(index) + ".txt"), 'w')
            f.writelines("")

        index += 1


def mmdect_add_pseudo_labels_csv2txt():
    """
    利用mmdection框架最后生成的csv文件来制作testA伪标签 用于yolov5模型
    其中2k图直接使用真实标签  非2k图才使用伪标签  2k图的序号28-80需要跳过
    :return:
    """
    # 要加入的伪标签数据的序号从7000.jpg开始
    # 注意文件名的映射 A榜测试中是1-1200 加入后相应的是7000-8199  同时要跳过序号28-80
    idx = 7000
    csv_path = '/home/underwater/use_for_generate_pseudo_labels_51166442_fusion_2k_ep2_no2k_ep11.csv'
    img_source = '/home/underwater/test-A-image'
    dest_image_path = '/home/underwater/yolov5/data_train_all_with_waterweeds_pesudo/images/train'
    dest_label_path = '/home/underwater/yolov5/data_train_all_with_waterweeds_pesudo/labels/train'
    data = pd.read_csv(csv_path).values
    # data = sorted(data, key=lambda x: x[1])
    print(data[0])
    # exit(0)
    # 取出csv中每一行
    # 形如['holothurian' '000916.xml' 0.9964924999999999 2624.923 930.2709 3192.3784 1168.5225]

    # 必要的话可以将先前已经做好的标签文件删去
    for i in range(7000, 8200):
        label_txt = "00" + str(i) + ".txt"
        file = os.path.join(dest_label_path, label_txt)
        if os.path.exists(file):
            os.remove(file)

    # 先把标签补充进去
    for k, row in enumerate(data):
        print("正在处理csv文件的第{}行".format(k+1))
        # 读出文件序号 28-80跳过
        file_id = int(row[1].split('.')[0])
        if 28 <= file_id <= 80:
            continue
        # 为保证伪标签具有一定的可信度 设置置信度阈值0.4
        if row[2] < 0.4:
            continue
        # txt以追加的方式写入
        target_name = "00" + str(file_id + 6999) + ".txt"
        f_w = open(os.path.join(dest_label_path, target_name), 'a+')
        # 获取图片高、宽
        img_name = row[1].split('.')[0] + '.jpg'
        img = cv2.imread(os.path.join(img_source, img_name))

        img_height = img.shape[0]
        img_width = img.shape[1]
        name = row[0]
        # 根据obj确定标签
        if name == 'holothurian':
            label = 0
        elif name == 'echinus':
            label = 1
        elif name == 'scallop':
            label = 2
        elif name == 'starfish':
            label = 3
        else:
            continue
        xmin = row[3]
        ymin = row[4]
        xmax = row[5]
        ymax = row[6]
        # 获取box的宽度和高度
        object_width = xmax - xmin
        object_height = ymax - ymin
        # 获取box的中心点坐标
        x_center = xmin + object_width / 2
        y_center = ymin + object_height / 2

        # 归一化,除以图片宽度，长度
        x_center = str(x_center / img_width)
        y_center = str(y_center / img_height)
        object_width = str(object_width / img_width)
        object_height = str(object_height / img_height)
        f_w.write(str(label) + ' ' + x_center + ' ' + y_center + ' ' + object_width + ' ' + object_height + '\n')

    # 没有检测出物体的图片需要补一个空txt做标签
    for i in range(7000, 8200):
        # 跳过2k图
        if 7027 <= i <= 7079:
            continue
        name = "00" + str(i) + ".txt"
        file = os.path.join(dest_label_path, name)
        if not os.path.exists(file):
            f = open(file, 'w')
            f.write("")
    # 再把测试A的图像补充到训练集
    files = os.listdir(img_source)
    for index, img_name in enumerate(files):
        print("正在拷贝测试A中第{}张图像到训练集".format(index+1))
        idx = int(img_name.split(".")[0])
        if 28 <= idx <= 80:
            continue
        tar_name = "00" + str(idx + 6999) + ".jpg"
        img = cv2.imread(os.path.join(img_source, img_name))
        cv2.imwrite(os.path.join(dest_image_path, tar_name), img)


# xml中增加换行符
def __indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            __indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def mmdect_pesudo_csv2xml():
    """
    利用csv文件生成xml制作testA的伪标签 用于cascade模型
    :return: 
    """
    # 新加入的伪标签数据从7000.jpg开始命名
    # 注意文件名的映射 A榜测试中是1-1200 加入后相应的是7000-8199  同时要跳过序号28-80
    idx = 7000
    csv_path = '/root/python_project/underwater_detection/mmdetection/data/underwater/2020_9_2_15_22_make_pseudo_for_cascade_htc_train_A_ep11.csv'
    img_source = '/root/python_project/underwater_detection/mmdetection/data/underwater/test-A-image'
    dest_image_path = '/root/python_project/underwater_detection/mmdetection/data/underwater/train_all_pseudo/image'
    dest_label_path = '/root/python_project/underwater_detection/mmdetection/data/underwater/train_all_pseudo/box'
    data = pd.read_csv(csv_path).values
    print(data[0])

    # 必要的话可以将先前已经做好的标签文件删去
    for i in range(7000, 8200):
        label_xml = "00" + str(i) + ".xml"
        file = os.path.join(dest_label_path, label_xml)
        if os.path.exists(file):
            os.remove(file)

    # 先把标签补充进去
    for k, row in enumerate(data):
        print("正在处理csv文件的第{}行".format(k + 1))
        # 读出文件序号 28-80跳过
        file_id = int(row[1].split('.')[0])
        if 28 <= file_id <= 80:
            continue
        # 为保证伪标签具有一定的可信度 设置置信度阈值0.4
        if row[2] < 0.4:
            continue
        target_name = "00" + str(file_id + 6999) + ".xml"

        # 获取图片高、宽
        img_name = row[1].split('.')[0] + '.jpg'
        img = cv2.imread(os.path.join(img_source, img_name))
        img_height = img.shape[0]
        img_width = img.shape[1]

        # python写入xml
        # 如果xml不存在将创建并填入相应的信息
        target_xml = os.path.join(dest_label_path, target_name)
        if not os.path.exists(target_xml):
            root = ET.Element('annotation')  # 创建节点
            tree = ET.ElementTree(root)  # 创建文档
            element_xml_idx = ET.Element('frame')
            element_xml_idx.text = "00" + str(file_id + 6999)
            element_size = ET.Element("size")
            # 写入图像宽高
            ele_width = ET.Element("width")
            ele_width.text = str(img_width)
            ele_height = ET.Element("height")
            ele_height.text = str(img_height)
            element_size.append(ele_width)
            element_size.append(ele_height)
            # 写入idx和图像尺寸
            root.append(element_xml_idx)
            root.append(element_size)
            tree.write(target_xml, encoding='utf-8', xml_declaration=True)

        # csv中读出的bbox信息

        obj_name = row[0]
        xmin = row[3]
        ymin = row[4]
        xmax = row[5]
        ymax = row[6]

        # 否则读出xml, 追加进去bbox信息
        tree = ET.parse(target_xml)
        root = tree.getroot()
        element_obj = ET.Element("object")
        # 准备object name
        element_obj_name = ET.Element("name")
        element_obj_name.text = obj_name
        # 准备bbox
        element_bbox = ET.Element("bndbox")
        ele_xmin = ET.Element("xmin")
        ele_ymin = ET.Element("ymin")
        ele_xmax = ET.Element("xmax")
        ele_ymax = ET.Element("ymax")
        ele_xmin.text = str(xmin)
        ele_ymin.text = str(ymin)
        ele_xmax.text = str(xmax)
        ele_ymax.text = str(ymax)
        element_bbox.append(ele_xmin)
        element_bbox.append(ele_ymin)
        element_bbox.append(ele_xmax)
        element_bbox.append(ele_ymax)
        # 填入
        element_obj.append(element_obj_name)
        element_obj.append(element_bbox)
        # 将这个对象放入root节点
        root.append(element_obj)
        # 修改格式
        __indent(root, 0)
        # 写回文件
        tree.write(target_xml, encoding='utf-8', xml_declaration=True)

    # 没有检测出物体的图片需要补一个空xml做标签
    for i in range(7000, 8200):
        # 跳过2k图
        if 7027 <= i <= 7079:
            continue
        name = "00" + str(i) + ".xml"
        file = os.path.join(dest_label_path, name)
        if not os.path.exists(file):
            root = ET.Element('annotation')  # 创建节点
            tree = ET.ElementTree(root)  # 创建文档
            tree.write(file, encoding='utf-8', xml_declaration=True)

    # 再把测试A的图像补充到训练集
    files = os.listdir(img_source)
    for index, img_name in enumerate(files):
        print("正在拷贝测试A中第{}张图像到训练集".format(index + 1))
        idx = int(img_name.split(".")[0])
        if 28 <= idx <= 80:
            continue
        tar_name = "00" + str(idx + 6999) + ".jpg"
        img = cv2.imread(os.path.join(img_source, img_name))
        cv2.imwrite(os.path.join(dest_image_path, tar_name), img)


def mytest():
    a = "00096"
    b = int(a)
    print(b)


if __name__ == '__main__':
    # fuse_2k_into_train_all()
    # split_into_train_val()
    # mytest()
    # add_pseudo_labels()
    # mmdect_add_pseudo_labels()
    # mytest()
    mmdect_pesudo_csv2xml()

