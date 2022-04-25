import numpy as np
import json
import random
import torch
from torchvision import transforms
from skimage.segmentation import slic
from torchvision import utils
from PIL import Image
from skimage.util import img_as_float
from skimage.segmentation import mark_boundaries
from skimage import io
from skimage.data import astronaut
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
img = img_as_float(io.imread("data/image_1_resized.png"))

segments = slic(img, n_segments=4, compactness=10)
ax.plot(mark_boundaries(img, segments))
fig.savefig('foo.png')
plt.close(fig)

target_height = 224
target_width = 224
'''img = Image.open('data/image_1.JPG')
resize = transforms.Compose([transforms.Scale((target_height,target_width)),transforms.ToTensor()])
print("original image size",img.size)
utils.save_image(resize(img),"data/image_1_resized.png")'''

img = img_as_float(io.imread("data/image_1_resized.png"))
print(img.shape)
all_data ={}
all_data['explanations'] = (np.random.random((target_height,target_width))).tolist()

number_of_segments=20

'''for i in range(1,number_of_segments):
    values = torch.from_numpy(slic(img, n_segments=i))
    print(type(values))
    #all_data['segments_'+str(i)]=(slic(img, n_segments=i)).tolist()
    print(i,torch.max(values),torch.min(values))'''

'''with open("data.json",'w') as file:
    json.dump(all_data,file)'''



