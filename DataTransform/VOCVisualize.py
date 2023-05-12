import os
import cv2
import re

pattens = ['name', 'xmin', 'ymin', 'xmax', 'ymax']


def get_annotations(xml_path):
    bbox = []
    with open(xml_path, 'r') as f:
        text = f.read().replace('\n', 'return')
        p1 = re.compile(r'(?<=<object>)(.*?)(?=</object>)')
        result = p1.findall(text)
        for obj in result:
            tmp = []
            for patten in pattens:
                p = re.compile(r'(?<=<{}>)(.*?)(?=</{}>)'.format(patten, patten))
                if patten == 'name':
                    tmp.append(p.findall(obj)[0])
                else:
                    tmp.append(int(float(p.findall(obj)[0])))
            bbox.append(tmp)
    return bbox


def save_viz_image(image_dir, image_name, xml_path, save_path):
    bbox = get_annotations(xml_path)
    image_path = os.path.join(image_dir, image_name)
    image = cv2.imread(image_path)
    for info in bbox:
        cv2.rectangle(image, (info[1], info[2]), (info[3], info[4]), (255, 0, 0), thickness=2)
        cv2.putText(image, info[0], (info[1], info[2]), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 2)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    name = os.path.join(save_path, image_name)
    cv2.imwrite(name, image)


if __name__ == '__main__':
    image_dir = 'D:\BaiduNetdiskDownload\VOC2028\VOC2028\DataEnhance\JPEGImages'
    xml_dir = 'D:\BaiduNetdiskDownload\VOC2028\VOC2028\DataEnhance\Annotations'
    save_dir = 'D:\BaiduNetdiskDownload\VOC2028\VOC2028\DataEnhance\VOC_Visualize'
    cnt=0
    image_list = os.listdir(image_dir)
    for i in image_list:
        if cnt <30:
            xml_path = os.path.join(xml_dir, i.replace('.jpg', '.xml'))
            print('Annotations Path: {}'.format(xml_path))
            save_viz_image(image_dir, i, xml_path, save_dir)
            cnt = cnt+1
