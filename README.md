# Brag Document MCP Server

A Model Context Protocol (MCP) server built with FastMCP that helps create and manage yearly Brag Documents in DOCX format. Perfect for tracking your professional achievements, goals, and learning throughout the year.

## Features

* ✅ **Create Brag Documents**: Generate brag documents from a template with all standard sections
* 📁 **Local Document Management**: DOCX-based document management with index tracking
* 🔄 **Template-Based**: Uses a customizable DOCX template for consistent formatting
* 🚀 **MCP Integration**: Seamlessly integrates with Cursor IDE and other MCP-compatible tools

## Prerequisites

* Python 3.10 or higher
* `uv` package manager (for installing FastMCP)
* Cursor IDE (for integration) or any MCP-compatible client

## Installation

### 1. Install `uv` Package Manager

`uv` is required to install FastMCP and its dependencies.

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, add `uv` to your PATH or restart your terminal.

### 2. Set Up the Project

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd brag-document-mcp
   ```

2. Create a virtual environment with Python 3.10+:
   ```bash
   uv venv --python 3.10
   ```

3. Install dependencies:
   ```bash
   uv pip install --python .venv/Scripts/python.exe fastmcp python-docx-ng
   ```
   
   Or using the requirements file:
   ```bash
   uv pip install --python .venv/Scripts/python.exe -r requirements.txt
   ```

## Configuration in Cursor

### Step 1: Locate Your MCP Configuration File

The MCP configuration file is located at:

* **Windows**: `C:\Users\<YourUsername>\.cursor\mcp.json`
* **macOS/Linux**: `~/.cursor/mcp.json`

### Step 2: Add the Server Configuration

Open `mcp.json` and add the `brag-document-mcp` server configuration:

```json
{
  "mcpServers": {
    "brag-document-mcp": {
      "command": "<path-to-project>/.venv/Scripts/python.exe",
      "args": [
        "<path-to-project>/server.py"
      ]
    }
  }
}
```

**Important Notes:**

* Replace `<path-to-project>` with the absolute path to this project directory
* On Windows, use forward slashes (`/`) or escaped backslashes (`\\`) in paths
* On macOS/Linux, the Python executable will be at `.venv/bin/python` instead of `.venv/Scripts/python.exe`

### Step 3: Restart Cursor

After saving `mcp.json`, restart Cursor IDE completely for the changes to take effect.

### Step 4: Verify Installation

After restarting, verify the server is working by asking in Cursor's chat:

* "Create a brag document for John Doe for year 2024"

If the server is configured correctly, Cursor will use the tool to create the document.

## Usage

Once configured, you can use the tools in Cursor's chat interface. The AI will automatically detect your request and use the appropriate tool.

### Available Tools

#### `bragdoc.create_brag_document`

Creates a brag document from the template if it doesn't exist. Never overwrites existing documents. Automatically replaces placeholders in the title and removes example entries.

**Parameters:**
- `full_name`: Full name of the person (e.g., "John Doe")
- `year`: Year for the brag document (e.g., 2024)
- `workspace_root`: (Optional) Custom workspace directory

**Example Prompts:**
- "Create a brag document for John Doe for year 2024"
- "Create a brag document for Jane Smith for 2024"
- "Set up a brag document for Alice Johnson, year 2024"

#### `bragdoc.add_entry`

Adds a new entry (bullet point) to a specified section in the brag document. The entry is appended by default, or inserted at a specific position if provided.

**Parameters:**
- `full_name`: Full name of the person (e.g., "John Doe")
- `year`: Year for the brag document (e.g., 2024)
- `section_path`: Section where to add the entry (e.g., "Projects", "Outside of work/Articles")
- `text`: Text content of the entry
- `position`: (Optional) Position index to insert at (0-based). If None, appends at end.
- `workspace_root`: (Optional) Custom workspace directory

**Example Prompts:**
- "Add an entry to the Projects section: Led the migration to microservices architecture"
- "Add 'Published article on AI trends' to the Articles section"
- "Add entry to Projects: Implemented new authentication system"
- "Add to Collaboration & mentorship: Mentored 3 junior developers this quarter"

## Project Structure

```
brag-document-mcp/
├── server.py              # Main MCP server implementation
├── document_utils.py      # Helper functions for document management
├── Templates/             # Document templates
│   └── A brag document template.docx
├── BragDocuments/         # Generated documents (created at runtime)
│   └── <Full Name>/
│       ├── Brag Document - <Full Name> (<Year>).docx
│       └── .index/
│           └── Brag Document - <Full Name> (<Year>).json
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── REQUIREMENTS.md        # Detailed requirements specification
└── README.md             # This file
```

## Document Structure

The brag document template includes the following sections:

**Top-level sections:**
- Goals for this year
- Goals for next year
- Projects
- Collaboration & mentorship
- Documentation
- What you learned
- Outside of work

**Nested sections:**
- Outside of work / Articles
- Outside of work / Webinars speaker
- Outside of work / Meetups
- Outside of work / Conferences

## Roadmap

The following features are planned for future releases:

* **Document Reading**: Get document outline and read specific sections
* **Entry Management**: Add, update, and delete entries in sections
* **MCP Resources**: Access document metadata and index files via resources
* **Google Drive Sync**: Sync documents with Google Drive (future)

See [REQUIREMENTS.md](REQUIREMENTS.md) for detailed specifications.

## Dependencies

* **fastmcp**: FastMCP framework for building MCP servers
* **python-docx-ng**: Library for working with DOCX files (fork of python-docx with improved style handling)

## Troubleshooting

### Server Not Starting

1. **Check Python version**: Ensure you're using Python 3.10 or higher
   ```bash
   .venv/Scripts/python.exe --version
   ```

2. **Verify dependencies**: Make sure all dependencies are installed
   ```bash
   uv pip install --python .venv/Scripts/python.exe -r requirements.txt
   ```

3. **Check file paths**: Verify the paths in `mcp.json` are correct and use forward slashes

### Tool Not Available in Cursor

1. **Restart Cursor**: Always restart Cursor after changing `mcp.json`
2. **Check logs**: Look for errors in Cursor's MCP logs
3. **Verify server runs**: Test the server manually:
   ```bash
   .venv/Scripts/python.exe server.py
   ```

### Template Not Found

If you see "Template not found" errors:
1. Ensure `Templates/A brag document template.docx` exists in your project root
2. Check that the template file is not corrupted
3. Verify the workspace_root path if using a custom location

## Contributing

Contributions are welcome! When adding new tools:

1. Follow the existing code style
2. Add clear docstrings
3. Handle errors appropriately
4. Test your changes
5. Update REQUIREMENTS.md implementation status
6. Update this README if adding significant features

## License

This project is open source and available for use and modification.

## Resources

* [FastMCP Documentation](https://github.com/jlowin/fastmcp)
* [MCP Protocol Specification](https://modelcontextprotocol.io/)
* [python-docx Documentation](https://python-docx.readthedocs.io/)
* [Cursor MCP Integration](https://cursor.sh/docs/mcp)
