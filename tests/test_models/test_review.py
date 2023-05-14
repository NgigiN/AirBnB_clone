#!/usr/bin/python3
""" test module for the review module & class"""

from tests.test_models.test_base_model import test_basemodel
from models.review import Review


class test_review(test_basemodel):
    """Test class for the review module"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """ test fo the id"""
        new = self.value()
        self.assertEqual(type(new.place_id), str)

    def test_user_id(self):
        """ test for the user id"""
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """ test for the text"""
        new = self.value()
        self.assertEqual(type(new.text), str)
