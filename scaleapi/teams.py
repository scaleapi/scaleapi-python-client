from enum import Enum


class TeammateRole(Enum):
    """Teammate Roles Enum"""

    Labeler = "labeler"
    Member = "member"
    Manager = "manager"
    Admin = "admin"


class Teammate:
    """Teammate class, containing teammate information."""

    def __init__(self, json, client):
        self._json = json
        self.email: str = json["email"]
        self.role = json["role"]
        self._client = client
        # fill in rest here (non-optional fields)
        self.company = json.get("company")
        self.first_name = json.get("firstName")
        self.last_name = json.get("lastName")
        self.is_studio_labeler = json.get("isStudioLabeler")
        self.expiry = json.get("expiry")

    def __hash__(self):
        return hash(self.email)

    def __str__(self):
        return f"Teammate(email={self.email})"

    def __repr__(self):
        return f"Teammate({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json

    def update_teammate_role(self, new_role: TeammateRole):
        """Updates teammate role"""
        return self._client.update_teammates_role([self.email], new_role)
