from ultralytics.data.split_dota import split_test, split_trainval

# split train, val, and test set, with labels.
split_trainval(
    data_root="G:/ultralytics-main/dataset/YRBD/",
    save_dir="G:/ultralytics-main/dataset/YRBD_ms/",
    rates=[0.4, 1.0, 2],
    gap=512,
)