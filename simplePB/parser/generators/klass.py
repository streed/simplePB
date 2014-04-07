
class Klass( object ):

  IMPORT = "import simplePB"

  def __init__( self, name=None, package=None, attributes=[], includes=[] ):
    self.package = package
    self.name = name
    self.attributes = attributes
    self.includes = includes

  def generate( self ):
    return "%s\n%s\nclass %s:\n%s\n%s\n%s\n%s\n%s\n" % ( 
        self.IMPORT, 
        self.generateImports(), 
        self.name, 
        self.generateMembers(), 
        self.generateConstructor(),
        self.generateOutputs(), 
        self.generateInputs(),
        self.generateEncode() )

  def generateConstructor( self ):
    s = ""

    s += "  def __init__( self, %s ):\n" % ( ",".join( [ i["key"] for i in self.attributes ] ) )
    for i in self.attributes:
      s += "    self.%s = %s\n" % ( i["key"], i["key"] )

    return s

  def generateMembers( self ):
    m = []
    for i in self.attributes:
      if( isinstance( i["value"], dict ) ):
        m.append( "  _%s = List( %s() )" % ( i["key"], i["value"]["List"] ) )
      else:
        m.append( "  _%s = %s()" % ( i["key"], i["value"] ) )

    return "\n".join( m )

  def generateImports( self ):
    m = []
    for i in self.includes:
      m.append( "from ..%s import %s" % i["protocol"]["name"], i["protocol"]["name"] )

    return "\n".join( m )

  def generateOutputs( self ):
    m = []

    for i in self.attributes:
      s = ""
      s += "  def _out_%s( self ):\n" % ( i["key"] )
      s += "    return self._%s.encode( self.%s )\n" % ( i["key"], i["key"] )
      m.append( s )

    return "\n".join( m )

  def generateInputs( self ):
    m = []

    for i in self.attributes:
      s = ""
      s += "  def _in_%s( self, v ):\n" % ( i["key"] )
      s += "    %s = self._%s.decode( v )\n" % ( i["key"], i["key"] )
      m.append( s )

    return "\n".join( m )

  def generateEncode( self ):
    s = ""
    s += "  @property\n"
    s += "  def encode( self ):\n"
    s += "    ret = \"\"\n"
    for i in self.attributes:
      s += "    ret += self._out_%s()\n" % i["key"]
    s += "    return ret\n"

    return s

  def generateDecode( self ):
    pass
