<img src="https://github.com/hagl-external/OpenLabelingFormat/blob/master/Resources/olf_logo.jpg" width="1200" />

# OLF - Open Labeling Format
## Brief
The Open Labeling Format is a specification aimed at labeling (not only) automotive sensor data like below:
<img src="https://github.com/hagl-external/OpenLabelingFormat/blob/master/Resources/labeling.jpg" width="1200" />

## Details
For a complete description of the OLF schema please read the [white-paper](https://github.com/hagl-external/OpenLabelingFormat/blob/master/Documentation/OLF_WhitePaper.pdf). Please also have a look at the [schema file](https://github.com/hagl-external/OpenLabelingFormat/blob/master/Schemas/schema.olf.json) itself.

## Overview
```bash
.
├── Documentation
│   └── OLF_WhitePaper.pdf                    # White-paper and in-depth description of the format
├── Documents
│   └── example.olf                           # Sample OLF file (dummy)
├── License.md                                # License file
├── OpenLabelingFormat.lxsopt                 # Project file(s) for Liquid Studio
├── OpenLabelingFormat.lxsproj                # Project file(s) for Liquid Studio
├── README.md                                 # This file
├── Resources
│   ├── labeling.jpg                          # Sample screen of labeling process
│   ├── hagl_logo.jpg                         # HELLA Aglaia logo
│   └── olf_logo.jpg                          # OLF logo
├── Schemas
│   └── schema.olf.json                       # Actual OLF specification as JSON schema
└── Tools
    ├── Converter
    │   ├── COCO
    │   │   └── coco2olf.py                   # Converter from MS COCO to OLF
    │   └── TFRecord
    │       └── OLFDetection2DTFRecord.py     # Converter from OLF to TFRecord
    ├── Loader
    │   ├── OLFDetection2D.py                 # Base class for extracting 2D detections from an OLF file
    │   └── PyTorch
    │       └── OLFDetection2DDataset.py      # Detection dataset class for PyTorch based on OLFDetection2D.py
    └── Notebooks
        ├── Demo_OLFDetection_PyTorch.ipynb   # Demo notebook showing how to use OLFDetection2DDataset.py
        └── Demo_OLFDetection_TFRecord.ipynb  # Demo notebook showing how to use OLFDetection2DTFRecord.py
```

## Requirements
The OLF schema has been designed using Liquid Studio 2019 - JSON Editor Edition 17.1.5.9520 offered by [Liquid Technologies](https://www.liquid-technologies.com). It is based on JSON schema draft-07.

Python scripts require the following package versions:

|Package|Version|
|--|--|
|jsonschema|3.1.1|
|object-detection|0.0.3|
|pandas|0.25.1|
|python|3.6.9|
|scikit-image|0.15.0|
|tensorflow|2.0.0|
|torch|1.3.0|

## Quick-Start
To convert detections from [MS COCO](http://images.cocodataset.org/annotations/annotations_trainval2014.zip) into OLF, check-out [this script](https://github.com/hagl-external/OpenLabelingFormat/blob/master/Tools/Converter/COCO/coco2olf.py).

For a demo on how to use an OLF file as a PyTorch detection dataset, check-out [this notebook](https://github.com/hagl-external/OpenLabelingFormat/blob/master/Tools/Notebooks/Demo_OLFDetection_PyTorch.ipynb).

For a demo on how to convert an OLF file into a detection TFRecord, checkout [this notebook](https://github.com/hagl-external/OpenLabelingFormat/blob/master/Tools/Notebooks/Demo_OLFDetection_TFRecord.ipynb).

## License
The OLF standard, the schema file(s) and the documentation file(s) are licensed under a<br />
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png" /></a><a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"> Creative Commons Attribution-ShareAlike 4.0 International License</a>.

For all other parts of the repository [this](https://github.com/hagl-external/OpenLabelingFormat/blob/master/License.md) license applies.

## Maintainer & Copyright
This repository is currently maintained by [HELLA Aglaia Mobile Vision GmbH](https://hella-aglaia.com).

<img src="https://github.com/hagl-external/OpenLabelingFormat/blob/master/Resources/hagl_logo.jpg" width="120" /> Copyright (c) 2020, HELLA Aglaia Mobile Vision GmbH
