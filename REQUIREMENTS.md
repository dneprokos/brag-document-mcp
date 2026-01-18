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

Preferred:

- Update by entry_id

Fallback (if needed):

- Match by text + occurrence index

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

bragdoc.create_brag_document

Status: [x] Implemented

Creates document if missing.

Input

- full_name

- year

- workspace_root (optional)

Output

- status: created | exists

- document_path

- index_path

bragdoc.get_outline

Status: [ ] Not implemented

Returns document structure.

Output

- sections

- entries per section

- entry IDs (if available)

bragdoc.get_section

Status: [ ] Not implemented

Returns content of a specific section.

Input

- full_name

- year

- section_path

- workspace_root (optional)

Output

- section_path

- entries (array of entry objects with entry_id, text, created_at, updated_at)

bragdoc.add_entry

Status: [ ] Not implemented

Adds a new entry.

Input

- section_path

- text

- position (optional)

Output

- entry_id

- section_path

- text

bragdoc.update_entry

Status: [ ] Not implemented

Updates an existing entry.

Input

- entry_id

- new_text

bragdoc.delete_entry

Status: [ ] Not implemented

Deletes an entry.

Input

- entry_id

9. MCP Resources
Document resource

Status: [ ] Not implemented

```
bragdoc://document/<full_name>/<year>
```

Contains:

- document path

- last modified time

Index resource

Status: [ ] Not implemented

```
bragdoc://index/<full_name>/<year>
```

Contains:

- section registry

- entry ID mappings

- minimal positioning info

Section schema resource

Status: [ ] Not implemented

```
bragdoc://schema/sections
```

Static list of supported sections and paths.

Section resource

Status: [ ] Not implemented

```
bragdoc://section/<full_name>/<year>/<section_path>
```

Contains:

- section_path

- entries in that section

- entry IDs and metadata

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