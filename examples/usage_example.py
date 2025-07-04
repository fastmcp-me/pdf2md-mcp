"""
Example usage of the PDF2MD MCP Server.

This example demonstrates how to use the server programmatically.
"""

import asyncio
from pdf2md_mcp.server import convert_pdf_to_markdown


async def example_local_file_conversion():
    """Example: Convert a local PDF file to Markdown."""
    print("Converting local PDF file...")
    
    # Example with a local file
    result = await convert_pdf_to_markdown(
        file_path="./sample.pdf",
        output_dir="./output"
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Success! Output file: {result['output_file']}")
        print(f"Summary: {result['summary']}")
        print(f"Pages processed: {result['pages_processed']}")
        print(f"AI Sampling used: {result.get('sampling_used', False)}")


async def example_url_conversion():
    """Example: Convert a PDF from URL to Markdown."""
    print("Converting PDF from URL...")
    
    # Example with a URL
    result = await convert_pdf_to_markdown(
        file_path="https://example.com/document.pdf",
        output_dir="./downloads"
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Success! Output file: {result['output_file']}")
        print(f"Summary: {result['summary']}")
        print(f"Pages processed: {result['pages_processed']}")
        print(f"AI Sampling used: {result.get('sampling_used', False)}")


async def example_resume_conversion():
    """Example: Resume conversion of a partially processed file."""
    print("Resuming conversion...")
    
    # This will check for existing content and continue from where it left off
    result = await convert_pdf_to_markdown(
        file_path="./large_document.pdf"
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Resumed conversion from page {result['start_page']}")
        print(f"Output file: {result['output_file']}")
        print(f"Additional pages processed: {result['pages_processed']}")
        print(f"AI Sampling used: {result.get('sampling_used', False)}")


async def main():
    """Run all examples."""
    print("=== PDF2MD MCP Server Examples ===\n")
    
    await example_local_file_conversion()
    print()
    
    await example_url_conversion()
    print()
    
    await example_resume_conversion()
    print()
    
    print("Examples completed!")


if __name__ == "__main__":
    asyncio.run(main())
