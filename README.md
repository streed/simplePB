Simple Protocol Buffers
=======================
[![Build Status](https://travis-ci.org/streed/simplePB.png?branch=master)](https://travis-ci.org/streed/simplePB)

Problem:
========

Defining a suitable communication protocol can be difficult and hard to maintain when new fields are added to the protocol at a later point.

Solution:
=========
Looking at the Google library [Protocol Buffers](https://developers.google.com/protocol-buffers) I found a conventient soluton to my problem.
But, I wanted to take it a step further and create a DSL on top of the protocol buffers themselves and from this allow for the following properties.

* Protocols are broken into _proto_ classes.
* Protocols are defined in _.pb_ files.
* The _.pb_ files are compiled into their equivalent Python classes.
* Objects sent will be serialized into a binary format that can be represented in Base64.
* Objects read can be deserialized back into their Python object.

This mimics the current Protocol Buffers offered by Google, but to allow for the flexibility for my projects I am building ontop of this and
adding the following additional functionality.

* Protocols can inherit from other Protocols.
* Protocols can overload member fields from inherited Protocols.

This above allows for the following situation

_header.pb_
```ruby
package example

proto Header ->
	id -> Int
	length -> Int

```

_message.pb_
```ruby
package example

import header

proto Message | Header | ->
	message -> String
	from -> String
	to -> List:String
	timestamp -> Date

```

_heartbeat.pb_
```ruby
package example

import message

proto HeartBeat | Message | ->
	heartbeatId -> Int

```
The above class hierarchy allows for a common base _Header_ class to be defined that then allows for common fields to be moved there and independently
modified with respect to its sub-class Protocols.

The above compilation of data members in the ``HeartBeat`` protocol is identical to the following definition:

```ruby
package example

proto HeartBeat ->
	id -> Int
	length -> Int
	message -> String
	from -> String
	to -> List:String
	timestamp -> Date
	heartbeatId -> Int
```

But, this much more verbose version is a ``HeartBeat`` message that contains much more data that ultimately should not be handled
in the ``HeartBeat`` protocol and should be pushed down into parent protocols. This also allows for polymorphism when dealing with
the messages for example that along with the heart beat there is another message as such:

```ruby
package example

import message

proto Hosts | Message | ->
	hosts -> List:String
```

```python
from example.hosts import Hosts
from example.heartbeat import HeartBeat

hs = Hosts()
hs.hosts.concat( [ "10.0.0.1", "10.0.0.2", "10.0.0.3" ] )

hb = HeartBeat()
hb.heartBeatId = 100

messages = [ hs, hb ]

for m in messages:
    send( messages, to="10.0.0.5", from="10.0.0.6" )

```

In the case above the send message simply works with ``Message`` protocols. And, thus does not care that there is a list
of ``hosts`` or a ``heartBeatId`` tacked onto the messages. When the message is finally sent the method ``serialize`` is
called and everything is handled automatically and the receiving client will properly read the messages.
