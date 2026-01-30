"""
Embedders package - pluggable vector store backends.

Embedders are auto-discovered from this package. Any class inheriting
from BaseEmbedder is automatically registered by its store_type property.
"""

import importlib
import logging
import pkgutil
from pathlib import Path

from .base import BaseEmbedder

logger = logging.getLogger(__name__)

# Registry of store_type -> embedder class
_EMBEDDER_REGISTRY: dict[str, type[BaseEmbedder]] = {}


def _discover_embedders() -> None:
    """Auto-discover embedder classes in this package."""
    package_dir = Path(__file__).parent

    for module_info in pkgutil.iter_modules([str(package_dir)]):
        if module_info.name == "base":
            continue
        try:
            module = importlib.import_module(f".{module_info.name}", package=__name__)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type)
                        and issubclass(attr, BaseEmbedder)
                        and attr is not BaseEmbedder):
                    instance = attr.__new__(attr)
                    store_type = attr.store_type.fget(instance)
                    _EMBEDDER_REGISTRY[store_type] = attr
                    logger.info(f"Registered embedder: {store_type} -> {attr.__name__}")
        except Exception as e:
            logger.warning(f"Failed to load embedder module '{module_info.name}': {e}")

    logger.info(f"Embedder discovery complete: {len(_EMBEDDER_REGISTRY)} embedder(s) registered "
                f"({list(_EMBEDDER_REGISTRY.keys())})")


def get_embedder_class(store_type: str) -> type[BaseEmbedder]:
    """Get an embedder class by store type."""
    if not _EMBEDDER_REGISTRY:
        _discover_embedders()
    if store_type not in _EMBEDDER_REGISTRY:
        raise ValueError(
            f"Unknown store type: {store_type}. "
            f"Available: {list(_EMBEDDER_REGISTRY.keys())}"
        )
    return _EMBEDDER_REGISTRY[store_type]


def supported_stores() -> list[str]:
    """Return list of supported store types."""
    if not _EMBEDDER_REGISTRY:
        _discover_embedders()
    return list(_EMBEDDER_REGISTRY.keys())


_discover_embedders()
