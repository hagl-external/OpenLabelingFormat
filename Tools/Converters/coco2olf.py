import json
import uuid
import mimetypes
import datetime
import pandas as pd

with open ('instances_val2014.json', 'r') as f:
    coco = json.load(f)

def md5Checksum(filePath, url = None):
    import requests
    import hashlib
    if url == None:
        with open(filePath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()
    else:
        r = requests.get(url, stream = True)
        m = hashlib.md5()
        for line in r.iter_lines():
            m.update(line)
        return m.hexdigest()

def coco_mediaInfo(coco_images):
    olf_mediaInfo = []
    for coco_image in coco_images:
        olf_mediaInfo.append({
            "name": coco_image["file_name"],
            "url": coco_image["coco_url"],
            "type": mimetypes.guess_type(coco_image["file_name"])[0],
            "width": coco_image["width"],
            "height": coco_image["height"],
            #"hash": {
            #    "value": md5Checksum(filePath = "", url = coco_image["coco_url"]),
            #    "method": "md5"
            #}
        })
    return olf_mediaInfo

def coco_objectInfo(coco_annotations, coco_categories, coco_images):
    olf_objectInfo = []
    df_coco_categories = pd.DataFrame(coco_categories).reset_index(drop = True)
    df_coco_images = pd.DataFrame(coco_images).reset_index(drop = True)
    i = 0
    for coco_annotation in coco_annotations:
        i += 1
        if i % 1000 == 0:
            print(i)
        #    break
        obj = {
            "uuid": str(uuid.uuid4()),
            "nameOfMedia": df_coco_images[df_coco_images["id"] == coco_annotation["image_id"]]["file_name"].to_string(index = False).lstrip(),
            "class": df_coco_categories[df_coco_categories["id"] == coco_annotation["category_id"]]["name"].to_string(index = False).lstrip(),
            "attributes": [],
            "shapeGroups": [{
                "uuid": str(uuid.uuid4()),
                "instructions": "Object shape is represented by a single 2d bounding box in image space.",
                "validity": {
                    "at": df_coco_images[df_coco_images["id"] == coco_annotation["image_id"]].index.tolist()[0],
                    "unit": "frames"
                },
                "shapes": [{
                    "box2D": {
                        "topLeft": {
                            "x": coco_annotation["bbox"][0],
                            "y": coco_annotation["bbox"][1],
                            "unit": "px"
                        },
                        "bottomRight": {
                            "x": coco_annotation["bbox"][0] + coco_annotation["bbox"][2],
                            "y": coco_annotation["bbox"][1] + coco_annotation["bbox"][3],
                            "unit": "px"
                        },
                        "rotation": {
                            "angle": 0.0,
                            "unit": "deg"
                        }
                    }
                }]
            }],
            "relations": []
        }
        olf_objectInfo.append(obj)
    return olf_objectInfo

versionInfo = {
    "name": "OpenLabelFormat",
    "schema": "0.4",
    "labelFile": "0.1"
}

mediaInfo = {
    "references": coco_mediaInfo(coco["images"])
}

projectInfo = {
    "intervals": list(range(0, len(mediaInfo["references"]))),
    "unit": "frames"
}

odometryInfo = {}

calibrationInfo = {}

positionInfo = {}

metaInfo = []

objectInfo = coco_objectInfo(coco["annotations"], coco["categories"], coco["images"])

olf = {
    "versionInfo": versionInfo,
    "projectInfo": projectInfo,
    "odometryInfo": odometryInfo,
    "calibrationInfo": calibrationInfo,
    "positionInfo": positionInfo,
    "mediaInfo": mediaInfo,
    "metaInfo": metaInfo,
    "objectInfo": objectInfo
}

json_out = json.dumps(olf, indent = None)

with open("instances_val2014_olf.json", "w") as f:
    f.write(json_out)
