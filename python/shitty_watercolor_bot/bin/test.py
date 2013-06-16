

from pgmagick import Image
from imgfx import ImgFX


fx=ImgFX()

#img=Image('watercolor-output.png')

img=fx.bobross('giraffe.jpg')
img.write('output.png')