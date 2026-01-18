Brag Document MCP – Requirements

1. Purpose

The goal of this MCP is to help create, manage, and later sync a yearly Brag Document.

At this stage, the focus is on:

Local DOCX-based document management

Clear section-based updates

Preparing the ground for future Google Drive sync

This is an incremental design: start simple, extend later.

2. Document Format

Source of truth: DOCX

Reason: editable, template-friendly, supports iterative updates

PDF: out of scope for now (may be added later as export)

3. Template

Template file location:

```
Templates/A brag document template.docx
```

New documents are created by copying the template

Existing documents are never overwritten

4. Local File Structure

Default structure (configurable root):

```
Templates/
  A brag document template.docx

BragDocuments/
  <Full Name>/
    Brag Document - <Full Name> (<Year>).docx
    .index/
      Brag Document - <Full Name> (<Year>).json
    .sync/
      Brag Document - <Full Name> (<Year>).json   (future)
```

Why .index?

DOCX does not support stable identifiers.
The index file stores:

- entry IDs

- section mapping

- metadata needed for reliable updates/deletes

5. Document Structure (from template)
Top-level sections

- Goals for this year

- Goals for next year

- Projects

- Collaboration & mentorship

- Documentation

- What you learned

- Outside of work

Nested sections

- Outside of work / Articles

- Outside of work / Webinars speaker

- Outside of work / Meetups

- Outside of work / Conferences

These section names are fixed and known in v2.

6. Core Concepts
Section

A logical part of the document.

- Identified by section_path

    - Example: Projects

    - Example: Outside of work/Articles

Entry

A single manageable line inside a section.

Minimal fields:

- entry_id (generated, stable)

- text

- section_path

- created_at

- updated_at

Entries are usually added as bullet points.

7. Functional Requirements
7.1 Ensure document exists

- If the document exists → return its path

- If it does not exist → create it from the template

- Create folders automatically

- Do not overwrite existing files

7.2 Read document outline

- Detect sections

- Read entries per section

- Return entries with IDs (if known)

7.2.1 Read specific section

- Read content of a single section by section_path

- Return all entries in that section with their IDs

- Support both top-level and nested sections

7.3 Add entry

- Add a new entry to a given section

- Append by default

- Use bullet formatting

- Generate a new entry_id

- Store mapping in .index

7.4 Update entry

Status: [x] Implemented

Preferred:

- Update by entry_id [x] Implemented

Fallback:

- Match by text + section_path + occurrence index [x] Implemented

7.5 Delete entry

Preferred:

- Delete by entry_id

Fallback:

- Match by section + text

7.6 Section awareness

- Tools must allow targeting any known section

- Nested sections must be supported

- No free-form section creation yet (future feature)

8. MCP Tools (v2)

| Tool Name | Status | Description | Input Parameters | Output |
|-----------|--------|-------------|-------------------|--------|
| `bragdoc.create_brag_document` | ✅ Implemented | Creates document from template if missing. Never overwrites existing documents. | • `full_name` (required)<br>• `year` (required)<br>• `workspace_root` (optional) | • `status`: "created" \| "exists"<br>• `document_path`<br>• `index_path` |
| `bragdoc.get_outline` | ❌ Not implemented | Returns document structure with sections and entries. | • `full_name` (required)<br>• `year` (required)<br>• `workspace_root` (optional) | • `sections`<br>• `entries` per section<br>• `entry_ids` (if available) |
| `bragdoc.get_section` | ❌ Not implemented | Returns content of a specific section with all entries. | • `full_name` (required)<br>• `year` (required)<br>• `section_path` (required)<br>• `workspace_root` (optional) | • `section_path`<br>• `entries`: array of entry objects with `entry_id`, `text`, `created_at`, `updated_at` |
| `bragdoc.add_entry` | ✅ Implemented | Adds a new entry (bullet point) to a specified section. Appends by default. | • `full_name` (required)<br>• `year` (required)<br>• `section_path` (required)<br>• `text` (required)<br>• `position` (optional, 0-based)<br>• `workspace_root` (optional) | • `entry_id`<br>• `section_path`<br>• `text`<br>• `position` |
| `bragdoc.update_entry` | ✅ Implemented | Updates an existing entry. Supports two methods:<br>1. By `entry_id` (preferred)<br>2. By `old_text` + `section_path` (fallback) | • `full_name` (required)<br>• `year` (required)<br>• `new_text` (required)<br>• `entry_id` (optional, preferred)<br>• `old_text` (optional, used with `section_path`)<br>• `section_path` (optional, used with `old_text`)<br>• `occurrence_index` (optional, default 0)<br>• `workspace_root` (optional) | • `entry_id`<br>• `section_path`<br>• `text`<br>• `updated_at` |
| `bragdoc.delete_entry` | ❌ Not implemented | Deletes an entry from the document. | • `full_name` (required)<br>• `year` (required)<br>• `entry_id` (required)<br>• `workspace_root` (optional) | • `entry_id`<br>• `status`: "deleted" |

**Example Prompts:**

- **create_brag_document**: "Create a brag document for John Doe for year 2024"
- **add_entry**: "Add an entry to the Projects section: Led the migration to microservices architecture"
- **update_entry (by ID)**: "Update entry with ID abc-123 to: Led the successful migration to microservices architecture"
- **update_entry (by text)**: "Update 'Speaker of Test Warez conference 2025' in Conferences section to: Speaker of Test Warez conference 2026"

9. MCP Resources

| Resource URI | Status | Description | Contains |
|--------------|--------|-------------|----------|
| `bragdoc://document/<full_name>/<year>` | ❌ Not implemented | Document metadata resource | • `document_path`<br>• `last_modified_time`<br>• `created_at` |
| `bragdoc://index/<full_name>/<year>` | ❌ Not implemented | Index file resource with entry mappings | • `section_registry`<br>• `entry_id_mappings`<br>• `paragraph_indices`<br>• `metadata` |
| `bragdoc://schema/sections` | ❌ Not implemented | Static schema resource listing all supported sections | • `top_level_sections`: array of section names<br>• `nested_sections`: array of nested section paths<br>• `section_hierarchy`: complete section structure |
| `bragdoc://section/<full_name>/<year>/<section_path>` | ❌ Not implemented | Section-specific resource with entries | • `section_path`<br>• `entries`: array of entry objects<br>• `entry_ids` and metadata<br>• `entry_count` |

10. Google Drive Sync (future)
Planned sync modes

- local_master – local document overwrites Drive

- drive_master – Drive document overwrites local

Planned tools

- bragdoc.drive.link

- bragdoc.drive.sync

- bragdoc.drive.status

Sync rules

- Always create backups before overwriting

- Track sync state in .sync metadata file

11. Non-Goals (for now)

- No automatic TOC regeneration

- No PDF export

- No cloud auth handling

- No conflict UI

- No content auto-generation

12. Acceptance Criteria

- Document can be created from template

- Sections are detected correctly

- Entries can be added, updated, and deleted reliably

- Entry IDs remain stable across runs

- Index file stays in sync with DOCX