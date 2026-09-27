"""GISGPT: VFM-native spatial foundation model research utilities."""

from .vfm_schema import VFMManifest, load_manifest
from .validator import ValidationReport, validate_manifest

__all__ = ["VFMManifest", "ValidationReport", "load_manifest", "validate_manifest"]
__version__ = "0.1.0"
