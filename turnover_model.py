"""Utilities for turnover model operations.

This module exposes :func:`employee_data.load_employee_data` under the local
namespace to avoid duplicating logic while retaining a backward-compatible
API.
"""
from __future__ import annotations

from employee_data import load_employee_data

__all__ = ["load_employee_data"]
