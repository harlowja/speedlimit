# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import math
import time

from monotonic import monotonic as _now


class SpeedLimit(object):
    """Speed/limiting iterator wrapper object.

    A wrapper object that uses the `token bucket`_ algorithm to limit the
    rate at which values comes out of an iterable. This can be used to limit
    the consumption speed of iteration of some other iterator (or iterable).

    .. _token bucket: http://en.wikipedia.org/wiki/Token_bucket
    """
    def __init__(self,
                 # How many items to yield from the provided
                 # wrapped iterator (per second).
                 items_per_second,
                 # Used to simulate a thread with its own 'tic rate'. Making
                 # this smaller affects the accuracy of the 'tic' calculation,
                 # which affects the accuracy of consumption (and delays).
                 refresh_rate_seconds=0.01,
                 # How *full* the initial bucket is.
                 initial_bucket_size=1,
                 # Made a keyword argument, so one could replace this
                 # with a eventlet.sleep or other idling function...
                 sleep_func=time.sleep):
        self._refresh_rate_seconds = refresh_rate_seconds
        self._bucket = (items_per_second *
                        refresh_rate_seconds * initial_bucket_size)
        self._items_per_tic = items_per_second * refresh_rate_seconds
        self._next_fill = _now() + refresh_rate_seconds
        self._sleep = sleep_func

    def _check_fill(self):
        # Fill the bucket based on elapsed time.
        #
        # This simulates a background thread...
        now = _now()
        if now > self._next_fill:
            d = now - self._next_fill
            tics = int(math.ceil(d / self._refresh_rate_seconds))
            self._bucket += tics * self._items_per_tic
            self._next_fill += tics * self._refresh_rate_seconds

    def speed_limit_iter(self, itr, chunk_size_cb=None):
        """Return an iterator/generator which limits after each iteration.

        :param itr: an iterator to wrap
        :param chunk_size_cb: a function that can calculate the
                              size of each chunk (if none provided this
                              defaults to 1)
        """
        for chunk in itr:
            if chunk_size_cb is None:
                sz = 1
            else:
                sz = chunk_size_cb(chunk)
            self._check_fill()
            if sz > self._bucket:
                now = _now()
                tics = int((sz - self._bucket) / self._items_per_tic)
                tm_diff = self._next_fill - now
                secs = tics * self._refresh_rate_seconds
                if tm_diff > 0:
                    secs += tm_diff
                self._sleep(secs)
                self._check_fill()
            self._bucket -= sz
            yield chunk
