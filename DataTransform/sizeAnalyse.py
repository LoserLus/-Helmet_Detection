import os
import xml.etree.ElementTree as ET
from math import sqrt

from tqdm import trange

result = {
    'person_s': 0,
    'person_m': 0,
    'person_l': 0,
    'helmet_s': 0,
    'helmet_m': 0,
    'helmet_l': 0
}
area = {
    'person_s': 0,
    'person_m': 0,
    'person_l': 0,
    'helmet_s': 0,
    'helmet_m': 0,
    'helmet_l': 0
}
box_wh_p = {}
box_wh_h = {}


def GetAnnotBoxLoc(AnotPath):
    tree = ET.ElementTree(file=AnotPath)
    root = tree.getroot()
    fileName = root.find('filename')
    Size = root.find('size')
    w = int(Size.find('width').text)
    h = int(Size.find('height').text)
    # print('File:{} Width:{} Height:{}'.format(fileName.text,w,h))
    ObjectSet = root.findall('object')
    # ObjBndBoxSet = {}
    for Object in ObjectSet:
        ObjName = Object.find('name').text
        BndBox = Object.find('bndbox')
        x1 = int(BndBox.find('xmin').text)
        y1 = int(BndBox.find('ymin').text)
        x2 = int(BndBox.find('xmax').text)
        y2 = int(BndBox.find('ymax').text)
        bw = x2 - x1
        bh = y2 - y1
        bw = bw if bw > 0 else -bw
        bh = bh if bh > 0 else -bh
        r = int(bw / bh + 0.5)
        r = r if r >= 1 else int(bh / bw + 0.5)
        tarea = bw * bh
        if ObjName == 'hat':
            if r in box_wh_h:
                box_wh_h[r] = box_wh_h[r] + 1
            else:
                box_wh_h[r] = 1
            if tarea < 32 * 32:
                result['helmet_s'] = result['helmet_s'] + 1
                area['helmet_s'] = area['helmet_s'] + tarea
            elif tarea > 96 * 96:
                result['helmet_l'] = result['helmet_l'] + 1
                area['helmet_l'] = area['helmet_l'] + tarea
            else:
                result['helmet_m'] = result['helmet_m'] + 1
                area['helmet_m'] = area['helmet_m'] + tarea
        elif ObjName == 'person':
            if r in box_wh_p:
                box_wh_p[r] = box_wh_p[r] + 1
            else:
                box_wh_p[r] = 1
            if tarea < 32 * 32:
                result['person_s'] = result['person_s'] + 1
                area['person_s'] = area['person_s'] + tarea
            elif tarea > 96 * 96:
                result['person_l'] = result['person_l'] + 1
                area['person_l'] = area['person_l'] + tarea
            else:
                result['person_m'] = result['person_m'] + 1
                area['person_m'] = area['person_m'] + tarea
        # print('Object: {} xmin: {} ymin:{} xmax:{} ymax:{}'.format(ObjName,x1,y1,x2,y2))


os.chdir('D:\BaiduNetdiskDownload\VOC2028\VOC2028\Annotations')
files = os.listdir('.')
total = len(files)
for i in trange(total):
    file = files[i]
    path = os.path.join('.', file)
    GetAnnotBoxLoc(path)
result['person_total'] = result['person_s'] + result['person_m'] + result['person_l']
result['helmet_total'] = result['helmet_s'] + result['helmet_m'] + result['helmet_l']
area['person_total'] = area['person_s'] + area['person_m'] + area['person_l']
area['person_avg_s'] = area['person_s'] / result['person_s']
area['person_avg_m'] = area['person_m'] / result['person_m']
area['person_avg_l'] = area['person_l'] / result['person_l']
area['person_avg'] = area['person_total'] / result['person_total']

area['helmet_total'] = area['helmet_s'] + area['helmet_m'] + area['helmet_l']
area['helmet_avg_s'] = area['helmet_s'] / result['helmet_s']
area['helmet_avg_m'] = area['helmet_m'] / result['helmet_m']
area['helmet_avg_l'] = area['helmet_l'] / result['helmet_l']
area['helmet_avg'] = area['helmet_total'] / result['helmet_total']

area['total_avg_s'] = (area['helmet_s']+area['person_s'])/(result['helmet_s']+result['person_s'])
area['total_avg_m'] = (area['helmet_m']+area['person_m'])/(result['helmet_m']+result['person_m'])
area['total_avg_l'] = (area['helmet_l']+area['person_l'])/(result['helmet_l']+result['person_l'])
area['total_avg'] = (area['helmet_total']+area['person_total'])/(result['helmet_total']+result['person_total'])

area['person_avg_s_len'] = sqrt(area['person_avg_s'])
area['person_avg_m_len'] = sqrt(area['person_avg_m']) 
area['person_avg_l_len'] = sqrt(area['person_avg_l'])
area['helmet_avg_s_len'] = sqrt(area['helmet_avg_s'])
area['helmet_avg_m_len'] = sqrt(area['helmet_avg_m'])
area['helmet_avg_l_len'] = sqrt(area['helmet_avg_l'])
area['total_avg_s_len'] = sqrt(area['total_avg_s'])
area['total_avg_m_len'] = sqrt(area['total_avg_m'])
area['total_avg_l_len'] = sqrt(area['total_avg_l'])
area['person_avg_len'] = sqrt(area['person_avg'])
area['helmet_avg_len'] = sqrt(area['helmet_avg'])
area['total_avg_len'] = sqrt(area['total_avg'])


print(result)
print(area)
print(box_wh_h)
print(box_wh_p)
