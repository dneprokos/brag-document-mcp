"""
Brag Document MCP Server

A Model Context Protocol (MCP) server built with FastMCP that helps create,
manage, and sync yearly Brag Documents in DOCX format.
"""

import shutil
import json
from typing import Optional

from fastmcp import FastMCP

from document_utils import (
    get_document_path,
    get_index_path,
    get_template_path,
    ensure_index_file,
)

# Initialize FastMCP server
mcp = FastMCP("Brag Document MCP")


@mcp.tool()
def create_brag_document(
    full_name: str,
    year: int,
    workspace_root: Optional[str] = None
) -> str:
    """Create a brag document for a person and year.
    
    Creates a new brag document from the template for the specified person and year.
    The document is created in DOCX format with all standard sections (Goals, Projects, 
    Collaboration & mentorship, Documentation, What you learned, Outside of work, etc.).
    If the document already exists, returns the existing document path without overwriting.
    Also creates an index JSON file for tracking document entries and sections.
    
    Use this tool when the user asks to create, make, set up, or ensure a brag document exists.
    
    Args:
        full_name: Full name of the person (e.g., "John Doe", "Kostiantyn Teltov")
        year: Year for the brag document (e.g., 2024, 2026)
        workspace_root: Optional root directory for documents (defaults to current working directory)
    
    Returns:
        JSON string with status (created or exists), document_path, and index_path
    """
    try:
        # Get paths
        doc_path = get_document_path(full_name, year, workspace_root)
        index_path = get_index_path(full_name, year, workspace_root)
        
        # Check if document already exists
        if doc_path.exists():
            # Ensure index exists even if document exists
            ensure_index_file(index_path)
            
            return json.dumps({
                "status": "exists",
                "document_path": str(doc_path),
                "index_path": str(index_path)
            }, indent=2)
        
        # Document doesn't exist - create it
        # Get template path
        template_path = get_template_path(workspace_root)
        
        if not template_path.exists():
            return json.dumps({
                "error": f"Template not found at {template_path}. Please ensure the template exists."
            }, indent=2)
        
        # Create parent directories
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy template to create new document
        shutil.copy2(template_path, doc_path)
        
        # Create index file
        ensure_index_file(index_path)
        
        return json.dumps({
            "status": "created",
            "document_path": str(doc_path),
            "index_path": str(index_path)
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to ensure document: {str(e)}"
        }, indent=2)


if __name__ == "__main__":
    # Run the server
    mcp.run()
