"""
Patch to allow Django 4.2 to work with PostgreSQL 10.
PostgreSQL 10 doesn't have all features of 12+,
but for development this is acceptable.
"""

def _patched_check(self):
    """Skip the PostgreSQL version check for development."""
    pass


def apply_patch():
    """Apply the PostgreSQL version compatibility patch."""
    try:
        from django.db.backends.base.base import BaseDatabaseWrapper
        original = BaseDatabaseWrapper.check_database_version_supported
        BaseDatabaseWrapper.check_database_version_supported = _patched_check
    except (ImportError, AttributeError):
        pass


apply_patch()
