import pandas as pd
import random
import geopandas as gpd
from shapely.geometry import Point, Polygon
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 函数1：用于读取Excel文件
def read_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        logging.info(f"Excel file {file_path} read successfully.")
        return df
    except Exception as e:
        logging.error(f"Error reading Excel file {file_path}: {e}")
        raise


# 函数2：根据用户提供不同屏障类型数量随机筛选数据
def filter_data(df, criteria, random_seed=None):
    filtered_data = pd.DataFrame(columns=df.columns)
    for dataset, types in criteria.items():
        for type_, count in types.items():
            subset = df[(df['Dataset'] == dataset) & (df['Type'] == type_)]
            if len(subset) < count:
                logging.warning(f"There are not enough {type_} in {dataset}.")
            sample = subset.sample(min(len(subset), count), random_state=random_seed)
            filtered_data = pd.concat([filtered_data, sample])
    return filtered_data


# 函数3：保存筛选后的数据重新编号并导出到新的Excel文件
def save_to_excel(data, file_path):
    try:
        data['ID'] = range(1, len(data) + 1)
        data = data[['ID', 'TID', 'Type', 'Lat', 'Lon', 'Country', 'Dataset']]
        data.to_excel(file_path, index=False)
        logging.info(f"Excel file {file_path} created successfully.")
    except Exception as e:
        logging.error(f"Error saving Excel file {file_path}: {e}")
        raise


# 函数4：将筛选的坐标点转换为点矢量文件
def save_to_shapefile(data, file_path):
    try:
        geometry = [Point(xy) for xy in zip(data['Lon'], data['Lat'])]
        gdf_points = gpd.GeoDataFrame(data, geometry=geometry, crs='EPSG:4326')
        gdf_points.to_file(file_path)
        logging.info(f"Points shapefile {file_path} created successfully.")
    except Exception as e:
        logging.error(f"Error saving shapefile {file_path}: {e}")
        raise


# 函数5：根据每个点生成一个矩形矢量边界，并记录 ID
def create_and_save_rectangles(gdf_points, file_path, size=4000):
    try:
        rectangles = []
        ids = []  # 用于记录矩形的 ID
        for index, row in gdf_points.iterrows():
            point = row.geometry
            minx, miny, maxx, maxy = point.buffer(size).bounds
            rectangle = Polygon([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)])
            rectangles.append(rectangle)
            ids.append(row['ID'])  # 将当前点的 ID 添加到列表中
        gdf_rectangles = gpd.GeoDataFrame(geometry=rectangles, crs='EPSG:3857')
        gdf_rectangles['ID'] = ids  # 将记录的 ID 添加为新的列
        gdf_rectangles.to_file(file_path)
        logging.info(f"Fishnet shapefile {file_path} created successfully.")
    except Exception as e:
        logging.error(f"Error creating fishnet shapefile {file_path}: {e}")
        raise


# 新增的函数：根据需求筛选数据并统计
def filter_and_sample(input_file_1, input_file_2, criteria):
    try:
        df1 = input_file_1
        df2 = input_file_2

        # 集合 A: 从 input_file_2 中筛选出除 input_file_1 外的部分
        set_A = df2[~df2['TID'].isin(df1['TID'])]

        # 集合 B: 从 input_file_1 中筛选出 check_results 为 “有效图片”的部分
        set_B = df1[df1['check_results'] == '有效图片']

        # 统计集合 B 中不同 Dataset 的不同 Type 的数量
        counts_B = set_B.groupby(['Dataset', 'Type']).size().unstack(fill_value=0)

        # 计算集合 C: 需要补充的数量
        criteria_df = pd.DataFrame(criteria).T
        counts_C = criteria_df.sub(counts_B, fill_value=0).clip(lower=0).fillna(0).astype(int)

        # 从集合 A 中随机抽取集合 C 所需数量的坐标点
        filtered_data = pd.DataFrame(columns=set_A.columns)
        for dataset, types in counts_C.iterrows():
            for type_, count in types.items():
                subset = set_A[(set_A['Dataset'] == dataset) & (set_A['Type'] == type_)]
                if len(subset) < count:
                    logging.warning(f"There are not enough {type_} in {dataset} in set_A.")
                sample = subset.sample(min(len(subset), count), random_state=42)
                filtered_data = pd.concat([filtered_data, sample])

        return filtered_data
    except Exception as e:
        logging.error(f"Error in filter_and_sample function: {e}")
        raise


# 主函数
def main(input_file_1, input_file_2, output_file, criteria, rectangle_size=4000):
    try:
        # 过滤纬度超过 52° 的屏障
        df_2 = read_excel(input_file_2)
        df_2 = df_2[df_2['Lat'] <= 52]

        # 若未输入检查结果则直接按预定数量随机筛选坐标点；若输入检查结果则补充坐标点
        if input_file_1.strip():  # 如果 input_file_1 非空
            df_1 = read_excel(input_file_1)
            # 使用 filter_and_sample 函数补充坐标点
            filtered_data = filter_and_sample(df_1, df_2, criteria)
        else:  # 如果 input_file_1 为空
            # 使用 filter_data 函数随机筛选
            filtered_data = filter_data(df_2, criteria, random_seed=325)

        # 保存结果到新的Excel文件
        save_to_excel(filtered_data, output_file)

        # 将筛选的坐标点转换为点矢量文件并保存为Shapefile格式
        save_to_shapefile(filtered_data, output_file.replace('.xlsx', '_points.shp'))

        # 将筛选的坐标点转换到投影坐标系（EPSG:3857）
        geometry = [Point(xy) for xy in zip(filtered_data['Lon'], filtered_data['Lat'])]
        gdf_points = gpd.GeoDataFrame(filtered_data, geometry=geometry, crs='EPSG:4326')
        gdf_points = gdf_points.to_crs('EPSG:3857')

        # 根据每个点生成一个矩形边界，并将生成的矩形保存为Shapefile格式
        create_and_save_rectangles(gdf_points, output_file.replace('.xlsx', '_fishnet.shp'), size=rectangle_size)

    except Exception as e:
        logging.error(f"An error occurred in the main process: {e}")
        raise


if __name__ == "__main__":
    #input_file_1 = " "
    input_file_1 = r"F:\river_barrier\location_excel_with_results_sum.xlsx"
    input_file_2 = r"F:\river_barrier\location_input.xlsx"
    output_file = r"F:\river_barrier\location_excel.xlsx"
    criteria = {
        'GROD': {'Dams': 200, 'Weirs': 100, 'Locks': 100, 'Partial Dams': 200},
        'MRBD': {'Dams': 200, 'Weirs': 200, 'Locks': 300},
        'AMBER': {'Dams': 200, 'Weirs': 300, 'Locks': 200}
    }
    main(input_file_1, input_file_2, output_file, criteria, rectangle_size=2000)
