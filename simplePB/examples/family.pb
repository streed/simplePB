package examples

include person.pb
include child.pb

proto Family ->
	parents -> List:Person
	children -> List:Children

