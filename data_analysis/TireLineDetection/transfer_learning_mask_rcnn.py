from PIL import Image
import matplotlib.pyplot as plt
import torch
import torchvision.transforms as T
import torchvision
import torch
import numpy as np
import cv2
import random
import time
import os
from pycocotools.coco import COCO
import skimage.io as io


if __name__ == "__main__":   
    model = torchvision.models.detection.maskrcnn_resnet50_fpn_v2(pretrained=True)

    print(os.getcwd())


    data_dir='Car-Parts-Segmentation-master/testset'
    annotation_file='{}/annotations.json'.format(data_dir)

    coco=COCO(annotation_file)
    categoryIDs = coco.getCatIds()
    categories = coco.loadCats(categoryIDs)

    imgIds = coco.getImgIds()
    images = coco.loadImgs(imgIds)

    random_imgId = imgIds[np.random.randint(0,len(imgIds))]
    img = coco.loadImgs(random_imgId)[0]

    I = io.imread('{}/{}'.format(data_dir,img['path']))/255.0
    plt.imshow(I)
    plt.axis('off')

    annIds = coco.getAnnIds(imgIds=img['id'], iscrowd=None)
    anns = coco.loadAnns(annIds)
    coco.showAnns(anns)
    plt.show()
