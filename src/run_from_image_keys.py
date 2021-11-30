"""
This scripts computes a vector embedding for each image file stored on my AWS S3 storage, then writes a matrix
with all vector embeddings along with image labels in a text file.

TODO: big overhead, because a new S3 access session is opened for each image --> broadcast connection to S3?
"""

import random
from io import BytesIO

import PIL.Image
import boto3
from pyspark import Row

from common import start_spark
from encoder import Encoder

S3_BUCKET_NAME = 'nsaintgeoursbucket'


def load_image(image_key: str, bucket_name: str) -> PIL.Image.Image:
    """
    Load an image from AWS S3 storage.

    Args:
        image_key (str): image key in AWS S3 bucket
        bucket_name (str): S3 bucket name

    Returns: (PIL.Image.Image) RGB image data
    """
    bucket = boto3.resource('s3').Bucket(bucket_name)
    buffer = BytesIO()
    bucket.Object(image_key).download_fileobj(buffer)
    return PIL.Image.open(buffer)


def process_image(image_key: str) -> Row:
    """
    Encodes an image into a vector of float values using a pre-trained DNN encoder.

    Args:
        image_key (str): image key in AWS S3 bucket

    Returns: (Row) the image encoding, represented by a Row with fields:

        origin (str): image original path (i.e., the image key in S3 bucket)
        label (str): the image label
        x0 (float): first feature of image encoding
        (...)
        x_(n-1) (float): last feature of image encoding
    """
    print(f"...... process image {image_key}")
    image_label = image_key.split('/')[-2]
    image_array = load_image(image_key=image_key, bucket_name=S3_BUCKET_NAME)
    image_encoding = my_encoder.value.encode(image_array)
    image_encoding = {f'x{i}': value for i, value in enumerate(image_encoding)}
    return Row(origin=image_key, label=image_label, **image_encoding)


if __name__ == '__main__':
    spark = start_spark()

    print("... list images from Fruits 360 dataset")
    s3_bucket = boto3.resource('s3').Bucket(S3_BUCKET_NAME)
    image_keys = [image.key for image in s3_bucket.objects.all() if '.jpg' in image.key]
    image_keys = random.sample(image_keys, 3)

    print("... load image encoder")
    my_encoder = spark.sparkContext.broadcast(Encoder())

    print("... encode images and write output to file")
    output = spark.sparkContext.parallelize(image_keys).map(process_image).toDF()
    output.coalesce(1).write.csv("output", header="true", mode="overwrite")
