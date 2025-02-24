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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from scaleapi.api_client.v2.models.task import Task
from typing import Optional, Set
from typing_extensions import Self

class GetTasksResponse(BaseModel):
    """
    GetTasksResponse
    """ # noqa: E501
    tasks: List[Task] = Field(description="Array of task objects")
    next_token: Optional[StrictStr] = Field(default=None, description="A token used to retrieve the next page of results if there are more. You can find the `next_token` in your last request")
    __properties: ClassVar[List[str]] = ["tasks", "next_token"]

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
        """Create an instance of GetTasksResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in tasks (list)
        _items = []
        if self.tasks:
            for _item_tasks in self.tasks:
                if _item_tasks:
                    _items.append(_item_tasks.to_dict())
            _dict['tasks'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetTasksResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "tasks": [Task.from_dict(_item) for _item in obj["tasks"]] if obj.get("tasks") is not None else None,
            "next_token": obj.get("next_token")
        })
        return _obj
