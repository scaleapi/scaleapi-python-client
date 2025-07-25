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
    BOOLEAN = 'boolean'
    TEXT = 'text'
    CATEGORY = 'category'
    CATEGORY_MULTIPLE = 'category_multiple'
    FILE = 'file'
    WORKSPACE_CONTAINER = 'workspace_container'
    RANKED_CHOICES = 'ranked_choices'
    RANKED_GROUPS = 'ranked_groups'
    RUBRIC_CRITERIA = 'rubric_criteria'
    RUBRIC_RATING = 'rubric_rating'
    LABELED_TEXT = 'labeled_text'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of AnnotationType from a JSON string"""
        return cls(json.loads(json_str))
