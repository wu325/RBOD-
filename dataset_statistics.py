import os
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

def load_annotations(xml_folder):
    """
    Loads all .xml annotation files from the specified folder and parses the object information in each file.
    Parameters:
    xml_folder (str): The path to the folder where the .xml file is stored.
    output:
    dict: A dictionary with the key being the filename and the value being a list of information about the objects in each file.
    """
    annotations = {}
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith('.xml'):
            tree = ET.parse(os.path.join(xml_folder, xml_file))
            root = tree.getroot()
            objects = []
            for obj in root.findall('object'):
                name = obj.find('name').text
                robndbox = obj.find('robndbox')
                cx = float(robndbox.find('cx').text)
                cy = float(robndbox.find('cy').text)
                w = float(robndbox.find('w').text)
                h = float(robndbox.find('h').text)
                area = w * h
                objects.append((name, area, w, h, cx, cy))
            annotations[xml_file] = objects
    return annotations

def load_metadata(metadata_file):
    """
    Load image coordinate position information from Excel file.
    Parameters:
    metadata_file (str): Path to the Excel file where the metadata is stored.
    output:
    DataFrame: A data frame containing the image ID and its corresponding information.
    """
    return pd.read_excel(metadata_file)

def plot_category_counts(annotations, metadata):
    """
    Plot the stacked bars for the number of different target detection categories.
    Parameters:
    annotations (dict): Loaded labeled file object information
    metadata (DataFrame): Picture coordinate position information.
    """
    category_counts = {}
    target_categories = ['dam', 'groyne', 'lock', 'sluice', 'weir']

    for xml_file, objects in annotations.items():
        folder = metadata.loc[metadata['ID'] == os.path.splitext(xml_file)[0], 'Folder'].values[0]
        for name, _, _, _, _, _ in objects:
            if name in target_categories:
                category_counts.setdefault((folder, name), 0)
                category_counts[(folder, name)] += 1

    df_counts = pd.DataFrame(category_counts.items(), columns=['Category', 'Count'])
    df_counts[['Folder', 'Name']] = pd.DataFrame(df_counts['Category'].tolist(), index=df_counts.index)

    df_counts = df_counts[df_counts['Name'].isin(target_categories)]
    df_counts = df_counts.pivot_table(index='Name', columns='Folder', values='Count', fill_value=0)

    df_counts = df_counts[['train', 'val', 'test']]
    print(df_counts)

    df_counts.plot(kind='barh', stacked=True)
    plt.ylabel('Object Categories')
    plt.xlabel('Total Count')
    plt.xticks(rotation=0)
    plt.savefig(r'G:\目标检测标注数据集\2024河流屏障目标检测数据集分析\不同目标类别堆叠条形图.eps', format='eps')
    plt.show()

def plot_object_counts_distribution(annotations):
    """
    Plotting a line graph of the distribution of the number of target objects
    Parameters:
    annotations (dict): Loaded labeled file object information.
    """
    object_counts = [len(objects) for objects in annotations.values()]

    max_count = max(object_counts) if object_counts else 0

    count_freq = np.bincount(object_counts)

    plt.plot(range(len(count_freq)), count_freq, marker='o', markersize=2.5, alpha=0.7)
    plt.xlabel('Number of Objects per .xml File')
    plt.ylabel('Count')
    plt.xticks(range(0, max_count + 1, 10))
    plt.xlim(-1, max_count)
    plt.savefig(r'G:\目标检测标注数据集\2024河流屏障目标检测数据集分析\目标数量频率折线图.eps', format='eps')
    plt.show()

def plot_area_frequency(annotations):
    """
    Plot the frequency distribution of the target object's labeled box area.
    Parameters:
    annotations (dict):  information about the loaded annotation file objects.
    """
    areas = [area for objects in annotations.values() for name, area, w, h, cx, cy in objects]

    if areas:
        median_area = np.log10(np.median(areas))
        max_area = np.log10(np.max(areas))
        min_area = np.log10(np.min(areas))
        mean_area = np.log10(np.mean(areas))

        print(f"面积统计信息:\n中位数: {median_area}\n最大值: {max_area}\n最小值: {min_area}\n平均值: {mean_area}")

    log_areas = np.log10(np.array(areas) + 1)

    plt.hist(log_areas, bins=70, alpha=0.7)
    plt.xlabel('Log10(Area)')
    plt.ylabel('Frequency')
    plt.savefig(r'G:\目标检测标注数据集\2024河流屏障目标检测数据集分析\标注框面积频率直方图.eps', format='eps')
    plt.show()

def plot_area_boxplot(annotations):
    """
    Plot box-and-line diagrams of labeled box areas for different target object classes.

    Parameters:
    annotations (dict): Loaded labeled file object information.
    """
    area_dict = {}

    for objects in annotations.values():
        for name, area, w, h, cx, cy in objects:
            if name not in area_dict:
                area_dict[name] = []
            area_dict[name].append(area)

    log_area_dict = {name: np.log10(np.array(areas) + 1) for name, areas in area_dict.items()}

    plt.boxplot(log_area_dict.values(), labels=log_area_dict.keys(), widths=0.3)
    plt.ylabel('Log10(Area)')
    plt.savefig(r'G:\目标检测标注数据集\2024河流屏障目标检测数据集分析\不同类别标注框面积直方图.eps', format='eps')
    plt.show()

def plot_aspect_ratio_diagonal_length(annotations, metadata):
    """
    Plot the frequency histogram of the labeled box aspect ratio and diagonal length of the target object, sub-train/test/val.
    Parameters:
    annotations (dict): Loaded labeled file object information.
    metadata (DataFrame): Picture coordinate position information.
    """
    ratios = []
    diagonal_lengths = []

    for xml_file, objects in annotations.items():
        folder = metadata.loc[metadata['ID'] == os.path.splitext(xml_file)[0], 'Folder'].values[0]
        for _, _, w, h, _, _ in objects:
            aspect_ratio = w / h if h > 0 else 0
            diagonal_length = np.sqrt(w ** 2 + h ** 2)

            log_aspect_ratio = np.log10(aspect_ratio + 1)
            log_diagonal_length = np.log10(diagonal_length + 1)

            ratios.append((folder, log_aspect_ratio))
            diagonal_lengths.append((folder, log_diagonal_length))

    if ratios:
        log_ratios = np.array([ratio[1] for ratio in ratios])
        median_ratios = np.median(log_ratios)
        mean_ratios = np.mean(log_ratios)
        min_ratios = np.min(log_ratios)
        max_ratios = np.max(log_ratios)
        print(
            f"宽高比统计信息：\n中位数: {median_ratios}\n最大值: {mean_ratios}\n最小值: {min_ratios}\n平均值: {max_ratios}")
    if diagonal_lengths:
        log_diagonal_lengths = np.array([length[1] for length in diagonal_lengths])
        median_diagonal_lengths = np.median(log_diagonal_lengths)
        mean_diagonal_lengths = np.mean(log_diagonal_lengths)
        min_diagonal_lengths = np.min(log_diagonal_lengths)
        max_diagonal_lengths = np.max(log_diagonal_lengths)
        print(
            f"对角线长度统计信息：\n中位数: {median_diagonal_lengths}\n最大值: {mean_diagonal_lengths}\n最小值: {min_diagonal_lengths}\n平均值: {max_diagonal_lengths}")

    df_ratios = pd.DataFrame(ratios, columns=['Folder', 'Log Aspect Ratio'])
    df_diagonal_lengths = pd.DataFrame(diagonal_lengths, columns=['Folder', 'Log Diagonal Length'])

    color_map_diagonal = {'train': '#95cdfe', 'val': '#3a63b5', 'test': '#5d97c5'}
    color_map_ratios = {'train': '#dacefe', 'val': '#ad81c1', 'test': '#a398c5'}

    plt.figure(figsize=(10, 6))

    for folder, group in df_ratios.groupby('Folder'):
        plt.hist(group['Log Aspect Ratio'], bins=300, alpha=0.7, color=color_map_ratios[folder],
                 label=f'{folder} - Length-width')

    for folder, group in df_diagonal_lengths.groupby('Folder'):
        plt.hist(group['Log Diagonal Length'], bins=300, alpha=0.7, color=color_map_diagonal[folder],
                 label=f'{folder} - Diagonal')

    plt.xlabel('Diagonal length and length-width ratio of labeled boxes')
    plt.ylabel('Frequency')
    plt.legend()
    plt.savefig(r'G:\目标检测标注数据集\2024河流屏障目标检测数据集分析\宽高比和对角线长度.pdf', format='pdf')
    plt.show()

if __name__ == "__main__":
    xml_folder = r"G:\目标检测标注数据集\2024河流屏障目标检测数据集分析\YRBD-voc格式\labels"
    metadata_file = r"G:\目标检测标注数据集\2024河流屏障目标检测数据集分析\图片坐标位置\图片对应坐标.xlsx"

    annotations = load_annotations(xml_folder)
    metadata = load_metadata(metadata_file)

    plot_category_counts(annotations, metadata)
    plot_object_counts_distribution(annotations)
    plot_area_frequency(annotations)
    plot_area_boxplot(annotations)
    plot_aspect_ratio_diagonal_length(annotations, metadata)
