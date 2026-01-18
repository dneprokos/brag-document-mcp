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
    generate_entry_id,
    load_index,
    add_entry_to_document,
    add_entry_to_index,
    update_entry_to_document,
    update_entry_to_index,
    find_entry_by_text,
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
        try:
            shutil.copy2(template_path, doc_path)
        except Exception as e:
            return json.dumps({
                "error": f"Failed to copy template: {str(e)}"
            }, indent=2)
        
        # Verify document was created
        if not doc_path.exists():
            return json.dumps({
                "error": f"Failed to create document at {doc_path}."
            }, indent=2)
        
        # Initialize document: replace placeholders and remove examples
        # Do this in a way that doesn't risk corrupting the file
        try:
            from document_utils import initialize_document_from_template
            # Create a backup before initialization
            backup_path = doc_path.with_suffix('.backup.docx')
            shutil.copy2(doc_path, backup_path)
            try:
                initialize_document_from_template(doc_path, full_name, year)
                # Remove backup if initialization succeeded
                if backup_path.exists():
                    backup_path.unlink()
            except Exception:
                # If initialization fails, restore from backup
                if backup_path.exists():
                    shutil.copy2(backup_path, doc_path)
                    backup_path.unlink()
        except Exception:
            # If initialization fails completely, document still exists from copy
            pass
        
        # Final verification
        if not doc_path.exists():
            return json.dumps({
                "error": f"Document was lost during initialization at {doc_path}."
            }, indent=2)
        
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


@mcp.tool()
def add_entry(
    full_name: str,
    year: int,
    section_path: str,
    text: str,
    position: Optional[int] = None,
    workspace_root: Optional[str] = None
) -> str:
    """Add a new entry to a specified section in the brag document.
    
    Adds a new entry (bullet point) to the specified section in the brag document.
    The entry is appended by default, or inserted at a specific position if provided.
    A unique entry ID is generated and stored in the index file for future reference.
    
    Use this tool when the user asks to add an entry, bullet point, or item to a section.
    
    Args:
        full_name: Full name of the person (e.g., "John Doe")
        year: Year for the brag document (e.g., 2024)
        section_path: Section to add the entry to (e.g., "Projects", "Outside of work/Articles")
        text: Text content of the entry
        position: Optional position to insert the entry (0-based, None appends at end)
        workspace_root: Optional root directory for documents (defaults to current working directory)
    
    Returns:
        JSON string with entry_id, section_path, and text
    """
    try:
        # Get paths
        doc_path = get_document_path(full_name, year, workspace_root)
        index_path = get_index_path(full_name, year, workspace_root)
        
        # Check if document exists
        if not doc_path.exists():
            return json.dumps({
                "error": f"Document not found for {full_name}, year {year} at {doc_path}.",
                "message": "Please create the document first using create_brag_document tool.",
                "suggestion": f"Create document for {full_name}, {year} before adding entries."
            }, indent=2)
        
        # Ensure index exists
        ensure_index_file(index_path)
        
        # Generate entry ID
        entry_id = generate_entry_id()
        
        # Add entry to document
        paragraph_index = add_entry_to_document(
            doc_path,
            section_path,
            text,
            position
        )
        
        # Add entry to index
        add_entry_to_index(
            index_path,
            entry_id,
            section_path,
            text,
            paragraph_index
        )
        
        return json.dumps({
            "entry_id": entry_id,
            "section_path": section_path,
            "text": text,
            "position": paragraph_index
        }, indent=2)
        
    except ValueError as e:
        return json.dumps({
            "error": str(e)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "error": f"Failed to add entry: {str(e)}"
        }, indent=2)


@mcp.tool()
def update_entry(
    full_name: str,
    year: int,
    new_text: str,
    entry_id: Optional[str] = None,
    old_text: Optional[str] = None,
    section_path: Optional[str] = None,
    occurrence_index: int = 0,
    workspace_root: Optional[str] = None
) -> str:
    """Update an existing entry in the brag document.
    
    Updates the text content of an existing entry. You can identify the entry in two ways:
    1. By entry_id (preferred): Provide the unique entry_id
    2. By text and section (fallback): Provide old_text and section_path
    
    The entry must exist in the document and index file.
    
    Use this tool when the user asks to update, modify, or change an existing entry.
    
    Args:
        full_name: Full name of the person (e.g., "John Doe")
        year: Year for the brag document (e.g., 2024)
        new_text: New text content for the entry
        entry_id: (Optional) Unique identifier of the entry to update (preferred method)
        old_text: (Optional) Current text content of the entry (used with section_path)
        section_path: (Optional) Section path where the entry is located (used with old_text)
        occurrence_index: (Optional) Which occurrence to update if multiple matches (0-based, default 0)
        workspace_root: Optional root directory for documents (defaults to current working directory)
    
    Returns:
        JSON string with entry_id, section_path, text, and updated_at timestamp
    """
    try:
        # Get paths
        doc_path = get_document_path(full_name, year, workspace_root)
        index_path = get_index_path(full_name, year, workspace_root)
        
        # Check if document exists
        if not doc_path.exists():
            return json.dumps({
                "error": f"Document not found for {full_name}, year {year} at {doc_path}.",
                "message": "Please create the document first using create_brag_document tool."
            }, indent=2)
        
        # Check if index exists
        if not index_path.exists():
            return json.dumps({
                "error": f"Index file not found for {full_name}, year {year}.",
                "message": "The document may not have any entries yet. Please add an entry first."
            }, indent=2)
        
        # Determine which method to use for finding the entry
        if entry_id:
            # Method 1: Update by entry_id (preferred)
            resolved_entry_id = entry_id
        elif old_text and section_path:
            # Method 2: Find entry by text and section (fallback)
            try:
                resolved_entry_id = find_entry_by_text(
                    index_path,
                    old_text,
                    section_path,
                    occurrence_index
                )
                if resolved_entry_id is None:
                    return json.dumps({
                        "error": f"Entry not found with text '{old_text}' in section '{section_path}'.",
                        "message": "Please verify the text and section path are correct."
                    }, indent=2)
            except ValueError as e:
                return json.dumps({
                    "error": str(e),
                    "message": "Try specifying a different occurrence_index or use entry_id instead."
                }, indent=2)
        else:
            return json.dumps({
                "error": "Either entry_id or (old_text + section_path) must be provided.",
                "message": "Provide entry_id for direct lookup, or old_text and section_path for text-based search."
            }, indent=2)
        
        # Load index to get entry information
        index_data = load_index(index_path)
        
        # Check if entry exists
        if resolved_entry_id not in index_data["entries"]:
            return json.dumps({
                "error": f"Entry with ID '{resolved_entry_id}' not found.",
                "message": "The entry may have been deleted or the identifier is incorrect."
            }, indent=2)
        
        # Get entry data
        entry_data = index_data["entries"][resolved_entry_id]
        paragraph_index = entry_data["paragraph_index"]
        entry_section_path = entry_data["section_path"]
        
        # Update entry in document
        update_entry_to_document(
            doc_path,
            paragraph_index,
            new_text
        )
        
        # Update entry in index
        update_entry_to_index(
            index_path,
            resolved_entry_id,
            new_text
        )
        
        # Reload to get updated timestamp
        updated_index_data = load_index(index_path)
        updated_entry = updated_index_data["entries"][resolved_entry_id]
        
        return json.dumps({
            "entry_id": resolved_entry_id,
            "section_path": entry_section_path,
            "text": new_text,
            "updated_at": updated_entry["updated_at"]
        }, indent=2)
        
    except KeyError as e:
        return json.dumps({
            "error": f"Entry not found: {str(e)}"
        }, indent=2)
    except IndexError as e:
        return json.dumps({
            "error": f"Document structure issue: {str(e)}"
        }, indent=2)
    except ValueError as e:
        return json.dumps({
            "error": str(e)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "error": f"Failed to update entry: {str(e)}"
        }, indent=2)


if __name__ == "__main__":
    # Run the server
    mcp.run()
