# -*- coding: utf-8 -*-

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

import string

import speedlimit

from testtools import testcase


class TestLimits(testcase.TestCase):

    def test_alphabet(self):
        limiter = speedlimit.SpeedLimit(26)
        it = iter(string.ascii_lowercase)
        letters = []
        for alpha in limiter.speed_limit_iter(it):
            letters.append(alpha)
        letters = "".join(letters)
        self.assertEqual(string.ascii_lowercase, letters)
