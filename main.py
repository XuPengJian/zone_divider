import os
from shapely.geometry import Polygon, Point

# 参数输入部分
project_path = 'example/4'
# txt_path = 'example/5.txt'
# cad_dat_path = 'example/001.DAT'
output_path = 'example/output'


def find_files(directory, suffix='.txt'):
    # 存储所有.txt文件的路径
    found_files = []
    # os.walk()遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名是否为suffix
            if file.endswith(suffix):
                # 将文件的完整路径添加到列表中
                found_files.append(os.path.join(root, file).replace('\\', '/'))
    return found_files


# 单个文件生成txt的代码
def generate_txt(dat_path, txt_path, output_txt_path):
    # 打开dat文件，读取里面的点信息
    poly_line = []
    with open(dat_path, 'r') as f:
        for line in f:
            dat_data = line.strip().split(',')
            longitude = float(dat_data[2])
            latitude = float(dat_data[3])
            poly_line.append([longitude, latitude])
    # print(poly_line)

    # 确保多边形是封闭的，即起点和终点相同
    if poly_line[0] != poly_line[-1]:
        poly_line.append(poly_line[0])

    # 创建多边形
    polygon = Polygon(poly_line)

    # 打开原始txt文件
    with open(txt_path, 'r') as f:
        data_list = f.readlines()

    # print(data_list)
    # 获取表头
    head = data_list[0]
    # 先新建output.txt抄一下表头
    with open(output_txt_path, 'w') as f:
        f.write(head)

    # 逐行读取剩下的数据
    for i in range(1, len(data_list)):
        txt_data = data_list[i].split('\t')
        longitude = float(txt_data[1])
        latitude = float(txt_data[2])
        point = Point(longitude, latitude)

        # 判断点是否在多边形内部
        is_inside = point.within(polygon)
        if is_inside:
            with open(output_txt_path, 'a') as f:
                f.write(data_list[i])

            print('image_name:', txt_data[0])


# 分地块的文件
dat_files = find_files(project_path, '.DAT')
dat_files.sort()
# 分镜头的文件，一般为5个镜头
txt_files = find_files(project_path, '.txt')
txt_files.sort()

# 先遍历dat文件作为分块依据
for i, each_dat in enumerate(dat_files):
    # 定义新建文件夹的名字
    name_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    output_dir = os.path.join(output_path, name_list[i])
    os.makedirs(output_dir, exist_ok=True)
    for j, each_txt in enumerate(txt_files):
        output_txt = os.path.join(output_dir, f'{j + 1}.txt').replace('\\', '/')
        print(output_txt)
        generate_txt(each_dat, each_txt, output_txt)
