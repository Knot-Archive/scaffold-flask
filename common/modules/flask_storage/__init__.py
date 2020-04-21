from .filesystem import FileSystemStorage, FileSystemStorageFile
from .mock import MockStorage, MockStorageFile
from .base import (
    FileExistsError,
    FileNotFoundError,
    PermissionError,
    Storage,
    StorageException,
    StorageFile
)

__all__ = (
    FileExistsError,
    FileNotFoundError,
    FileSystemStorage,
    FileSystemStorageFile,
    MockStorage,
    MockStorageFile,
    PermissionError,
    Storage,
    StorageException,
    StorageFile,
    'STORAGE_DRIVERS',
    'get_default_storage_class',
    'get_filesystem_storage_class',
)

STORAGE_DRIVERS = {
    'filesystem': FileSystemStorage,
    'mock': MockStorage
}


def get_default_storage_class(app):
    return STORAGE_DRIVERS[app.config['DEFAULT_FILE_STORAGE']]


def get_filesystem_storage_class(app):
    if app.config['TESTING']:
        return MockStorage
    else:
        return FileSystemStorage
