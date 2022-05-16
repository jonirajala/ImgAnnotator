# https://pytorch.org/docs/stable/data.html#torch.utils.data.Dataset
# https://pytorch.org/tutorials/beginner/basics/data_tutorial.html

import os
import sqlite3
from torchvision.io import read_image
from torch.utils.data import Dataset
from torchvision.transforms import Resize, Compose
import pandas as pd


from ui.utils.sql_operations import create_connection, select_all_annotations
from ui.main import DATABASE_PATH


class ImageAnnotationsDataset(Dataset):
    """
    Custom torch dataset class for the annotated images

    params:
        img_dir: string
        transform: pytorch transforms
        target_transform: pytorch transforms
        testing: bool
    """
    def __init__(self, img_dir, transform=None, target_transform=None, testing=False):
        # if we are testing, we want to use temporary databes
        if testing:
            db = create_connection("../tests/testdatabase.db") # Connect to the database
        else:
            db = create_connection(DATABASE_PATH) # Connect to the database

        try:
            self.data = pd.DataFrame(select_all_annotations(db)).groupby(1)  # Query all the annotations and group by image
        except KeyError:
            print("Empty Dataset")
            self.data = []

        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if self.data != []:
            image = list(self.data.groups.keys())[idx]
            annotations_df = self.data.get_group(image)
            annotations = [eval(i) for i in annotations_df[2].tolist()] # Turn list of strings to list of tuples
            labels = annotations_df[3].tolist()
            img_path = os.path.join(self.img_dir, image)
            image = read_image(img_path)

            transform = Compose([
                    Resize((520, 920)) # Mandatory to match the annotations and the images
                ])
            if self.transform:
                transform.append(self.transform)

            image = transform(image)

            if self.target_transform:
                label = self.target_transform(labels)
                
            return image, (annotations, labels) # image: tensor, target tuple(boxes, labels) 
        return None
