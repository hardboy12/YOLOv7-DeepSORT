import os
from glob import glob
import xml.etree.ElementTree as ET
xml_dir = r'E:\2023-2025-projects\Yak dataset partitioning\datasets\Annotations'####xml文件夹
output_txt_dir = r'E:\2023-2025-projects\Yak dataset partitioning\datasets\yolo-data\txt'####输出yolo所对应格式的文件夹
# ###进行归一化操作

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def load_xml():####这里是你自己的分类
    # classes = ['bruise','crack','blackspot', 'rot']
    classes = ['maoniu']

    xml_list = glob(os.path.join(xml_dir, '*.xml'))
    # print(len(xml_list), xml_list)
    count_pictures = {}
    count_detection = {}
    count = 0
    class_num0 = 0
    class_num1 = 0
    class_num2 = 0
    class_num3 = 0
    class_num4 = 0
    class_num5 = 0
    for file in xml_list:
        count = count + 1
        imgName = file.split('\\')[-1][:-4]  # 文件名，不包含后缀
        imglabel = os.path.join(output_txt_dir, imgName + '.txt')  # 创建TXT（文件夹路径加文件名加.TXT）
        # print(imglabel)
        out_file = open(imglabel,'w', encoding='UTF-8')  # 以写入的方式打开TXT
        tree = ET.parse(file)
        root = tree.getroot()
        for child in root:
            if child.tag == 'size':
                w = child[0].text
                h = child[1].text
            if child.tag == 'object':
                x_min = child[4][0].text
                y_min = child[4][1].text
                x_max = child[4][2].text
                y_max = child[4][3].text
                box = convert((int(w), int(h)), (int(x_min), int(x_max), int(y_min), int(y_max)))
                label = child[0].text
                if label in classes:##按照上面的顺序填写标签，如果超过这些自己增加复制就行了
                    if label == 'maoniu':
                        label = '0'
                        class_num0 += 1
                        out_file.write(str(label) + ' ' + ' '.join([str(round(a, 6)) for a in box]) + '\n')  # 把内容写入TXT中
                    # if label == 'crack':
                    #     label = '1'
                    #     class_num1 += 1
                    #     out_file.write(str(label) + ' ' + ' '.join([str(round(a, 6)) for a in box]) + '\n')
                    #
                    # if label == 'blackspot':
                    #     label = '2'
                    #     class_num2 += 1
                    #     out_file.write(str(label) + ' ' + ' '.join([str(round(a, 6)) for a in box]) + '\n')
                    # if label == 'rot':
                    #     label = '3'
                    #     class_num3 += 1
                    #     out_file.write(str(label) + ' ' + ' '.join([str(round(a, 6)) for a in box]) + '\n')
                    # print('ALL:', count, " bruise:", class_num0, "  crack:", class_num1, "  blackspot:", class_num2,
                    #       " rot:", class_num3)
    print('ALL:', count, "maoniu:", class_num0)
    return len(xml_list), classes, count_pictures, count_detection  # return 用在函数内部表示当调用该函数时，

if __name__ == '__main__':
    classes = load_xml()
    print(classes)