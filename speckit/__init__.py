"""
Speckit - From idea to sophisticated implementation.

A comprehensive tool for solo developers to structure ideas into 
production-ready specs with planning, design, and implementation phases.
"""

__version__ = "2.0.0"
__author__ = "Speckit"

from .core import Spec, SpecBuilder
from .planning import PlanningPhase
from .design import DesignPhase
from .implementation import ImplementationPhase

__all__ = [
    "Spec",
    "SpecBuilder", 
    "PlanningPhase",
    "DesignPhase",
    "ImplementationPhase",
]
