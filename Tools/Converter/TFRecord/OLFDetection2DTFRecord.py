'''
MIT License

Copyright (c) 2020 HELLA Aglaia Mobile Vision GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import io
import numpy as np
import pandas as pd
import tensorflow as tf
from OLFDetection2D import OLFDetection2D
from PIL import Image

# The following functions can be used to convert a value to a type compatible
# with tf.Example.
def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if not isinstance(value, list):
        if isinstance(value, type(tf.constant(0))):
            value = value.numpy()  # BytesList won't unpack a string from an EagerTensor.
        value = [value]
    else:
        value = [v.numpy() if isinstance(value, type(tf.constant(0))) else v for v in value]
    return tf.train.Feature(bytes_list = tf.train.BytesList(value = value))

def _float_feature(value):
    """Returns a float_list from a float / double."""
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(float_list = tf.train.FloatList(value = value))

def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(int64_list = tf.train.Int64List(value = value))

class OLFDetection2DTFRecord(OLFDetection2D):

    def __init__(self, olf_file, media_types = ["image/png", "image/jpeg"], root_dir = None):
        """
        :param olf_file: Path to json file that contains annotations in OLF format.
        :param media_types: List of media mime types that should be selected.
        :param root_dir: Optional directory containing files referenced in 'olf_file'. If None,
        URLs from within 'olf_file' are used.
        """
        super(OLFDetection2DTFRecord, self).__init__(olf_file, media_types, root_dir)
        classInfo = pd.DataFrame(sorted(np.unique(np.hstack(self.objectInfo["class"])).tolist()), columns = ["class"]).reset_index(drop = True)
        self.classInfo = dict(zip(classInfo["class"].to_list(), classInfo.index.to_list()))

    def __len__(self):
        return len(self.mediaInfo)

    def __getitem__(self, idx):
        media = self.mediaInfo.iloc[idx, :]
        annotations = self.objectInfo.iloc[idx, :]
        assert media["name"] == annotations["nameOfMedia"]
        assert len(annotations["box2D_max"]) == len(annotations["class"])
        return {"img": media,
                "box": annotations["box2D_max"],
                "cls": annotations["class"]
                }

    def toTFRecord(self, out_path):
        """
        :param out_path: Path to output tfrecord file.
        """
        print("OLFDetection2DTFRecord: Writing tfrecord...")
        with tf.io.TFRecordWriter(out_path) as writer:
            for i in range(len(self)):
                example = self.create_tf_example(self[i])
                writer.write(example)

    def create_tf_example(self, example):
        with tf.io.gfile.GFile(example["img"]["url"], 'rb') as fid:
            encoded_img = fid.read() # Encoded image bytes
        encoded_img_io = io.BytesIO(encoded_img)
        image = Image.open(encoded_img_io)
        width, height = image.size # Image width and height
        filename = example["img"]["name"].encode("utf-8")  # Filename of the image. Empty if image is not from file
        image_format = example["img"]["type"].split("/")[-1].encode("utf-8") # b'jpeg' or b'png'

        xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
        xmaxs = [] # List of normalized right x coordinates in bounding box # (1 per box)
        ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
        ymaxs = [] # List of normalized bottom y coordinates in bounding box # (1 per box)
        classes_text = [] # List of string class name of bounding box (1 per box)
        classes = [] # List of integer class id of bounding box (1 per box)

        for i in range(len(example["box"])):
            xmins.append(example["box"][i][0] / width)
            ymins.append(example["box"][i][1] / height)
            xmaxs.append(example["box"][i][2] / width)
            ymaxs.append(example["box"][i][3] / height)
            classes_text.append(example["cls"][i].encode("utf-8"))
            classes.append(self.classInfo[example["cls"][i]])

        tf_example = tf.train.Example(features = tf.train.Features(feature = {
            'image/height': _int64_feature(height),
            'image/width': _int64_feature(width),
            'image/filename': _bytes_feature(filename),
            'image/source_id': _bytes_feature(filename),
            'image/encoded': _bytes_feature(encoded_img),
            'image/format': _bytes_feature(image_format),
            'image/object/bbox/xmin': _float_feature(xmins),
            'image/object/bbox/xmax': _float_feature(xmaxs),
            'image/object/bbox/ymin': _float_feature(ymins),
            'image/object/bbox/ymax': _float_feature(ymaxs),
            'image/object/class/text': _bytes_feature(classes_text),
            'image/object/class/label': _int64_feature(classes),
        }))
        return tf_example.SerializeToString()
