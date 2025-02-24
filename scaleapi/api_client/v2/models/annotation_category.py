# coding: utf-8

"""
    GenAI API Spec

    Data Engine: Generative AI API Specification

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class AnnotationCategory(BaseModel):
    """
    AnnotationCategory
    """ # noqa: E501
    id: StrictStr = Field(description="Unique identifier for an annotation.")
    key: StrictStr = Field(description="Key for the annotation.")
    type: StrictStr = Field(description="The type of the value and the possible_values, if they exist.")
    title: Optional[StrictStr] = Field(default=None, description="Title of the annotation.")
    description: Optional[StrictStr] = Field(default=None, description="Further details about the question.")
    labels: Optional[List[StrictStr]] = Field(default=None, description="String representation of the possible options.")
    not_applicable: Optional[StrictBool] = Field(default=None, description="This is set when the annotation is not applicable in the context.")
    cannot_assess: Optional[StrictBool] = Field(default=None, description="This is set when the annotation cannot be assessed in the context.")
    metadata: Optional[AnnotationMetadata] = None
    value: Optional[StrictStr] = Field(default=None, description="Single-select category annotation.")
    possible_values: Optional[List[StrictStr]] = Field(default=None, description="The possible values for this annotation.")
    __properties: ClassVar[List[str]] = ["id", "key", "type", "title", "description", "labels", "not_applicable", "cannot_assess", "metadata", "value", "possible_values"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        excluded_fields: Set[str] = set([
        ])
        return self.model_dump_json(by_alias=True, exclude_unset=True, exclude=excluded_fields)

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of AnnotationCategory from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of metadata
        if self.metadata:
            _dict['metadata'] = self.metadata.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AnnotationCategory from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "key": obj.get("key"),
            "type": obj.get("type"),
            "title": obj.get("title"),
            "description": obj.get("description"),
            "labels": obj.get("labels"),
            "not_applicable": obj.get("not_applicable"),
            "cannot_assess": obj.get("cannot_assess"),
            "metadata": AnnotationMetadata.from_dict(obj["metadata"]) if obj.get("metadata") is not None else None,
            "value": obj.get("value"),
            "possible_values": obj.get("possible_values")
        })
        return _obj

from scaleapi.api_client.v2.models.annotation_metadata import AnnotationMetadata
# TODO: Rewrite to not use raise_errors
AnnotationCategory.model_rebuild(raise_errors=False)
