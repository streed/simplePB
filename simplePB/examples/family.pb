package examples

include person
include child

proto Family {
	parents -> List:Person
	children -> List:Children
}
