

from pgmagick import Image
from imgfx import ImgFX


fx=ImgFX()

#img=Image('watercolor-output.png')

img=fx.bobross('test.jpg')
img.write('test-output.png')