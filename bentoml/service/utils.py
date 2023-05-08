import base64
import logging
from io import BytesIO
from typing import Optional

import boto3
import requests
from PIL import Image

def read_image(data) -> Optional[Image.Image]:
    """
    Implement reading image input passed by user in request as one of following fields:
    - 'image' - return decoded image
    - 'url' - return image downloaded from url
    - 's3_url' - return image read from s3_url in form <bucket_name>/<object_key>
    """
    img = None

    image_en = data.get('image', None)
    if image_en:
        binary_data: bytes = base64.b64decode(image_en)
        return Image.open(BytesIO(binary_data))

    url = data.get('url', None)
    if url:
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    s3_url = data.get('s3_url', None)
    if s3_url:
        s3 = boto3.resource('s3')
        bucket_name = s3_url.split('/')[0]
        key = '/'.join(s3_url.split('/')[1:])
        s3_object = s3.Object(bucket_name, key)
        file_content = s3_object.get()['Body'].read()
        return Image.open(BytesIO(file_content))

    return img