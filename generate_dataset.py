import os
import cv2
import random


def mytest():
    a = [i for i in range(10)]
    random.shuffle(a)
    print(a)
    b = (1024, 2048)
    if isinstance(b, int):
        print("hh")


def read_dict(filepath):
    f = open(filepath, 'r',)
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
        print("处理到第{}张图片".format(ind+1))
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
        print("正在生成训练集第{}张图片".format(idx+1))
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


def add_pseudo_labels():
    """
    制作带有伪标签的新训练集
    :return:
    """
    # 伪标签加入的数据从007000.jpg开始命名
    index = 7000
    data_source_path = '/home/underwater/yolov5/inference/test-A-image'
    label_source_path = '/home/underwater/yolov5/inference/pseudo_labels_conf0.5'
    dest_image_path = '/home/underwater/yolov5/data_pseudo_labels/images/train'
    dest_label_path = '/home/underwater/yolov5/data_pseudo_labels/labels/train'
    images = os.listdir(data_source_path)
    for ids, image in enumerate(images):
        print("正在生成第{}个伪标签数据".format(ids+1))
        name = image.split('.')[0]
        im = cv2.imread(os.path.join(data_source_path, image))
        cv2.imwrite(os.path.join(dest_image_path, "00" + str(index) + ".jpg"), im)
        # 由于置信度阈值设置较高 有的数据点没有检测结果输出 需要生成一个空目标文件
        try:
            label = open(os.path.join(label_source_path, name+".txt"), 'r').readlines()
            f = open(os.path.join(dest_label_path, "00" + str(index) + ".txt"), 'w')
            f.writelines(label)
        except:
            # 写一个空文件
            f = open(os.path.join(dest_label_path, "00" + str(index) + ".txt"), 'w')
            f.writelines("")
        
        index += 1

    
if __name__ == '__main__':
    # fuse_2k_into_train_all()
    # split_into_train_val()
    # mytest()
    add_pseudo_labels()