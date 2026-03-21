"""Data Source Connectors"""
from .base import BaseConnector, Document
from .folder_connector import FolderConnector
from .database_connector import DatabaseConnector
from .sharepoint_connector import SharePointConnector


def get_connector(source_type: str, config: dict) -> BaseConnector:
    """Factory function to get data source connector"""
    connectors = {
        "folder": FolderConnector,
        "database": DatabaseConnector,
        "sharepoint": SharePointConnector,
    }
    
    if source_type not in connectors:
        raise ValueError(f"Unknown source type: {source_type}")
    
    return connectors[source_type](config)


__all__ = [
    "BaseConnector",
    "Document",
    "FolderConnector",
    "DatabaseConnector",
    "SharePointConnector",
    "get_connector",
]
