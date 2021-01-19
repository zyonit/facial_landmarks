import time
import cv2
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import imutils
import matplotlib.image as mpimg
from collections import OrderedDict
# from skimage import io, transform
from math import *
import xml.etree.ElementTree as ET

import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms.functional as TF
from torchvision import datasets, models, transforms
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import numpy as np
from numpy import ones,vstack
from numpy.linalg import lstsq
import os
import matplotlib.pyplot as plt
from PIL import Image

train_metadatapath = r"../src/list_98pt_rect_attr_train.txt"
test_metadatapath = r"../src/list_98pt_rect_attr_test.txt"
images_path = r"C:\Users\zayon\Documents\MSC\NN\project\datasets\wflw\WFLW_images"

class Transforms():
    def __init__(self):
        pass

    def rotate(self, image, landmarks, angle):
        angle = random.uniform(-angle, +angle)

        transformation_matrix = torch.tensor([
            [+cos(radians(angle)), -sin(radians(angle))],
            [+sin(radians(angle)), +cos(radians(angle))]
        ])

        image = imutils.rotate(np.array(image), angle)

        landmarks = landmarks - 0.5
        new_landmarks = np.matmul(landmarks, transformation_matrix)
        new_landmarks = new_landmarks + 0.5
        return Image.fromarray(image), new_landmarks

    def resize(self, image, landmarks, img_size):
        image = TF.resize(image, img_size)
        return image, landmarks

    def color_jitter(self, image, landmarks):
        color_jitter = transforms.ColorJitter(brightness=0.3,
                                              contrast=0.3,
                                              saturation=0.3,
                                              hue=0.1)
        image = color_jitter(image)
        return image, landmarks

    def crop_face(self, image, landmarks, crops):
        left = float(crops[0])
        top = float(crops[1])
        width = crops[2]-crops[0]
        height = crops[3]-crops[1]

        image = TF.crop(image, top, left, height, width)

        img_shape = np.array(image).shape
        landmarks = torch.tensor(landmarks) - torch.tensor([[left, top]])
        landmarks = landmarks / torch.tensor([float(img_shape[1]), float(img_shape[0])])
        return image, landmarks

    def __call__(self, image, landmarks, crops):
        image = Image.fromarray(image)
        image, landmarks = self.crop_face(image, landmarks, crops)
        image, landmarks = self.resize(image, landmarks, (224, 224))
        image, landmarks = self.color_jitter(image, landmarks)
        image, landmarks = self.rotate(image, landmarks, angle=10)

        image = TF.to_tensor(image)
        image = TF.normalize(image, [0.5], [0.5])
        return image, landmarks

class FaceLandmarksDataset(Dataset):

    def __init__(self,train = True,  transform=None):

        self.image_filenames = []
        self.landmarks = []
        self.crops = []
        self.transform = transform
        if train == True:
            self.metadatapath = train_metadatapath
        else:
            self.metadatapath = test_metadatapath

        with open(train_metadatapath, 'r') as filehandle:
            for line in filehandle:
                # remove linebreak which is the last character of the string
                face_instance = line[:-1].split(' ')

                self.image_filenames.append( face_instance[-1])
                # self.landmarks.append([float(i) for i in face_instance[:196]] )
                self.crops.append([int(i) for i in face_instance[196:200]] )
                landmark = []
                for num in range(98):
                    x_coordinate = (float(face_instance[num*2]))
                    y_coordinate = float(face_instance[num*2 + 1])
                    landmark.append(list(map(int,[x_coordinate, y_coordinate])))
                self.landmarks.append(landmark)

        self.landmarks = np.array(self.landmarks).astype('float32')

        assert len(self.image_filenames) == len(self.landmarks)

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, index):
        image = cv2.imread(os.path.join(images_path, self.image_filenames[index]), 1) ## chnaged to color image
        landmarks = self.landmarks[index]

        if self.transform:
            image, landmarks = self.transform(image, landmarks, self.crops[index])

        landmarks = landmarks - 0.5

        return image, landmarks
#  # dataset = FaceLandmarksDataset(transform=Transforms())
# dataset = FaceLandmarksDataset(transform=None)
#
# image, landmarks = dataset[0]
# print(image.shape)
# # landmarks = (landmarks + 0.5) * 224
# plt.figure(figsize=(10, 10))
# # plt.figure.show()
# # image = image.permute(1, 2, 0)
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB));
# plt.show()

dataset = FaceLandmarksDataset(transform=Transforms())

image, landmarks = dataset[0]
print(image.shape)
landmarks = (landmarks + 0.5) * 224
plt.figure(figsize=(10, 10))
image = image.permute(1, 2, 0)
plt.imshow(cv2.cvtColor(image.numpy(), cv2.COLOR_BGR2RGB));

plt.scatter(landmarks[:,0], landmarks[:,1], s=8);
plt.show()
