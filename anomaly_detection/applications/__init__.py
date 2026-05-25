"""
Application-specific anomaly detection methods.

This module contains implementations of anomaly detection algorithms
tailored for specific applications such as:
- Driving behavior analysis (driving submodule)
- KPI monitoring
- Log analysis
- And more
"""

from . import driving

__all__ = ["driving"]
