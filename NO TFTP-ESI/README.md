Python-3 TCP and UDP servers and clients
========================================

These examples implement a very simple service called ``upper``. The ``upper`` servers
reply to the client the uppercase version of the text message that it sends.

As they have a teaching objective. I sacrificed error handling (like exceptions) for
readability and size. A right implementation should add that mechanisms.

You should install ``mercurial`` software in your computer and download this repository with next command:

    :::bash

    $ hg clone https://bitbucket.org/esi_atc/upper


UDP
---

* [client] [udp-client]
* [synchronous server] [udp-server]
* [synchronous server with SocketServer] [udp-SS]

* [multiprocess server][udp-fork]
* [multiprocess server with SocketServer] [udp-SS-fork]


[udp-client]: https://bitbucket.org/arco_group/upper/raw/tip/UDP_client.py
[udp-server]: https://bitbucket.org/arco_group/upper/raw/tip/UDP_server.py
[udp-SS]: https://bitbucket.org/arco_group/upper/raw/tip/UDP_SS.py

[udp-fork]: https://bitbucket.org/arco_group/upper/raw/tip/UDP_fork.py
[udp-SS-fork]: https://bitbucket.org/arco_group/upper/raw/tip/UDP_SS_fork.py


TCP
---

* [client] [tcp-client]
* [synchronous server] [tcp-server]
* [synchronous server with SocketServer] [tcp-SS]

* [forking server][tcp-fork]
* [forking server with SocketServer] [tcp-SS-fork]
* [forking server with Process] [tcp-process]
* [preforking server (process workers)] [tcp-worker]

* [threaded server][tcp-thread]
* [threaded server with SocketServer] [tcp-SS-thread]

* [async server with select] [tcp-select]
* [async server with asyncore] [tcp-asyncore]
* [async server with twisted] [tcp-twisted]


[tcp-client]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_client.py
[tcp-server]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_server.py
[tcp-SS]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_SS.py

[tcp-fork]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_fork.py
[tcp-SS-fork]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_SS_fork.py
[tcp-process]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_process.py
[tcp-worker]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_workers.py

[tcp-thread]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_thread.py
[tcp-SS-thread]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_SS_thread.py

[tcp-select]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_select.py
[tcp-asyncore]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_asyncore.py
[tcp-twisted]: https://bitbucket.org/arco_group/upper/raw/tip/TCP_twisted.py