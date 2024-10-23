# 代码说明：批量裁剪图片至统一尺寸
import os
from collections import defaultdict
from osgeo import gdal

# 设置输入和输出文件夹路径
input_tiff_folder = r"F:\river_barrier\output results\geotiff"  # 输入存储需要裁剪的geotiff图片文件夹
output_tiff_folder = r"F:\river_barrier\output results\geotiff_clip" # 输出存储裁剪后的geotiff图片文件夹

# 设置图片大小（单位pixel）
min_width = 3359
min_height = 3359

# 创建输出文件夹
if not os.path.exists(output_tiff_folder):
    os.makedirs(output_tiff_folder)

# 遍历所有tiff文件进行裁剪
for tiff_file in os.listdir(input_tiff_folder):
    if tiff_file.endswith(".tif") or tiff_file.endswith(".tiff"):
        tiff_path = os.path.join(input_tiff_folder, tiff_file)
        # 读取tiff图像
        dataset = gdal.Open(tiff_path)
        if dataset is None:
            print("文件 {} 无法打开或不是有效的图像文件。".format(tiff_file))
            continue

        # 获取地理空间信息
        geotransform = dataset.GetGeoTransform()
        projection = dataset.GetProjection()

        # 计算裁剪框的大小
        left = (dataset.RasterXSize - min_width) // 2
        top = (dataset.RasterYSize - min_height) // 2
        right = left + min_width
        bottom = top + min_height

        # 读取图像数据
        data = dataset.ReadAsArray(left, top, min_width, min_height)

        # 创建输出文件
        output_path = os.path.join(output_tiff_folder, tiff_file)
        driver = gdal.GetDriverByName("GTiff")
        out_dataset = driver.Create(output_path, min_width, min_height, dataset.RasterCount, dataset.GetRasterBand(1).DataType)
        out_dataset.SetProjection(projection)
        out_dataset.SetGeoTransform((geotransform[0] + left * geotransform[1], geotransform[1], 0, geotransform[3] + top * geotransform[5], 0, geotransform[5]))
        for i in range(1, dataset.RasterCount + 1):
            out_band = out_dataset.GetRasterBand(i)
            out_band.WriteArray(data[i - 1])
            out_band.FlushCache()

        # 关闭数据集
        dataset = None
        out_dataset = None

print("数据处理完成-----------------------------")