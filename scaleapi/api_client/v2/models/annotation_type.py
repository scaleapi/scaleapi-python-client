# coding: utf-8

"""
    GenAI API Spec

    Data Engine: Generative AI API Specification

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class AnnotationType(str, Enum):
    """
    AnnotationType
    """

    """
    allowed enum values
    """
    INTEGER = 'integer'
    TEXT = 'text'
    CATEGORY = 'category'
    CATEGORY_MULTIPLE = 'category_multiple'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of AnnotationType from a JSON string"""
        return cls(json.loads(json_str))
