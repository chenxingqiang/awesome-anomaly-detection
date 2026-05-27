"""
Driving behavior analysis and aggressive driving detection module.

This module provides tools for analyzing driving data and detecting
aggressive driving events using anomaly detection techniques.
"""

from .config import first_time, only_evaluation
from .driving_data_preprocess import apply_preprocess
from .find_aggressive_driving_event import find_event
from .parallel_aggressive_driving_detection import apply_detection

__all__ = [
    "first_time",
    "only_evaluation",
    "apply_preprocess",
    "find_event",
    "apply_detection",
]
