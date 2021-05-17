class File:
    """File class, containing File information."""

    def __init__(self, json, client):
        self._json = json
        self.id = json["id"]
        self.attachment_url = json["attachment_url"]
        self._client = client

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"File(id={self.id})"

    def __repr__(self):
        return f"File({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json
