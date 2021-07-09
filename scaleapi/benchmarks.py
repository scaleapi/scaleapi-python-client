class Benchmark:
    """Benchmark class, containing Benchmark information."""

    def __init__(self, json, client):
        self._json = json
        self.id = json["benchmark_id"]
        self.initial_response = getattr(json, "initial_response", None)
        self.expected_response = json["expected_response"]
        self._client = client

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"Benchmark(id={self.id})"

    def __repr__(self):
        return f"Benchmark({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json
