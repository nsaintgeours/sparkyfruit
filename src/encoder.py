"""
Pre-trained deep neural network for image encoding.
"""
from typing import List

import PIL.Image
import torch
import torchvision.models as models
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize


class Encoder(object):

    def __init__(self):
        """
        Returns a new Encoder instance with attributes:

            model (models.vgg.VGG): pre-trained deep neural network with last classification layer removed.
            transform (Compose): input image transformation that the model expect.
        """
        self.model = models.vgg16(pretrained=True)
        self.model.classifier = torch.nn.Sequential(*[self.model.classifier[i] for i in range(5)])
        self.transform = Compose([
            Resize(255),
            CenterCrop(224),
            ToTensor(),
            Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def encode(self, image_array: PIL.Image.Image) -> List[float]:
        """
        Encodes a RGB image into a fixed-sized vector.

        Args:
            image_array (PIL.Image.Image): RGB image data

        Returns: (List[float]) encoding vector with fixed size n=3.
        """
        image_tensor = self.transform(image_array)
        image_batch = image_tensor.unsqueeze(0)
        with torch.no_grad():
            image_encoding = self.model(image_batch)[0].tolist()[:3]
        return image_encoding
