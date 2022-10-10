from config.default import DefaultSettings
from config.get_settings import get_settings

settings = get_settings()


__all__ = [
    'DefaultSettings',
    'settings',
]
