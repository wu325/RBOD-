#代码说明：批量geotiff格式图片转换为jpg格式图片
import os
import time
from osgeo import gdal
import numpy as np
from PIL import Image

def geotiff_to_jpg(input_geotiff, output_folder):
    # 打开 GeoTIFF 文件
    dataset = gdal.Open(input_geotiff)

    # 获取地图的宽度和高度
    width = dataset.RasterXSize
    height = dataset.RasterYSize

    # 读取地图数据（三个波段）
    band1 = dataset.GetRasterBand(1)
    band2 = dataset.GetRasterBand(2)
    band3 = dataset.GetRasterBand(3)
    data1 = band1.ReadAsArray()
    data2 = band2.ReadAsArray()
    data3 = band3.ReadAsArray()

    # 将三个波段数据合并为 RGB 图像
    img_data = np.dstack((data1, data2, data3))

    # 将数据裁剪到 0 到 255 之间，并转换为无符号 8 位整数
    img_data = np.clip(img_data, 0, 255).astype(np.uint8)

    # 创建 PIL 图片对象
    img = Image.fromarray(img_data)

    # 获取输入 GeoTIFF 文件的文件名（不包括扩展名）
    filename = os.path.splitext(os.path.basename(input_geotiff))[0]

    # 构建输出 JPEG 文件的路径
    output_jpg = os.path.join(output_folder, f"{filename}.jpg")

    # 保存为 JPEG 格式的图片
    img.save(output_jpg)

    # 关闭数据集
    dataset = None

if __name__ == "__main__":
    input_folder = r"F:\river_barrier\output results\geotiff_clip"  # 输入geotiff文件的文件夹路径
    output_folder = r"F:\river_barrier\output results\jpg"  # 输出 JPEG 文件的文件夹路径

    # 开始计时
    start_time = time.time()

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".tif") or filename.endswith(".tiff"):  # 确保是 GeoTIFF 文件
            input_geotiff = os.path.join(input_folder, filename)
            geotiff_to_jpg(input_geotiff, output_folder)

    # 计算总运行时间
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total elapsed time: {elapsed_time:.2f} seconds")
