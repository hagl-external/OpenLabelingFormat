import os
import json
import glob
import pandas as pd
from torch.utils.data import Dataset
from skimage import io

class OLFDetectionDataset(Dataset):
    """Classic for reading datasets from OpenLabelFormat (OLF)"""

    def __init__(self, olf_file, root_dir = None, transform = None):
        """
        :param olf_file: Path to json file that contains annotations in OLF format.
        :param root_dir: Optional directory containing files referenced in 'olf_file'. If None,
        URLs from within 'olf_file' are used.
        :param transform: Optional transforms to be applied on a sample.
        """
        with open(olf_file, "r", encoding = "utf-8-sig") as f_olf:
            self.olf = json.loads(f_olf.read())
        self.root_dir = root_dir
        self.transform = transform
        self.mediaInfo = self.prepareMediaInfo()
        self.objectInfo = self.prepareObjectInfo()
        del self.olf

    def prepareMediaInfo(self):
        print("OLFDetectionDataset: Preparing media...")
        df_mediaInfo = pd.DataFrame(self.olf["mediaInfo"]["references"])
        df_mediaInfo = df_mediaInfo[df_mediaInfo["type"].apply(lambda x: x.split("/")[0]) == "image"]
        if self.root_dir is not None:
            suffixes = df_mediaInfo["name"].apply(lambda x: "." + x.split(".")[-1]).unique().tolist()
            root_dir_urls = []
            for suffix in suffixes:
                root_dir_urls.extend(glob.glob(self.root_dir + "/**/*" + suffix, recursive = True))
            root_dir_urls = {root_dir_url.split(os.sep)[-1] : root_dir_url for root_dir_url in root_dir_urls}
            df_mediaInfo["url"] = df_mediaInfo["name"].apply(lambda x: root_dir_urls.get(x, None))
            df_mediaInfo = df_mediaInfo.dropna(subset = ["url"])
        df_mediaInfo = df_mediaInfo.sort_values(by = ["name"])
        return df_mediaInfo.reset_index(drop = True)

    def getBox2DMax(self, shapeGroups):
        shapes = [shapeGroup["shapes"] for shapeGroup in shapeGroups]
        shapes = [shape for _ in shapes for shape in _ if "box2D" in shape]
        x0 = min([shape["box2D"]["topLeft"]["x"] for shape in shapes])
        y0 = min([shape["box2D"]["topLeft"]["y"] for shape in shapes])
        x1 = max([shape["box2D"]["bottomRight"]["x"] for shape in shapes])
        y1 = max([shape["box2D"]["bottomRight"]["y"] for shape in shapes])
        return [x0, y0, x1, y1]

    def prepareObjectInfo(self):
        print("OLFDetectionDataset: Preparing annotations...")
        df_objectInfo = pd.DataFrame(self.olf["objectInfo"])
        df_objectInfo = df_objectInfo[df_objectInfo["nameOfMedia"].isin(self.mediaInfo["name"])].reset_index(drop = True)
        df_objectInfo = df_objectInfo[df_objectInfo["shapeGroups"].astype("str").str.contains("box2D")].reset_index(drop = True)
        self.mediaInfo = self.mediaInfo[self.mediaInfo["name"].isin(df_objectInfo["nameOfMedia"])].reset_index(drop = True)
        df_objectInfo["box2D_max"] = df_objectInfo["shapeGroups"].apply(self.getBox2DMax)
        df_objectInfo = pd.concat([df_objectInfo.groupby(["nameOfMedia"])["box2D_max"]
                                  .apply(list), df_objectInfo.groupby(["nameOfMedia"])["class"]
                                  .apply(list)], axis = 1)
        df_objectInfo = df_objectInfo.sort_values(by = ["nameOfMedia"])
        return df_objectInfo.reset_index(drop = False)

    def __len__(self):
        return len(self.mediaInfo)

    def __getitem__(self, idx):
        media = self.mediaInfo.iloc[idx, :]
        annotations = self.objectInfo.iloc[idx, :]
        assert media["name"] == annotations["nameOfMedia"]
        assert len(annotations["box2D_max"]) == len(annotations["class"])
        img = io.imread(media["url"])
        if self.transform is not None:
            img = self.transform(img)
        return {"img": img,
                "box": annotations["box2D_max"],
                "cls": annotations["class"]
                }

#olf_dataset = OLFDetectionDataset("../../../Documents/instances_val2014_olf.json", "/home/soehch2/Docker/SharedFolder/CurrentDatasets/val2014")
