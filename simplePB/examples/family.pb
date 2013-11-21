package examples.family

import base.person
import children.child

proto Family ->
	parents -> List:Person
	children -> List:Children

