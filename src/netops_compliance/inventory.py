"""Reject unknown fields and duplicate YAML keys without leaking input values."""

from pathlib import Path

import yaml
from pydantic import ValidationError

from .models import Inventory, RuleSet


class InputError(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise InputError("YAML keys must be unique strings")
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_model(path: Path, model):
    try:
        if path.stat().st_size > 1_000_000:
            raise InputError("input exceeds size limit")
        return model.model_validate(
            yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
        )
    except (OSError, UnicodeError, yaml.YAMLError, ValidationError, RecursionError) as exc:
        raise InputError(f"invalid {model.__name__} file; check schema and file access") from exc


def load_inventory(path: Path) -> Inventory:
    return load_model(path, Inventory)


def load_rules(path: Path) -> RuleSet:
    return load_model(path, RuleSet)


def select_devices(inventory, names, groups, all_devices):
    if sum((bool(names), bool(groups), all_devices)) != 1:
        raise InputError("select exactly one of --device, --group, or --all")
    if set(names) - {d.name for d in inventory.devices} or set(groups) - {
        g for d in inventory.devices for g in d.groups
    }:
        raise InputError("unknown device or group selection")
    selected = [
        d
        for d in inventory.devices
        if all_devices or d.name in names or set(d.groups).intersection(groups)
    ]
    if not selected:
        raise InputError("selection is empty")
    return selected
