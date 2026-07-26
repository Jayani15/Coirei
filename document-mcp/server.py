from mcp.server.fastmcp import FastMCP

from tools.upload import upload_document
from tools.search import search_documents_tool
from tools.summary import summarize_document
from tools.documents import (
    list_documents_tool,
    get_document_info,
    delete_document_tool
)
from tools.statistics import document_statistics

# Create MCP Server
mcp = FastMCP("DocuMind MCP")


@mcp.tool()
def upload(file_path: str):
    """
    Upload and index a document.
    """
    return upload_document(file_path)


@mcp.tool()
def search(query: str):
    """
    Search documents using semantic similarity.
    """
    return search_documents_tool(query)


@mcp.tool()
def summarize(filename: str):
    """
    Summarize a document.
    """
    return summarize_document(filename)


@mcp.tool()
def list_documents():
    """
    List all uploaded documents.
    """
    return list_documents_tool()


@mcp.tool()
def document_info(filename: str):
    """
    Get document metadata.
    """
    return get_document_info(filename)


@mcp.tool()
def delete(filename: str):
    """
    Delete a document.
    """
    return delete_document_tool(filename)


@mcp.tool()
def statistics():
    """
    Show document statistics.
    """
    return document_statistics()


if __name__ == "__main__":
    print("Starting DocuMind MCP...")
    mcp.run()
    print("Server stopped.")