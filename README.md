# VIA2COCO

This repository contains Python code to convert annotations from Oxford's VGG Image Annotator (VIA) to Microsoft's Common Objects in Context (COCO) format.

## Installation

- Install the latest version of [Python 3.X](https://www.python.org/downloads/).

## Usage

The simplest usage would be to specify a list of categories.

Caveat:
-   categories should have distinct names,
-   the order matters, as it will be used to number categories.

```python
import convert as via2coco

input_dir = '/content/data/balloon/train/'
input_json = input_dir + 'via_region_data.json'
categories = ['balloon']

coco_dict = via2coco.convert(
    imgdir=input_dir,
    annpath=input_json,
    categories=categories,
)
```

By default, the first category is indexed as 1.
This can be changed to 0 (or any non-negative integer) as follows:

```python
import convert as via2coco

input_dir = '/content/data/balloon/train/'
input_json = input_dir + 'via_region_data.json'
categories = ['balloon']
first_class_index = 0

coco_dict = via2coco.convert(
    imgdir=input_dir,
    annpath=input_json,
    categories=categories,
    first_class_index=first_class_index,
)
```

To save the output as a JSON file:

```python
import convert as via2coco

input_dir = '/content/data/balloon/train/'
input_json = input_dir + 'via_region_data.json'
categories = ['balloon']

output_json = input_dir + 'coco_train.json'

coco_dict = via2coco.convert(
    imgdir=input_dir,
    annpath=input_json,
    categories=categories,
    output_file_name=output_json,
)
```

It is also possible to specify a list of super-categories.

Caveat:
-   super-categories can have the same name,
-   the lists of categories and super-categories should have the same length,
-   the order matters, as it will be used to match categories and super-categories. 

```python
import convert as via2coco

input_dir = '/content/data/balloon/train/'
input_json = input_dir + 'via_region_data.json'
categories = ['balloon']

super_categories = ['N/A']

coco_dict = via2coco.convert(
    imgdir=input_dir,
    annpath=input_json,
    categories=categories,
    super_categories=super_categories,
)
```

## References

-   [VIA2COCO: the original repository](https://github.com/codingwolfman/VIA2COCO)
-   [VGG Image Annotator (VIA)](http://www.robots.ox.ac.uk/~vgg/software/via/), by Oxford's Visual Geometry Group
-   [Common Objects in Context (COCO)](https://cocodataset.org/), by Microsoft
-   An example of the VIA format, [as shown in a Github issue](https://github.com/matterport/Mask_RCNN/issues/1973#issuecomment-577886927)
