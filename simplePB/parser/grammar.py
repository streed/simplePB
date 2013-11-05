import os
"""
package examples

proto Person {
	name -> String
	age -> Int
}
"""
import pyparsing as p

from generators.klass import Klass

NL =  p.LineEnd().suppress()
colon = p.Literal( ":" ).suppress()
arrow = p.Keyword( "->" ).suppress()
proto = p.Keyword( "proto" ).suppress()
package = p.Keyword( "package" ).suppress()
openBracket = p.Literal( "{" ).suppress()
closeBracket = p.Literal( "}" ).suppress()
word = p.Word( p.alphas )
key = word
value = word

Include = p.Keyword( "include" ) + p.Combine( p.Word( p.alphanums ) + ".pb" ) + p.OneOrMore( NL )
Include.setParseAction( lambda s, l, t: t[1] )
PackageName = package + word + p.OneOrMore( NL )
List = value + colon + value
List.setParseAction( lambda s, l, t: { t[0]: t[1] } )
Attribute = key + arrow + p.Or( [ value, List ] )  + NL
Attribute.setParseAction( lambda s, l, t: { "key": t[0], "value": t[1] } )

indentStack = [1]
def checkPeerIndent( s, l, t ):
	c = p.col( l, s )
	print(  c, indentStack[-1] )
	if( c != indentStack[-1] ):
		if( ( not indentStack ) or c > indentStack[-1] ):
			raise p.ParseFatalException( s, l, "illegal nesting" )
		raise p.ParseException( s, l, "not a peer entry" )

def checkSubIndent( s, l, t ):
	c = p.col( l, s )
	if( c > indentStack[-1] ):
		indentStack.append( c )
	else:
		raise p.ParseException( s, l, "not a subentry" )

def checkUnindent( s, l, t ):
	if( l >= len( s ) ):
		return

	c = p.col( l, s )

	if( not (  c < indentStack[-1] and c <= indentStack[-2] ) ):
		raise p.ParseException( s, l, "not an unindent" )

def doUndent():
	indentStack.pop()

INDENT = NL + p.Empty() + p.Empty().copy().setParseAction( checkSubIndent ) 
UNDENT = p.FollowedBy( p.Empty() ).setParseAction( checkUnindent )
UNDENT.setParseAction( doUndent )

IndentedAttribute = Attribute.copy().setParseAction( checkPeerIndent )
IndentedAttribute.setParseAction( lambda s, l, t: { "key": t[0], "value": t[1] } )
IndentedProtocol = p.Group( proto + word + arrow + INDENT + p.Group( p.OneOrMore( IndentedAttribute ) ) + UNDENT )
IndentedProtocol.setParseAction( lambda s, l, t: { "name": t[0][0], "attributes": t[0][1][:] } )

ProtocolDescription = PackageName + p.Group( p.ZeroOrMore( Include ) ) + IndentedProtocol
ProtocolDescription.setParseAction( lambda s, l, t: { "package": t[0], "includes": t[1][:], "protocol": t[2] } )

def protocolParseFile( f ):
	path = list( os.path.split( f.name )[:1] )
	parsed = ProtocolDescription.parseFile( f )[0]
	
	includes = parsed["includes"][:]
	parsed["includes"] = []

	for i in includes:
		p = os.path.join( path[0], i )
		parsed["includes"].append( protocolParseFile( open( p, "r" ) ) )

	return parsed

def createClassFile( p ):

	with open( "./test%s.py" % p["protocol"]["name"], "w" ) as f:
		for i in p["includes"]:
			createClassFile( i )

		c = Klass( includes=p["includes"], **p["protocol"] )	

		f.write( c.generate() )

if __name__ == "__main__":
	createClassFile( protocolParseFile( open( "./simplePB/examples/family.pb" ) ) )
