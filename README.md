# collectd-write-qpid-json

A simple [Collectd][collectd-home] python plugin for writing metrics to an
[AMQP 1.0][amqp-home] compliant broker in the Collectd [JSON
format][collectd-json] using Apache Qpid's Messaging Api [python
bindings][qpid-messaging].

## But what about the supported AMQP plugin?

Collectd ships with an [AMQP Plugin][collectd-amqp] already. However it is
based on the [rabbitmq-c][rabbitmq-c] client library. RabbitMQ does not support
the AMQP 1.0/0-10 versions of AMQP for whatever reason so I needed something
else to talk to brokers that only support AMQP 1.0/0-10 such as the Apache QPID
C++ broker.

## License

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


[collectd-home]: https://collectd.org/ "The system statistics collection daemon"
[collectd-json]: https://collectd.org/wiki/index.php/JSON "Collectd JSON format"
[collectd-amqp]: https://collectd.org/wiki/index.php/Plugin:AMQP
[amqp-home]: http://www.amqp.org/resources/download "AMQP Protocol Downloads"
[qpid-home]: https://qpid.apache.org/ "Messaging built on AMQP"
[qpid-messaging]: https://qpid.apache.org/ "http://qpid.apache.org/components/messaging-api/index.html"
[rabbitmq-c]: https://github.com/alanxz/rabbitmq-c "RabbitMQ C Client"
