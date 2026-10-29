"""Sequential offline collection: failures are isolated and never echo exception text."""

import hashlib
from pathlib import Path

from .adapters import get_adapter
from .adapters.base import ParseError
from .models import Collection

SCENARIOS = ("compliant", "noncompliant", "malformed")


def collect_device(device, fixture_dir: Path, scenario: str, operation="audit"):
    result = Collection(device=device.name, platform=device.platform)
    if operation not in device.allowed_operations or "collect" not in device.allowed_operations:
        result.error = "operation_not_allowed"
        return result
    try:
        if scenario not in SCENARIOS:
            raise ValueError("unsupported fixture scenario")
        path = fixture_dir / device.platform / f"{scenario}.cfg"
        if path.stat().st_size > 1_000_000:
            raise ParseError("fixture too large")
        raw = path.read_bytes()
        result.baseline_hash = hashlib.sha256(raw).hexdigest()
        result.facts = get_adapter(device.platform).normalize(raw.decode("utf-8"))
    except (OSError, UnicodeError):
        result.error = "fixture_read_error"
    except ParseError:
        result.error = "fixture_parse_error"
    except Exception:
        # Exceptions from future adapters must not expose raw output or credentials.
        result.error = "collection_error"
    return result


def collect(devices, fixture_dir, scenario="compliant", operation="audit"):
    return [collect_device(d, fixture_dir, scenario, operation) for d in devices]
