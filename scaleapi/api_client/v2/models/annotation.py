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
import pprint
from typing import Any, Dict, Optional, Set, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationError,
    field_validator,
)
from typing_extensions import Literal, Self

ANNOTATION_ONE_OF_SCHEMAS = [
    "AnnotationBoolean",
    "AnnotationCategory",
    "AnnotationCategoryMultiple",
    "AnnotationFile",
    "AnnotationInteger",
    "AnnotationLabeledText",
    "AnnotationRankedChoices",
    "AnnotationRankedGroups",
    "AnnotationRubricCriteria",
    "AnnotationRubricRating",
    "AnnotationText",
    "AnnotationWorkspaceContainer",
]


class Annotation(BaseModel):
    """
    Represents a generic annotation.
    """

    # data type: AnnotationBoolean
    oneof_schema_1_validator: Optional[AnnotationBoolean] = None
    # data type: AnnotationInteger
    oneof_schema_2_validator: Optional[AnnotationInteger] = None
    # data type: AnnotationText
    oneof_schema_3_validator: Optional[AnnotationText] = None
    # data type: AnnotationCategory
    oneof_schema_4_validator: Optional[AnnotationCategory] = None
    # data type: AnnotationCategoryMultiple
    oneof_schema_5_validator: Optional[AnnotationCategoryMultiple] = None
    # data type: AnnotationFile
    oneof_schema_6_validator: Optional[AnnotationFile] = None
    # data type: AnnotationLabeledText
    oneof_schema_7_validator: Optional[AnnotationLabeledText] = None
    # data type: AnnotationRankedChoices
    oneof_schema_8_validator: Optional[AnnotationRankedChoices] = None
    # data type: AnnotationRankedGroups
    oneof_schema_9_validator: Optional[AnnotationRankedGroups] = None
    # data type: AnnotationRubricCriteria
    oneof_schema_10_validator: Optional[AnnotationRubricCriteria] = None
    # data type: AnnotationRubricRating
    oneof_schema_11_validator: Optional[AnnotationRubricRating] = None
    # data type: AnnotationWorkspaceContainer
    oneof_schema_12_validator: Optional[AnnotationWorkspaceContainer] = None
    actual_instance: Optional[
        Union[
            AnnotationBoolean,
            AnnotationCategory,
            AnnotationCategoryMultiple,
            AnnotationFile,
            AnnotationInteger,
            AnnotationLabeledText,
            AnnotationRankedChoices,
            AnnotationRankedGroups,
            AnnotationRubricCriteria,
            AnnotationRubricRating,
            AnnotationText,
            AnnotationWorkspaceContainer,
        ]
    ] = None
    one_of_schemas: Set[str] = {
        "AnnotationBoolean",
        "AnnotationCategory",
        "AnnotationCategoryMultiple",
        "AnnotationFile",
        "AnnotationInteger",
        "AnnotationLabeledText",
        "AnnotationRankedChoices",
        "AnnotationRankedGroups",
        "AnnotationRubricCriteria",
        "AnnotationRubricRating",
        "AnnotationText",
        "AnnotationWorkspaceContainer",
    }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )

    discriminator_value_class_map: Dict[str, Any] = {}

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError(
                    "If a position argument is used, only 1 is allowed to set `actual_instance`"
                )
            if kwargs:
                raise ValueError(
                    "If a position argument is used, keyword arguments cannot be used."
                )
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator("actual_instance")
    def actual_instance_must_validate_oneof(cls, v):
        instance = Annotation.model_construct()
        error_messages = []
        match = 0
        # validate data type: AnnotationBoolean
        if not isinstance(v, AnnotationBoolean):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationBoolean`"
            )
        else:
            match += 1
        # validate data type: AnnotationInteger
        if not isinstance(v, AnnotationInteger):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationInteger`"
            )
        else:
            match += 1
        # validate data type: AnnotationText
        if not isinstance(v, AnnotationText):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationText`"
            )
        else:
            match += 1
        # validate data type: AnnotationCategory
        if not isinstance(v, AnnotationCategory):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationCategory`"
            )
        else:
            match += 1
        # validate data type: AnnotationCategoryMultiple
        if not isinstance(v, AnnotationCategoryMultiple):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationCategoryMultiple`"
            )
        else:
            match += 1
        # validate data type: AnnotationFile
        if not isinstance(v, AnnotationFile):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationFile`"
            )
        else:
            match += 1
        # validate data type: AnnotationLabeledText
        if not isinstance(v, AnnotationLabeledText):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationLabeledText`"
            )
        else:
            match += 1
        # validate data type: AnnotationRankedChoices
        if not isinstance(v, AnnotationRankedChoices):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationRankedChoices`"
            )
        else:
            match += 1
        # validate data type: AnnotationRankedGroups
        if not isinstance(v, AnnotationRankedGroups):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationRankedGroups`"
            )
        else:
            match += 1
        # validate data type: AnnotationRubricCriteria
        if not isinstance(v, AnnotationRubricCriteria):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationRubricCriteria`"
            )
        else:
            match += 1
        # validate data type: AnnotationRubricRating
        if not isinstance(v, AnnotationRubricRating):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationRubricRating`"
            )
        else:
            match += 1
        # validate data type: AnnotationWorkspaceContainer
        if not isinstance(v, AnnotationWorkspaceContainer):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `AnnotationWorkspaceContainer`"
            )
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when setting `actual_instance` in Annotation with oneOf schemas: AnnotationCategory, AnnotationCategoryMultiple, AnnotationInteger, AnnotationText. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when setting `actual_instance` in Annotation with oneOf schemas: AnnotationCategory, AnnotationCategoryMultiple, AnnotationInteger, AnnotationText. Details: "
                + ", ".join(error_messages)
            )
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []

        data = json.loads(json_str) if isinstance(json_str, str) else json_str
        annotation_type = data.get("type") if isinstance(data, dict) else None

        # https://github.com/swagger-api/swagger-codegen/issues/10962
        try:
            if annotation_type == "boolean":
                instance.actual_instance = AnnotationBoolean.from_json(json_str)
                return instance
            elif annotation_type == "integer":
                instance.actual_instance = AnnotationInteger.from_json(json_str)
                return instance
            elif annotation_type == "text":
                instance.actual_instance = AnnotationText.from_json(json_str)
                return instance
            elif annotation_type == "category":
                instance.actual_instance = AnnotationCategory.from_json(json_str)
                return instance
            elif annotation_type == "category_multiple":
                instance.actual_instance = AnnotationCategoryMultiple.from_json(
                    json_str
                )
                return instance
            elif annotation_type == "file":
                instance.actual_instance = AnnotationFile.from_json(json_str)
                return instance
            elif annotation_type == "labeled_text":
                instance.actual_instance = AnnotationLabeledText.from_json(json_str)
                return instance
            elif annotation_type == "ranked_choices":
                instance.actual_instance = AnnotationRankedChoices.from_json(json_str)
                return instance
            elif annotation_type == "ranked_groups":
                instance.actual_instance = AnnotationRankedGroups.from_json(json_str)
                return instance
            elif annotation_type == "rubric_criteria":
                instance.actual_instance = AnnotationRubricCriteria.from_json(json_str)
                return instance
            elif annotation_type == "rubric_rating":
                instance.actual_instance = AnnotationRubricRating.from_json(json_str)
                return instance
            elif annotation_type == "workspace_container":
                instance.actual_instance = AnnotationWorkspaceContainer.from_json(
                    json_str
                )
                return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
            raise ValueError(
                "Can't discriminate annotation_type. Details: "
                + ", ".join(error_messages)
            )

        match = 0

        # deserialize data into AnnotationBoolean
        try:
            instance.actual_instance = AnnotationBoolean.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationInteger
        try:
            instance.actual_instance = AnnotationInteger.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationText
        try:
            instance.actual_instance = AnnotationText.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationCategory
        try:
            instance.actual_instance = AnnotationCategory.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationCategoryMultiple
        try:
            instance.actual_instance = AnnotationCategoryMultiple.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationFile
        try:
            instance.actual_instance = AnnotationFile.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationLabeledText
        try:
            instance.actual_instance = AnnotationLabeledText.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationRankedChoices
        try:
            instance.actual_instance = AnnotationRankedChoices.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationRankedGroups
        try:
            instance.actual_instance = AnnotationRankedGroups.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationRubricCriteria
        try:
            instance.actual_instance = AnnotationRubricCriteria.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationRubricRating
        try:
            instance.actual_instance = AnnotationRubricRating.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AnnotationWorkspaceContainer
        try:
            instance.actual_instance = AnnotationWorkspaceContainer.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when deserializing the JSON string into Annotation with oneOf schemas: AnnotationCategory, AnnotationCategoryMultiple, AnnotationInteger, AnnotationText. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into Annotation with oneOf schemas: AnnotationCategory, AnnotationCategoryMultiple, AnnotationInteger, AnnotationText. Details: "
                + ", ".join(error_messages)
            )
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(
            self.actual_instance.to_json
        ):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(
        self,
    ) -> Optional[
        Union[
            Dict[str, Any],
            AnnotationBoolean,
            AnnotationCategory,
            AnnotationCategoryMultiple,
            AnnotationFile,
            AnnotationInteger,
            AnnotationLabeledText,
            AnnotationRankedChoices,
            AnnotationRankedGroups,
            AnnotationRubricCriteria,
            AnnotationRubricRating,
            AnnotationText,
            AnnotationWorkspaceContainer,
        ]
    ]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(
            self.actual_instance.to_dict
        ):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


from scaleapi.api_client.v2.models.annotation_boolean import AnnotationBoolean
from scaleapi.api_client.v2.models.annotation_category import AnnotationCategory
from scaleapi.api_client.v2.models.annotation_category_multiple import (
    AnnotationCategoryMultiple,
)
from scaleapi.api_client.v2.models.annotation_file import AnnotationFile
from scaleapi.api_client.v2.models.annotation_integer import AnnotationInteger
from scaleapi.api_client.v2.models.annotation_labeled_text import AnnotationLabeledText
from scaleapi.api_client.v2.models.annotation_ranked_choices import (
    AnnotationRankedChoices,
)
from scaleapi.api_client.v2.models.annotation_ranked_groups import (
    AnnotationRankedGroups,
)
from scaleapi.api_client.v2.models.annotation_rubric_criteria import AnnotationRubricCriteria
from scaleapi.api_client.v2.models.annotation_rubric_rating import AnnotationRubricRating
from scaleapi.api_client.v2.models.annotation_text import AnnotationText
from scaleapi.api_client.v2.models.annotation_workspace_container import (
    AnnotationWorkspaceContainer,
)

# TODO: Rewrite to not use raise_errors
Annotation.model_rebuild(raise_errors=False)
