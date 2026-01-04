from pathlib import Path

import numpy as np
from pydantic import BaseModel, ConfigDict, field_validator
from PySide6.QtCore import QPoint


class Object(BaseModel):
    """Model to describe annotated images.

    Attributes
    ----------
    image_path : Path to image being annotated.
    annotated_objects : List of drawn objects.

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    imagePath: str
    annotatedObjects: list[QPoint] = []

    @field_validator("imagePath")
    @classmethod
    def validate_image_exists(cls, v):
        if not Path(v).exists():
            raise ValueError(f"Image not found: {v}")
        return v

    def save(self, filePath: str):
        """Save annotated objects to .npy"""
        np.save(filePath, self.annotatedObjects, allow_pickle=True)
