#!/usr/bin/python3
"""Define initialization method for BaseModels"""

from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
