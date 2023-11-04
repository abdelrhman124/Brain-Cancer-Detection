from PIL import Image
import os

image = Image.open('Y4.jpg')

width, height = image.size
new_size = (width//2, height//2)
resized_image = image.resize(new_size)

resized_image.save('compressed_image2.jpg', optimize=True, quality=50)