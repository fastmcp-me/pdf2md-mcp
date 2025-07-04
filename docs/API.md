# PDF2MD MCP Server API Documentation

## Overview

The PDF2MD MCP Server provides Model Context Protocol (MCP) tools for converting PDF files to Markdown format using AI sampling capabilities.

## Tools

### convert_pdf_to_markdown

Converts a PDF file to Markdown format using AI sampling.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_path` | string | Yes | Local file path or URL to the PDF file |
| `output_dir` | string | No | Output directory for the markdown file. Defaults to same directory as input file (for local files) or current working directory (for URLs) |

#### Returns

Returns a dictionary with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `output_file` | string or null | Path to the generated markdown file |
| `summary` | string | Summary of the conversion task |
| `pages_processed` | integer | Number of pages processed in this operation |
| `start_page` | integer | Page number where processing started |
| `source` | string | Description of the source (local file or URL) |
| `sampling_used` | boolean | Whether MCP sampling was used for extraction |
| `error` | string | Error message (only present if conversion failed) |

#### Examples

**Convert local PDF file:**
```json
{
  "tool": "convert_pdf_to_markdown",
  "arguments": {
    "file_path": "/path/to/document.pdf",
    "output_dir": "/output/directory"
  }
}
```

**Convert PDF from URL:**
```json
{
  "tool": "convert_pdf_to_markdown",
  "arguments": {
    "file_path": "https://example.com/document.pdf"
  }
}
```

**Response (Success):**
```json
{
  "output_file": "/output/directory/document.md",
  "summary": "Started PDF conversion from Local file: /path/to/document.pdf with AI sampling. Processed 5 pages starting from page 1. Output saved to: /output/directory/document.md",
  "pages_processed": 5,
  "start_page": 1,
  "source": "Local file: /path/to/document.pdf",
  "sampling_used": true
}
```

**Response (Error):**
```json
{
  "error": "File not found: /path/to/nonexistent.pdf",
  "output_file": null,
  "summary": "Failed - file not found",
  "pages_processed": 0
}
```

## Features

### Incremental Processing

The server automatically detects existing markdown content and can resume processing from where it left off. It looks for page markers in the existing content:

- `## Page X` - Header-style page markers
- `<!-- Page X -->` - Comment-style page markers

### URL Support

The server can download PDF files from URLs before processing them. Downloaded files are stored in the specified output directory or current working directory.

### Error Handling

The server provides comprehensive error handling for:
- Non-existent files
- Network errors when downloading URLs
- File permission issues
- Invalid file formats

## Implementation Notes

### AI Sampling Integration

The server uses FastMCP's `ctx.sample()` method to request content extraction from the client's LLM:

```python
# Extract content using LLM sampling
prompt = f"Please extract and convert the content from the PDF file: {pdf_path}..."
extracted_content = await ctx.sample(prompt)
```

The sampling process:

1. **Constructs a detailed prompt** asking the LLM to extract and convert PDF content to Markdown
2. **Uses `ctx.sample()`** to send the request to the client's LLM
3. **Processes the response** to count pages and format the output
4. **Falls back gracefully** if sampling is unavailable or fails

### Fallback Behavior

When no sampling context is available (e.g., during testing or if the client doesn't support sampling), the server:
- Uses a fallback extraction method
- Still creates properly formatted Markdown output
- Indicates fallback mode in the summary

### File Format Support

- Input: PDF files (local paths or URLs)
- Output: Markdown (.md) files with UTF-8 encoding

### Page Detection

The server uses regular expressions to detect existing page markers:
```python
r'(?:##\s*Page\s*(\d+)|<!--\s*Page\s*(\d+)\s*-->)'
```

## Configuration

### Server Startup

Start the server using:
```bash
pdf2md-mcp
```

### Client Configuration

Add to your MCP client configuration:
```json
{
  "mcpServers": {
    "pdf2md": {
      "command": "pdf2md-mcp",
      "args": [],
      "env": {},
      "description": "PDF to Markdown conversion using AI sampling"
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **File not found errors**: Ensure the PDF file path is correct and the file exists
2. **Permission errors**: Check that the server has read access to the input file and write access to the output directory
3. **Network errors**: Verify URL accessibility and network connectivity for URL-based conversions
4. **Large file processing**: For very large PDFs, consider processing in smaller batches

### Debug Mode

The server provides detailed error messages and summaries to help diagnose issues. Check the `summary` field in the response for processing details.

## Security Considerations

- The server can download files from URLs - ensure URL sources are trusted
- Output files are created with default system permissions
- No authentication is implemented - suitable for local/trusted environments only

## Performance

- Processing time depends on PDF size and complexity
- Network downloads add latency for URL-based conversions
- Incremental processing reduces re-processing time for large documents
