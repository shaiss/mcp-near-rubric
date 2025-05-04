# NEAR Rubric MCP Evaluation Module

This module provides evaluation capabilities for the NEAR Rubric MCP server.

## Components

### File Matcher

The `file_matcher.py` module provides sophisticated pattern matching capabilities for identifying relevant files and code sections in NEAR Protocol projects.

#### Key Features

- **Glob Pattern Matching**: Supports standard glob patterns like `**/*.rs`, `**/src/*.js`, etc.
- **Multiple Extension Patterns**: Handles patterns with multiple extensions like `*.{js,ts,jsx,tsx}`
- **Regex Pattern Matching**: Supports searching for regex patterns within code content
- **Cross-Platform Support**: Works consistently across Windows and Unix-like systems

#### Glob Pattern Support

The following glob patterns are supported:

- `**/*.ext` - Match files with extension `.ext` in any directory or subdirectory
- `**/dirname/*` - Match files in any directory named `dirname`
- `*.{ext1,ext2}` - Match files with any of the specified extensions
- `path/to/file.*` - Match files with any extension at a specific path

#### Usage Examples

```python
# Match files against glob patterns
matched_files = file_matcher.filter_files_by_patterns(available_files, glob_patterns)

# Check if a file matches a specific glob pattern
matches = file_matcher.match_file_with_glob("src/contract.rs", "**/*.rs")

# Find regex pattern matches in file content
matches = file_matcher.find_pattern_matches_in_file(file_content, regex_patterns)

# Handle complex glob patterns with multiple extensions
matches = file_matcher.resolve_complex_glob_pattern("**/*.{js,ts}", available_files)
```

### Pattern Library

The `pattern_library.py` module provides predefined patterns for identifying code characteristics across different NEAR evaluation categories.

#### Key Features

- **Category-specific Patterns**: Patterns tailored to each rubric category
- **Language-specific Patterns**: Different patterns for Rust, JavaScript, etc.
- **Pattern Discovery**: Functions to locate pattern matches in code

#### Usage Examples

```python
# Get patterns for a category and project type
patterns = await pattern_library.get_patterns_for_category("near_integration", "rust")

# Find pattern matches in multiple files
matches = pattern_library.find_pattern_matches_in_files(files_content, patterns)
```

### Prompt Generator

The `prompt_generator.py` module generates evaluation prompts for each rubric category.

#### Key Features

- **Category-specific Prompts**: Tailored prompts for each evaluation category
- **Project Type Adaptation**: Prompts adapted to Rust, JavaScript, etc.
- **Template Loading**: Loads prompts from template files or defaults

## Integration in the MCP Server

These components integrate with the MCP server to provide:

1. File selection guidance for clients
2. Pattern-based code analysis
3. Structured evaluation frameworks

The server leverages these capabilities while remaining lightweight, delegating actual file access to the client. 