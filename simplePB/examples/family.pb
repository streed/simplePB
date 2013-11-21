package examples.family

include .base.person
include .children.child

proto Family ->
	parents -> List:Person
	children -> List:Children

