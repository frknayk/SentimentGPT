import os
import shutil
from pathlib import Path
import json

def get_project_path():
    return str(Path(os.path.abspath(os.curdir)))

def get_model_path():
    project_path = get_project_path()
    return str(Path(project_path,"resources"))

def get_data_path(data_file:str):
    """data_file: must be placed under path-to-project/data/ folder

    Parameters
    ----------
    data_file : name of file
        only file name, not absolute path. (e.g: data.json)

    Returns
    -------
    str
        absolute path of file
    """
    return merge_paths([get_project_path(),"data",data_file])

def merge_paths(path_list):
    """Merge list of paths by automatically detecting OS suffix

    Parameters
    ----------
    path_list : list
        List of strings(path)

    Returns
    -------
    str
        merged path
    """
    path_merged = Path(path_list[0])
    for idx_path in range(1,len(path_list)):
        path_merged = path_merged.joinpath(path_list[idx_path])
    return str(path_merged)

def copy_configs_to_model():
    """Copy config files from config/ to resources/ folder.
    """
    project_path = get_project_path()
    # Use pathlib for cross-platform compatibility
    config_files = [
        str(Path(project_path,"config","config.json")),
        str(Path(project_path,"config","tokenizer_config.json")),
        str(Path(project_path,"config","tokenizer.json"))]
    # Copy config/ files to resources/ folder temporary 
    model_path = str(Path(project_path,"resources"))
    for cfg_file in config_files:
        shutil.copy(cfg_file, model_path)

def remove_configs_from_model():
    """Remove everything except pytorch_model.bin file in resources/ folder
    """
    project_path = get_project_path()
    model_path = str(Path(project_path,"resources"))
    resources_files = os.listdir(model_path)
    for rsc_file in resources_files:
        if rsc_file == "pytorch_model.bin":
            continue
        os.remove(str(Path(model_path,rsc_file)))

def read_data_file(file_name:str):
    data_path = get_data_path(file_name)
    with open(data_path) as json_file:
        conversation = json.load(json_file)
        json_file.close()

    return conversation
