import os
import json
import glob
import pandas as pd

class OLFDetection2D:
    """Class for reading datasets from OpenLabelFormat (OLF)"""

    def __init__(self, olf_file, media_types = ["image/png", "image/jpeg"], root_dir = None):
        """
        :param olf_file: Path to json file that contains annotations in OLF format.
        :param media_types: List of media mime types that should be selected.
        :param root_dir: Optional directory containing files referenced in 'olf_file'. If None,
        URLs from within 'olf_file' are used.
        """
        with open(olf_file, "r", encoding = "utf-8-sig") as f_olf:
            self.olf = json.loads(f_olf.read())
        self.media_types = media_types
        self.root_dir = root_dir
        self.mediaInfo = self.prepareMediaInfo()
        self.objectInfo = self.prepareObjectInfo()
        del self.olf

    def prepareMediaInfo(self):
        print("OLFDetection2D: Preparing media...")
        df_mediaInfo = pd.DataFrame(self.olf["mediaInfo"]["references"])
        df_mediaInfo = df_mediaInfo[df_mediaInfo["type"].isin(self.media_types)]
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
        print("OLFDetection2D: Preparing annotations...")
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