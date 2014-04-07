import os
from .generators.klass import Klass

def create_modules( package ):
  """Super simple case for now, will need to create
     a method to have nested packages inside of each
     other, but this will require the ability to fix
     up the imports correctly as well."""

  #we need to make the package directory.
  #we need to make the folder that this
  #parsed file will live in.
  # currentPath + package
  paths = package.split( "." )
  package = os.path.join( "./", os.path.join( *paths ) )
  os.makedirs( package )

  #Create the __init__.py files
  temp = "./"
  for p in paths:
    temp = os.path.join( temp, p )
    open( "%s/__init__.py" % temp, "a" ).close()

def createClassFile( p ):
  """This will take the parsed file and write out the python classes for it
  and any of its included files.
  """
  create_modules( p["package"] )
  name = p["protocol"]["name"]
  name.lower()
  path = os.path.join( *p["package"].split( "." ) )
  with open( "./%s/%s.py" % ( path,  name ), "w" ) as f:
    for i in p["imports"]:
      createClassFile( i )

    c = Klass( package=p["package"], includes=p["imports"], **p["protocol"] )	

    f.write( c.generate() )

