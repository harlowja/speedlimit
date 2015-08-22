===========
Speed limit
===========

Speed limit utilities that use the `token bucket`_ algorithm internally.

An example::

    >>> import string
    >>> import time
    >>>
    >>> import speedlimit
    >>>
    >>> police = speedlimit.SpeedLimit(1)
    >>>
    >>> it = iter(string.ascii_lowercase)
    >>> t_zero = time.time()
    >>>
    >>> for alpha in police.speed_limit_iter(it):
    ...     print("Got %s at %0.2f" % (alpha,  time.time() - t_zero))
    ...
    Got a at 1.00
    Got b at 2.00
    Got c at 3.00
    Got d at 4.00
    Got e at 5.00
    Got f at 6.00
    Got g at 7.00
    Got h at 8.00
    Got i at 9.00
    Got j at 10.00
    Got k at 11.00
    Got l at 12.00
    Got m at 13.00
    Got n at 14.00
    Got o at 15.00
    Got p at 16.00
    Got q at 17.00
    Got r at 18.00
    Got s at 19.00
    Got t at 20.00
    Got u at 21.00
    Got v at 22.00
    Got w at 23.00
    Got x at 24.00
    Got y at 25.00
    Got z at 26.00

.. _token bucket: http://en.wikipedia.org/wiki/Token_bucket
