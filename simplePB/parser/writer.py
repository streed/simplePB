import os
from .generators.klass import Klass

def create_modules( package ):
	"""Super simple case for now, will need to create
	a method to have nested packages inside of each
	other, but this will require the ability to fix
	up the imports correctly as well."""
	os.mkdir( package )

def createClassFile( p ):
	"""This will take the parsed file and write out the python classes for it
	and any of its included files.
	"""

	#we need to make the package directory.
	os.mkdir( p["package"] )
	create_modules( p["package"] )
	with open( "./%s/%s.py" %( p["package"],  p["protocol"]["name"] ), "w" ) as f:
		for i in p["includes"]:
			createClassFile( i )

		c = Klass( package=p["package"], includes=p["includes"], **p["protocol"] )	

		f.write( c.generate() )

