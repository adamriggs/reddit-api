from pgmagick import Image, Color, CompositeOperator, Geometry

class ImgFX(object):
	def __init__(self):
		
		pass
	
	def watercolor(self,imgStr):
		img=Image(imgStr)
		img.blur(2,2)
		img.oilPaint(5)
		img.enhance()
		img.sharpen()

		pink=Color(250,218,221,75)

		toplayer=Image(img.size(),pink)
		toplayer.matte(True)

		img.matte(True)
		img.composite(toplayer,0,0,CompositeOperator.CopyOpacityCompositeOp)

		img.blur(2,2)
		
		#img.write('watercolor-output.png')
		return img
		
	def bobross(self,imgStr):
		bob=Image('bob-transparent-canvas.png')
		bob.matte(True)
		
		img=self.watercolor(imgStr)
		#img.matte(True)
		newsize=Geometry(210,380)
		newsize.aspect(True)
		img.scale(newsize)
		
		#img.oilPaint(3)
		#img.enhance()
		#img.sharpen()
		#img.blur(2,2)
		#img.shear(-25,-15)
		result=Image(bob.size(),'white')
		result.composite(img,390,20,CompositeOperator.OverCompositeOp)
		result.composite(bob,0,0,CompositeOperator.OverCompositeOp)
		#img.debug(True)
		#bob.composite(img,390,20,CompositeOperator.OverCompositeOp)
		
		
		return result