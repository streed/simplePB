import os
"""
This describes the grammar for the following format:

human.pb
>>>>>>>
package examples

proto Human ->
	name -> String
	age -> Int

child.pb
>>>>>>>

package examples

import human.pb

proto Child | Human | ->
	favoriteColor -> String

parent.pb
>>>>>>>
package examples

import human.pb
import child.pb

proto Parent | Human | ->
	familySize -> Int
	numberOfChildren -> Int
	children -> List:Children

Protocol := package + imports + proto
package := "package" word
imports := import | import + imports
import := "import" word
proto := ( proto word | proto word parent ) arrow attributes
attributes := attribute | attribute attributes
attribute := word arrow word
parent := pipe word pipe
proto := "proto"
word := [a-zA-Z]{32}
pipe := "|"
arrow := "->"

One note is that atrtibutes must have a tab or spacing that is consistent, such as is the same syntax
for python when using a new code block.

"""
__author__ = "streed"
__version__ = "0.0"


import pyparsing as p

#TODO Make this thread-safe
#The stack variable for parsing the tab/space nesting.
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

def indentedProtocol( original, loc, tokens ):
	tokens = tokens.pop()

	if( len( tokens ) == 3 ):
		return { "name": tokens[0],
			 "parent": tokens[1],
			 "attributes": tokens[2].asList() }
	else:
		return { "name": tokens[0],
			 "attributes": tokens[1].asList() }

NL =  p.LineEnd().suppress()
INDENT = NL + p.Empty() + p.Empty().copy().setParseAction( checkSubIndent ) 
UNDENT = p.FollowedBy( p.Empty() ).setParseAction( checkUnindent )
UNDENT.setParseAction( doUndent )
colon = p.Literal( ":" ).suppress()
pipe = p.Literal( "|" ).suppress()
comma = p.Literal( "," ).suppress()
arrow = p.Keyword( "->" ).suppress()
proto = p.Keyword( "proto" ).suppress()
package = p.Keyword( "package" ).suppress()
openBracket = p.Literal( "{" ).suppress()
closeBracket = p.Literal( "}" ).suppress()
word = p.Word( p.alphas )
key = word
value = word
dot = p.Literal( "." ).suppress()
Import = p.Keyword( "import" ) + p.Combine( p.Word( p.alphanums ) ) + p.OneOrMore( NL )
Import.setParseAction( lambda s, l, t: t[1] + ".pb" )
PackagePart = word + dot
PackageParts = p.Group( p.OneOrMore( PackagePart ) + word )
PackageParts.setParseAction( lambda s, l, t: ".".join( t[0] ) )
PackageName = package + p.Or( [ PackageParts, word ] ) + p.OneOrMore( NL )
List = value + colon + value
List.setParseAction( lambda s, l, t: { t[0]: t[1] } )
Attribute = key + arrow + p.Or( [ value, List ] )  + NL
Attribute.setParseAction( lambda s, l, t: { "key": t[0], "value": t[1] } )
InheritedProtocols = pipe + word + pipe
IndentedAttribute = Attribute.copy().setParseAction( checkPeerIndent )
IndentedAttribute.setParseAction( lambda s, l, t: { "key": t[0], "value": t[1] } )
IndentedProtocol = p.Group( proto + word + p.Optional( InheritedProtocols ) + arrow + INDENT + p.Group( p.OneOrMore( IndentedAttribute ) ) + UNDENT )
IndentedProtocol.setParseAction( indentedProtocol )
ProtocolDescription = PackageName + p.Group( p.ZeroOrMore( Import ) ) + IndentedProtocol
ProtocolDescription.setParseAction( lambda s, l, t: { "package": t[0], "imports": t[1][:], "protocol": t[2] } )

def protocolParseFile( f ):
	"""This will parse the file handle `f` and then return the dict that explains the
	parsed information. This will also parse and recursively read in all of the imports.

	TODO: Add in a method to detect a circular dependency otherwise this could cause serious
	problems.
	"""

	path = list( os.path.split( f.name )[:1] )
	parsed = ProtocolDescription.parseFile( f )[0]

	imports = parsed["imports"][:]
	parsed["imports"] = []

	for i in imports:
		p = os.path.join( path[0], i )
		parsed["imports"].append( protocolParseFile( open( p, "r" ) ) )

	return parsed

