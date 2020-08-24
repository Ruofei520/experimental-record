from argparse import ArgumentParser

from mmdet.apis import inference_detector, init_detector, show_result_pyplot

import os

import csv

from tqdm import tqdm


def main():
    parser = ArgumentParser()
    parser.add_argument('--img_dir',default='/root/python_project/underwater_detection/mmdetection/data/underwater/test-A-image', help='Image file')
    parser.add_argument('--config',default='/root/python_project/underwater_detection/mmdetection/underwater_related_v2/htc_train/cascade_rcnn_x101_64x4d_fpn_1x_coco.py', help='Config file')
    parser.add_argument('--checkpoint',default='/root/python_project/underwater_detection/mmdetection/underwater_related_v2/htc_train/epoch_10.pth', help='Checkpoint file')
    parser.add_argument('--csv',default='/root/python_project/underwater_detection/mmdetection/underwater_related_v2/htc_train/htc_ep10.csv',help='the path to save .csv file')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--score_thr', type=float, default=0.0001, help='bbox score threshold')
    parser.add_argument('--show_dir',default=None,help='where result image to save')
    parser.add_argument('--result_img_name',default=None)
    args = parser.parse_args()


    # build the model from a config file and a checkpoint file
    model = init_detector(args.config, args.checkpoint, device=args.device)

    # 文件头，一般就是数据名
    csv_data=[]
    fileHeader=['name','image_id','confidence','xmin','ymin','xmax','ymax']
    csv_data.append(fileHeader)
    img_number=len(os.listdir(args.img_dir))
    for img_name in tqdm(os.listdir(args.img_dir)):
        result=inference_detector(model, os.path.join(args.img_dir,img_name))
        for label,bboxes in enumerate(result):
            for bbox in bboxes:
                score=bbox[4]
                if score>args.score_thr:
                    bbox_info = []
                    if label == 0:
                        bbox_info.append('holothurian')
                    elif label == 1:
                        bbox_info.append('echinus')
                    elif label == 2:
                        bbox_info.append('scallop')
                    elif label == 3:
                        bbox_info.append('starfish')
                    else:
                        assert (i < 4), "index out of range,index <4."
                    bbox_info.append(img_name[:-4]+'.xml')
                    bbox_info.append(score)
                    for x_y in bbox[:4]:
                        bbox_info.append(x_y)
                    csv_data.append(bbox_info)
    csvFile = open(args.csv, 'w')
    writer=csv.writer(csvFile)
    writer.writerows(csv_data)
    csvFile.close()
    print('inference complete, total number of images:',img_number)
    # 如果要可视化，可以继续修改下面
    # test a single image
    # show the results
    #show_result_pyplot(model, args.img, result, score_thr=args.score_thr,show_dir=args.show_dir,result_img_name=args.result_img_name)

if __name__ == '__main__':
    main()
