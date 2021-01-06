# -*- coding: utf-8 -*-
import unittest

import pytest
from unittest import mock

from openstack_loadtest import base


class testBase(unittest.TestCase):

    def test_missing_env(self):
        self.assertRaises(Exception, base.OpenStackUser)
