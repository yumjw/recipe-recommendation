#referred to Jie Jenn's code on his youtube video

import io, os
from numpy import random
from google.cloud import vision  #pip intall google-vision-cloud
from Pillow_Utility import draw_borders, Image
import pandas as pd


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken.json" #input downloaded json file name
client = vision.ImageAnnotatorClient()

file_name = 'bag.jpg' #input image file name
image_path = os.path.join('images', file_name) #input image file directory

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.object_localization(image=image)
localized_object_annotations = response.localized_object_annotations

df = pd.DataFrame(columns=['name', 'score'])
for obj in localized_object_annotations:
    df = df.append(
        dict(
            name=obj.name,
            score=obj.score
        ),
        ignore_index=True)

#draw bounding boxes
pillow_image = Image.open(image_path)
for obj in localized_object_annotations:
    r, g, b = random.randint(150, 255), random.randint(
        150, 255), random.randint(150, 255)
    #r, g, b = 255, 255, 255

    draw_borders(pillow_image, obj.bounding_poly, (r, g, b),
        pillow_image.size, obj.name, obj.score)

pillow_image.show()
