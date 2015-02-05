# collectd-write-qpid-json

A simple [Collectd][cd1] python plugin for writing metrics to an [AMQP
1.0][amqp1] compliant broker in the Collectd [JSON format][cd2] using Apache
Qpid's Messaging Api [python bindings][qpid2].

## But what about the supported AMQP plugin?

Collectd ships with an [AMQP Plugin][cd3] already. However it is based on the
[rabbitmq-c][rmq1] client library. RabbitMQ does not support the AMQP 1.0/0-10
versions of AMQP for whatever reason so I needed something else to talk to
brokers that only support AMQP 1.0/0-10 such as the Apache QPID C++ broker.

## How do I use it?

Configure your collectd.conf something similar to what is below:
```
<LoadPlugin python>
        Globals true
</LoadPlugin>
<Plugin python>
        ModulePath "/opt/collectd-write-qpid-json"
        Import write_qpid_json
        <Module write_qpid_json>
                TypesDB "/opt/collectd/share/collectd/types.db"
                TypesDB "/opt/collectd/etc/types.db"
                Exchange "collectd"
        </Module>
</Plugin>
```

Like many plugin's that use collectd's higher level language bindings, this
plugin needs Collectd's [type.db][cd4] so that it can properly provide
additional metadata about each collected value. I couldn't find a decent way to
ask Collectd for this information so you will need to duplicate it here even
though it is higher up in the config tree.

#### Support Options

Option   | Default      | Description
:------- |:------------ |:-----------
TypesDB  | ["/usr/share/collectd/types.db"] | List of TypesDB paths.
Host     | "localhost"  | Host of the AMQP endpoint.
Port     | "5672"       | Port that the AMQP endpoint is listening on.
User     | "guest"      | 
Password | "guest"      | 
Exchange | "amq.fanout" | AMQP address to send messages to.

## Should I use this?

I don't know if you should use it? I'm using it. I'll be responsive
if you have questions, fixes, bugs, if that helps. If you have any of
those you can interact with me via Github or shoot me an email
(craftsman@bendoerr.me).

<!-- TODO add details about why I wrote this, -->

## License
```
The MIT License (MIT)

Copyright (c) 2015 Ben Doerr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
<!-- Here be links -->
[amqp1]: http://www.amqp.org/resources/download "AMQP Protocol Downloads"
[cd3]: https://collectd.org/wiki/index.php/Plugin:AMQP
[cd1]: https://collectd.org/ "The system statistics collection daemon"
[cd2]: https://collectd.org/wiki/index.php/JSON "Collectd JSON format"
[cd4]: https://collectd.org/documentation/manpages/types.db.5.shtml
[qpid1]: https://qpid.apache.org/ "Messaging built on AMQP"
[qpid2]: https://qpid.apache.org/ "http://qpid.apache.org/components/messaging-api/index.html"
[rmq1]: https://github.com/alanxz/rmq1 "RabbitMQ C Client"
