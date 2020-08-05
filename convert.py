import os
from PIL import Image
import datetime
import json
import getArea


def create_image_info(
    image_id,
    file_name,
    image_size,
    date_captured=datetime.datetime.utcnow().isoformat(" "),
    license_id=1,
    coco_url="",
    flickr_url="",
):
    image_info = {
        "id": image_id,
        "file_name": file_name,
        "width": image_size[0],
        "height": image_size[1],
        "date_captured": date_captured,
        "license": license_id,
        "coco_url": coco_url,
        "flickr_url": flickr_url,
    }

    return image_info


def create_annotation_info(
    annotation_id, image_id, category_id, is_crowd, area, bounding_box, segmentation
):
    annotation_info = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "iscrowd": is_crowd,
        "area": area,  # float
        "bbox": bounding_box,  # [x,y,width,height]
        "segmentation": segmentation,  # [polygon]
    }

    return annotation_info


def get_segmenation(coord_x, coord_y):
    seg = []
    for x, y in zip(coord_x, coord_y):
        seg.append(x)
        seg.append(y)
    return [seg]


def convert(
    imgdir,
    annpath,
    categories=None,
    super_categories=None,
    output_file_name=None,
    first_class_index=1,  # typically, 0 or 1
):
    """
    :param imgdir: directory for your images
    :param annpath: path for your annotations
    :return: coco_output is a dictionary of coco style which you could dump it into a json file
    as for keywords 'info','licenses','categories',you should modify them manually
    """

    if categories is None:
        categories = ["rib", "clavicle"]

    default_category = categories[0]

    category_dict = dict()
    for (cat_id, cat_name) in enumerate(categories, start=first_class_index):
        category_dict[cat_name] = cat_id

    if super_categories is None:
        default_super_category = "bone"
        super_categories = [default_super_category for _ in categories]

    coco_output = {}
    coco_output["info"] = {
        "description": "Example Dataset",
        "url": "https://github.com/waspinator/pycococreator",
        "version": "0.1.0",
        "year": 2018,
        "contributor": "waspinator",
        "date_created": datetime.datetime.utcnow().isoformat(" "),
    }
    coco_output["licenses"] = [
        {
            "id": 1,
            "name": "Attribution-NonCommercial-ShareAlike License",
            "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
        }
    ]
    coco_output["categories"] = [
        {
            "id": category_dict[cat_name],
            "name": cat_name,
            "supercategory": super_cat_name,
        }
        for (cat_name, super_cat_name) in zip(categories, super_categories)
    ]
    coco_output["images"] = []
    coco_output["annotations"] = []

    ann = json.load(open(annpath))
    # annotations id start from zero
    ann_id = 0
    # in VIA annotations, keys are image name
    for img_id, key in enumerate(ann.keys()):

        filename = ann[key]["filename"]
        img = Image.open(imgdir + filename)
        # make image info and storage it in coco_output['images']
        image_info = create_image_info(
            img_id, os.path.basename(filename), image_size=img.size
        )
        # Caveat: image shapes are conventionally (height, width) whereas image sizes are conventionally (width, height)
        # References:
        # -   https://note.nkmk.me/en/python-opencv-pillow-image-size/
        # -   https://github.com/facebookresearch/detectron2/blob/master/detectron2/data/detection_utils.py#L189
        coco_output["images"].append(image_info)
        regions = ann[key]["regions"]
        # for one image ,there are many regions,they share the same img id
        for region in regions:
            region_attributes = regions[region]["region_attributes"]
            try:
                cat_name = region_attributes["label"]
            except KeyError:
                cat_name = default_category
            try:
                cat_id = category_dict[cat_name]
            except KeyError:
                print("Skipping unknown category {} in {}".format(cat_name, filename))
                continue
            iscrowd = 0
            shape_attributes = regions[region]["shape_attributes"]
            points_x = shape_attributes["all_points_x"]
            points_y = shape_attributes["all_points_y"]
            area = getArea.GetAreaOfPolyGon(points_x, points_y)
            min_x = min(points_x)
            max_x = max(points_x)
            min_y = min(points_y)
            max_y = max(points_y)
            box = [min_x, min_y, max_x - min_x, max_y - min_y]
            segmentation = get_segmenation(points_x, points_y)
            # make annotations info and storage it in coco_output['annotations']
            ann_info = create_annotation_info(
                ann_id, img_id, cat_id, iscrowd, area, box, segmentation
            )
            coco_output["annotations"].append(ann_info)
            ann_id = ann_id + 1

    if output_file_name is not None:
        print("Saving to {}".format(output_file_name))

        with open(output_file_name, "w") as f:
            json.dump(coco_output, f)

    return coco_output


if __name__ == "__main__":
    input_dir = "/content/data/balloon/train/"
    input_json = input_dir + "via_region_data.json"
    categories = ["balloon"]

    super_categories = ["N/A"]

    output_json = input_dir + "coco_train.json"

    coco_dict = convert(
        imgdir=input_dir,
        annpath=input_json,
        categories=categories,
        super_categories=super_categories,
        output_file_name=output_json,
    )
