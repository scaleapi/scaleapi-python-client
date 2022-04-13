from scaleapi.quality_tasks import QualityTask


class TrainingTask(QualityTask):
    """TrainingTask class, containing TrainingTask information."""

    def __str__(self):
        return f"TrainingTask(id={self.id})"

    def __repr__(self):
        return f"TrainingTask({self._json})"
