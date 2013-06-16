from pgmagick import Image, Color, CompositeOperator, Geometry

class ImgFX(object):
	def __init__(self):
		
		pass
	
	def watercolor(self,imgObj):
		print "watercolor()"
		img=imgObj
		#img.blur(2,2)
		img.oilPaint(1)
		img.enhance()
		img.sharpen()

		pink=Color(250,218,221,75)

		toplayer=Image(img.size(),pink)
		toplayer.matte(True)

		img.matte(True)
		img.composite(toplayer,0,0,CompositeOperator.CopyOpacityCompositeOp)

		img.blur(0,1)
		
		img.write('output.png')
		return img
		
	def bobross(self,imgStr):
		print "bobross()"
		bob=Image('bob-transparent-canvas.png')
		bob.matte(True)
		#print "1"
		img=Image(imgStr)
		#print "2"
		newsize=Geometry(200,343)
		newsize.aspect(True)
		img.scale(newsize)
		#print "3"
		img=self.watercolor(img)
		#print "4"
		result=Image(bob.size(),'white')
		result.composite(img,392,22,CompositeOperator.OverCompositeOp)
		result.composite(bob,0,0,CompositeOperator.OverCompositeOp)
		
		return result