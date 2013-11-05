import os
"""
package examples

proto Person {
	name -> String
	age -> Int
}
"""
import pyparsing as p

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
Protocol = proto + word + openBracket + p.OneOrMore( NL ) + p.OneOrMore( Attribute ) + p.Optional( NL ) + closeBracket
Protocol.setParseAction( lambda s, l, t: { "name": t[0], "attributes": t[1:] } )
ProtocolDescription = PackageName + p.Group( p.ZeroOrMore( Include ) ) + Protocol
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
			f.write( "from .%s import %s\n" % ( i["protocol"]["name"], i["protocol"]["name"] ) )
			createClassFile( i )

		f.write( "class %s:\n" % p["protocol"]["name"] )
		f.write( "\t__metaclass__ = simplePB.metaclass.GeneratedMetaClass\n" )
		for i in p["protocol"]["attributes"]:
			if( "List" in i["value"] ):
				f.write( "\t%s = List( %s() )\n" % ( i["key"], i["value"]["List"] ) )
			else:
				f.write( "\t%s = %s()\n" % ( i["key"], i["value"] ) )
	

if __name__ == "__main__":
	createClassFile( protocolParseFile( open( "./simplePB/examples/family.pb" ) ) )
