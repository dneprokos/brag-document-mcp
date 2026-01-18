"""
Document utilities for Brag Document MCP.

This module contains helper functions for managing brag documents,
including path resolution, index file management, and document operations.
"""

import os
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

# Constants
DEFAULT_WORKSPACE_ROOT = os.getcwd()
TEMPLATE_PATH = Path("Templates") / "A brag document template.docx"
BRAG_DOCUMENTS_DIR = "BragDocuments"


def get_workspace_root(workspace_root: Optional[str] = None) -> Path:
    """Get the workspace root path.
    
    Args:
        workspace_root: Optional custom workspace root. If None, uses default.
    
    Returns:
        Path object representing the workspace root.
    """
    return Path(workspace_root) if workspace_root else Path(DEFAULT_WORKSPACE_ROOT)


def get_document_path(
    full_name: str,
    year: int,
    workspace_root: Optional[str] = None
) -> Path:
    """Get the path to the brag document.
    
    Args:
        full_name: Full name of the person (e.g., "John Doe")
        year: Year for the brag document (e.g., 2024)
        workspace_root: Optional root directory for documents.
    
    Returns:
        Path to the brag document file.
    """
    root = get_workspace_root(workspace_root)
    return root / BRAG_DOCUMENTS_DIR / full_name / f"Brag Document - {full_name} ({year}).docx"


def get_index_path(
    full_name: str,
    year: int,
    workspace_root: Optional[str] = None
) -> Path:
    """Get the path to the index JSON file.
    
    Args:
        full_name: Full name of the person (e.g., "John Doe")
        year: Year for the brag document (e.g., 2024)
        workspace_root: Optional root directory for documents.
    
    Returns:
        Path to the index JSON file.
    """
    root = get_workspace_root(workspace_root)
    return (
        root
        / BRAG_DOCUMENTS_DIR
        / full_name
        / ".index"
        / f"Brag Document - {full_name} ({year}).json"
    )


def get_template_path(workspace_root: Optional[str] = None) -> Path:
    """Get the path to the template document.
    
    Args:
        workspace_root: Optional root directory for documents.
    
    Returns:
        Path to the template document.
    """
    root = get_workspace_root(workspace_root)
    return root / TEMPLATE_PATH


def ensure_index_file(index_path: Path) -> None:
    """Create index file if it doesn't exist.
    
    Initializes the index file with an empty structure for tracking
    document sections and entries.
    
    Args:
        index_path: Path where the index file should be created.
    
    Raises:
        OSError: If the file cannot be created or written.
    """
    index_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not index_path.exists():
        # Initialize with empty structure
        index_data = {
            "document_name": index_path.stem,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "sections": {},
            "entries": {}
        }
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
