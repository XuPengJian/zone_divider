import os
import shutil
from tqdm import tqdm

project_path = r'D:\航测数据\14-zhaoqing\5号区域'

head_name = 'ZQ5'
shot_name = ['A', 'B', 'C', 'D', 'E']
for i in range(5):
    shot_dir = os.path.join(project_path, str(i + 1))
    children_dirs = os.listdir(shot_dir)
    shot_images_path_list = []
    for each_child in children_dirs:
        children_dir = os.path.join(shot_dir, each_child)
        # 遍历目录
        for root, dirs, files in os.walk(children_dir):
            for file in files:
                # 检查文件扩展名是否在支持的列表中
                if any(file.lower().endswith(ext) for ext in ['jpg', 'JPG']):
                    # 打印文件的完整路径
                    shot_images_path_list.append(os.path.join(root, file))

    for j, each_image_path in enumerate(tqdm(shot_images_path_list)):
        destination_path = shot_dir + '/' + head_name + shot_name[i] + f'{j:05d}.JPG'
        # 将文件移动到指定路径
        shutil.move(each_image_path, destination_path)