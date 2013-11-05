
class Klass( object ):

	IMPORT = "import simplePB"
	METACLASS = "__metaclass__ = simplePB.metaclass.GeneratedMetaclass"

	def __init__( self, name=None, attributes=[], includes=[] ):
		self.name = name
		self.attributes = attributes
		self.includes = includes

	def generate( self ):
		return "%s\n%s\nclass %s:\n    %s\n%s\n" % ( self.IMPORT, self.generateImports(), self.name, self.METACLASS,
							self.generateMembers() )

	def generateMembers( self ):
		m = []
		for i in self.attributes:
			if( isinstance( i["value"], dict ) ):
				m.append( "    %s = List( %s() )" % ( i["key"], i["value"]["List"] ) )
			else:
				m.append( "    %s = %s()" % ( i["key"], i["value"] ) )

		return "\n".join( m )

	def generateImports( self ):
		m = []
		for i in self.includes:
			m.append( "import %s" % i["protocol"]["name"] )

		return "\n".join( m )
