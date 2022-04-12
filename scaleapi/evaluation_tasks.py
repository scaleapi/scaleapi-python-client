from scaleapi.quality_tasks import QualityTask


class EvaluationTask(QualityTask):
    """EvaluationTask class, containing EvaluationTask information."""

    def __str__(self):
        return f"EvaluationTask(id={self.id})"

    def __repr__(self):
        return f"EvaluationTask({self._json})"
