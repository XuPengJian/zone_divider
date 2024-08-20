from shapely.geometry import Polygon, Point

# 参数输入部分
project_path = 'example/4'
# txt_path = 'example/5.txt'
# cad_dat_path = 'example/001.DAT'
output_path = 'example/output.txt'




def generate_txt(cad_dat_path, txt_path, output_txt_path):
    # 打开dat文件，读取里面的点信息
    poly_line = []
    with open(cad_dat_path, 'r') as f:
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
    with open(output_path, 'w') as f:
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
