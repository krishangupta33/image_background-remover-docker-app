from rembg import remove
from PIL import Image


input = Image.open('cat.webp')

output = remove(input)

output.save('out.png')