from OLFDetection2D import OLFDetection2D
from torch.utils.data import Dataset
from skimage import io

class OLFDetection2DDataset(OLFDetection2D, Dataset):

    def __init__(self, olf_file, media_types = ["image/png", "image/jpeg"], root_dir = None, transform = None):
        """
        :param olf_file: Path to json file that contains annotations in OLF format.
        :param media_types: List of media mime types that should be selected.
        :param root_dir: Optional directory containing files referenced in 'olf_file'. If None,
        URLs from within 'olf_file' are used.
        :param transform: Optional transforms to be applied on a sample.
        """
        super(OLFDetection2DDataset, self).__init__(olf_file, media_types, root_dir)
        self.transform = transform

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
