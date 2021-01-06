# -*- coding: utf-8 -*-
import unittest

from openstack_loadtest import base


class testBase(unittest.TestCase):
    def test_missing_env(self):
        self.assertRaises(Exception, base.OpenStackUser)
