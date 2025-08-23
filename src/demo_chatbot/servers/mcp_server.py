"""
MCP (Model Context Protocol) Server Implementation

Provides tools for the agent to interact with external systems.
Features:
- Type-safe operations with Pydantic models
- Comprehensive error handling and logging
- Async/await support for better performance
- Resource management and security checks
- Monitoring and metrics collection
"""

import os
import sys
import json
import asyncio
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime

from mcp.server import Server
from pydantic import BaseModel, Field, validator

from ..config.settings import settings
from ..utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)


class FileOperationResult(BaseModel):
    """Result model for file operations."""
    success: bool
    message: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    error_code: Optional[str] = None


class DirectoryListResult(BaseModel):
    """Result model for directory listing."""
    success: bool
    directory: str
    files: List[Dict[str, Any]]
    directories: List[Dict[str, Any]]
    total_items: int
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    error: Optional[str] = None


class SearchResult(BaseModel):
    """Result model for search operations."""
    success: bool
    query: str
    results: List[Dict[str, str]]
    total_results: int
    search_engine: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    error: Optional[str] = None


class SystemInfoResult(BaseModel):
    """Result model for system information."""
    success: bool
    system: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    error: Optional[str] = None


class MCPServer:
    """MCP Server with enhanced tool implementations.
    
    Features:
    - Type-safe operations
    - Comprehensive error handling
    - Performance monitoring
    - Security validations
    - Async/await support
    """
    
    def __init__(self, server_name: str = "demo-chatbot-mcp"):
        """Initialize the MCP server.
        
        Args:
            server_name: Name of the MCP server
        """
        self.server_name = server_name
        self.server = Server(server_name)
        self.max_file_size = settings.max_file_size
        self.allowed_extensions = settings.allowed_file_extensions
        
        logger.info(f"Initializing MCP server: {server_name}")
        self.setup_tools()
        logger.info("MCP server initialized successfully")
    
    def _validate_file_path(self, file_path: str) -> Path:
        """Validate and resolve file path securely.
        
        Args:
            file_path: Path to validate
            
        Returns:
            Resolved Path object
            
        Raises:
            ValueError: If path is invalid or unsafe
        """
        try:
            path = Path(file_path)
            
            # Security: resolve to absolute path to prevent directory traversal
            if not path.is_absolute():
                path = Path.cwd() / path
            path = path.resolve()
            
            # Check if path is within allowed working directory
            working_dir = settings.working_directory.resolve()
            try:
                path.relative_to(working_dir)
            except ValueError:
                # Path is outside working directory, check if it's in current directory
                try:
                    path.relative_to(Path.cwd())
                except ValueError:
                    raise ValueError(f"Path outside allowed directories: {path}")
            
            return path
            
        except Exception as e:
            logger.warning(f"Path validation failed for {file_path}: {e}")
            raise ValueError(f"Invalid file path: {e}")
    
    def _check_file_extension(self, path: Path) -> bool:
        """Check if file extension is allowed.
        
        Args:
            path: Path to check
            
        Returns:
            True if extension is allowed
        """
        return path.suffix.lower() in self.allowed_extensions
    
    def setup_tools(self) -> None:
        """Setup available tools for the MCP server with enhanced error handling."""
        logger.info("Setting up MCP server tools")
        
        # Note: Actual tool registration would depend on MCP library implementation
        # For now, we define the tool functions that would be registered
        
        async def read_file(file_path: str, encoding: str = "utf-8") -> FileOperationResult:
            """Read contents of a file with comprehensive validation.
            
            Args:
                file_path: Path to the file to read
                encoding: File encoding (default: utf-8)
                
            Returns:
                FileOperationResult with file contents or error information
            """
            try:
                logger.debug(f"Reading file: {file_path}")
                
                # Validate and resolve path
                path = self._validate_file_path(file_path)
                
                # Check if file exists
                if not path.exists():
                    return FileOperationResult(
                        success=False,
                        message=f"File not found: {file_path}",
                        error_code="FILE_NOT_FOUND"
                    )
                
                # Check if it's actually a file
                if not path.is_file():
                    return FileOperationResult(
                        success=False,
                        message=f"Path is not a file: {file_path}",
                        error_code="NOT_A_FILE"
                    )
                
                # Check file size
                file_size = path.stat().st_size
                if file_size > self.max_file_size:
                    return FileOperationResult(
                        success=False,
                        message=f"File too large: {file_size} bytes (max: {self.max_file_size})",
                        file_size=file_size,
                        error_code="FILE_TOO_LARGE"
                    )
                
                # Check file extension
                if not self._check_file_extension(path):
                    return FileOperationResult(
                        success=False,
                        message=f"File type not allowed: {path.suffix}",
                        error_code="INVALID_FILE_TYPE"
                    )
                
                # Read file content using standard file operations
                try:
                    with open(path, 'r', encoding=encoding) as f:
                        content = f.read()
                except UnicodeDecodeError:
                    return FileOperationResult(
                        success=False,
                        message=f"Cannot decode file with {encoding} encoding",
                        file_path=str(path),
                        error_code="ENCODING_ERROR"
                    )
                
                logger.info(f"Successfully read file: {path} ({file_size} bytes)")
                return FileOperationResult(
                    success=True,
                    message=content,
                    file_path=str(path),
                    file_size=file_size
                )
                
            except PermissionError:
                logger.warning(f"Permission denied reading file: {file_path}")
                return FileOperationResult(
                    success=False,
                    message=f"Permission denied: {file_path}",
                    error_code="PERMISSION_DENIED"
                )
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")
                return FileOperationResult(
                    success=False,
                    message=f"Error reading file: {str(e)}",
                    error_code="UNKNOWN_ERROR"
                )
        
        async def write_file(file_path: str, content: str, encoding: str = "utf-8") -> FileOperationResult:
            """Write content to a file with validation and safety checks.
            
            Args:
                file_path: Path where to write the file
                content: Content to write to the file
                encoding: File encoding (default: utf-8)
                
            Returns:
                FileOperationResult with operation status
            """
            try:
                logger.debug(f"Writing file: {file_path}")
                
                # Validate and resolve path
                path = self._validate_file_path(file_path)
                
                # Check content size
                content_size = len(content.encode(encoding))
                if content_size > self.max_file_size:
                    return FileOperationResult(
                        success=False,
                        message=f"Content too large: {content_size} bytes (max: {self.max_file_size})",
                        error_code="CONTENT_TOO_LARGE"
                    )
                
                # Check file extension
                if not self._check_file_extension(path):
                    return FileOperationResult(
                        success=False,
                        message=f"File type not allowed: {path.suffix}",
                        error_code="INVALID_FILE_TYPE"
                    )
                
                # Create parent directories if needed
                path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write file content using standard file operations
                with open(path, 'w', encoding=encoding) as f:
                    f.write(content)
                
                logger.info(f"Successfully wrote file: {path} ({content_size} bytes)")
                return FileOperationResult(
                    success=True,
                    message=f"File written successfully: {path}",
                    file_path=str(path),
                    file_size=content_size
                )
                
            except PermissionError:
                logger.warning(f"Permission denied writing file: {file_path}")
                return FileOperationResult(
                    success=False,
                    message=f"Permission denied: {file_path}",
                    error_code="PERMISSION_DENIED"
                )
            except Exception as e:
                logger.error(f"Error writing file {file_path}: {e}")
                return FileOperationResult(
                    success=False,
                    message=f"Error writing file: {str(e)}",
                    error_code="UNKNOWN_ERROR"
                )
        
        async def list_directory(directory_path: str = ".") -> DirectoryListResult:
            """List contents of a directory with detailed information.
            
            Args:
                directory_path: Path to directory to list
                
            Returns:
                DirectoryListResult with directory contents
            """
            try:
                logger.debug(f"Listing directory: {directory_path}")
                
                # Validate and resolve path
                path = self._validate_file_path(directory_path)
                
                if not path.exists():
                    return DirectoryListResult(
                        success=False,
                        directory=directory_path,
                        files=[],
                        directories=[],
                        total_items=0,
                        error="Directory not found"
                    )
                
                if not path.is_dir():
                    return DirectoryListResult(
                        success=False,
                        directory=directory_path,
                        files=[],
                        directories=[],
                        total_items=0,
                        error="Path is not a directory"
                    )
                
                # Get directory contents using standard operations
                items = list(path.iterdir())
                files = []
                directories = []
                
                for item in items:
                    try:
                        stat_info = item.stat()
                        item_info = {
                            "name": item.name,
                            "path": str(item.absolute()),
                            "size": stat_info.st_size,
                            "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                            "permissions": oct(stat_info.st_mode)[-3:]
                        }
                        
                        if item.is_file():
                            files.append(item_info)
                        elif item.is_dir():
                            directories.append(item_info)
                            
                    except (PermissionError, OSError) as e:
                        logger.warning(f"Cannot access {item}: {e}")
                        continue
                
                # Sort results
                files.sort(key=lambda x: x["name"].lower())
                directories.sort(key=lambda x: x["name"].lower())
                
                total_items = len(files) + len(directories)
                
                logger.info(f"Listed directory {path}: {total_items} items")
                return DirectoryListResult(
                    success=True,
                    directory=str(path.absolute()),
                    files=files,
                    directories=directories,
                    total_items=total_items
                )
                
            except PermissionError:
                logger.warning(f"Permission denied accessing directory: {directory_path}")
                return DirectoryListResult(
                    success=False,
                    directory=directory_path,
                    files=[],
                    directories=[],
                    total_items=0,
                    error="Permission denied"
                )
            except Exception as e:
                logger.error(f"Error listing directory {directory_path}: {e}")
                return DirectoryListResult(
                    success=False,
                    directory=directory_path,
                    files=[],
                    directories=[],
                    total_items=0,
                    error=str(e)
                )
        
        async def search_web(query: str, max_results: int = 5) -> SearchResult:
            """Perform a web search with enhanced mock implementation.
            
            Args:
                query: Search query string
                max_results: Maximum number of results to return
                
            Returns:
                SearchResult with mock search results
            """
            try:
                logger.debug(f"Performing web search: {query}")
                
                if not query or not query.strip():
                    return SearchResult(
                        success=False,
                        query=query,
                        results=[],
                        total_results=0,
                        search_engine="mock",
                        error="Empty search query"
                    )
                
                # Validate max_results
                max_results = max(1, min(max_results, 20))  # Limit between 1-20
                
                # Generate mock results based on query
                search_terms = query.strip().split()
                results = []
                
                for i in range(max_results):
                    domain = ["wikipedia.org", "github.com", "stackoverflow.com", "docs.python.org", "example.com"][i % 5]
                    results.append({
                        "title": f"{search_terms[0].title()} - Comprehensive Guide {i+1}",
                        "url": f"https://{domain}/{query.replace(' ', '-').lower()}-{i+1}",
                        "snippet": f"Learn about {query} with detailed examples and best practices. This comprehensive guide covers everything you need to know about {' '.join(search_terms[:3])}...",
                        "domain": domain,
                        "relevance_score": round(1.0 - (i * 0.1), 2)
                    })
                
                logger.info(f"Generated {len(results)} mock search results for: {query}")
                return SearchResult(
                    success=True,
                    query=query,
                    results=results,
                    total_results=len(results),
                    search_engine="mock"
                )
                
            except Exception as e:
                logger.error(f"Error performing web search: {e}")
                return SearchResult(
                    success=False,
                    query=query,
                    results=[],
                    total_results=0,
                    search_engine="mock",
                    error=str(e)
                )
        
        async def get_system_info() -> SystemInfoResult:
            """Get comprehensive system information.
            
            Returns:
                SystemInfoResult with system details
            """
            try:
                logger.debug("Gathering system information")
                
                import platform
                system_info = {
                    "platform": platform.system(),
                    "platform_release": platform.release(),
                    "platform_version": platform.version(),
                    "architecture": platform.architecture()[0],
                    "machine": platform.machine(),
                    "processor": platform.processor(),
                    "python_version": platform.python_version(),
                    "python_implementation": platform.python_implementation(),
                    "hostname": platform.node()
                }
                
                # Try to get additional system info if psutil is available
                try:
                    import psutil
                    
                    # Memory information
                    memory = psutil.virtual_memory()
                    memory_info = {
                        "memory_total": memory.total,
                        "memory_available": memory.available,
                        "memory_percent": memory.percent,
                        "cpu_count": psutil.cpu_count(),
                        "cpu_count_logical": psutil.cpu_count(logical=True),
                        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                    }
                    system_info.update(memory_info)
                    
                    # Disk usage for current directory
                    try:
                        disk_usage = psutil.disk_usage('.')
                        disk_info = {
                            "total": disk_usage.total,
                            "used": disk_usage.used,
                            "free": disk_usage.free,
                            "percent": (disk_usage.used / disk_usage.total) * 100
                        }
                        system_info["disk_usage"] = disk_info
                    except Exception:
                        pass
                    
                    # Load average (Unix-like systems)
                    try:
                        if hasattr(psutil, 'getloadavg'):
                            load_avg = psutil.getloadavg()
                            system_info["load_average"] = load_avg
                    except Exception:
                        pass
                        
                except ImportError:
                    logger.info("psutil not available, providing basic system info")
                    system_info["note"] = "Install psutil for detailed system information"
                
                # Add environment information
                env_info = {
                    "working_directory": str(Path.cwd()),
                    "home_directory": str(Path.home()),
                    "python_executable": str(Path(sys.executable)),
                    "path_separator": os.sep,
                    "line_separator": os.linesep
                }
                system_info["environment"] = env_info
                
                logger.info("Successfully gathered system information")
                return SystemInfoResult(
                    success=True,
                    system=system_info
                )
                
            except Exception as e:
                logger.error(f"Error getting system information: {e}")
                return SystemInfoResult(
                    success=False,
                    system={},
                    error=str(e)
                )
        
        logger.info("MCP server tools setup completed")
    
    async def start(self, host: str = "localhost", port: int = 8080) -> None:
        """Start the MCP server with enhanced configuration.
        
        Args:
            host: Host address to bind to
            port: Port number to bind to
        """
        try:
            logger.info(f"Starting MCP server {self.server_name} on {host}:{port}")
            
            # Configure server settings
            server_config = {
                "host": host,
                "port": port,
                "access_log": True,
                "debug": settings.log_level == "DEBUG"
            }
            
            logger.info(f"Server configuration: {server_config}")
            await self.server.run(**server_config)
            
        except Exception as e:
            logger.error(f"Failed to start MCP server: {e}")
            raise
    
    async def stop(self) -> None:
        """Stop the MCP server gracefully."""
        try:
            logger.info(f"Stopping MCP server {self.server_name}")
            # Server shutdown logic would go here
            logger.info("MCP server stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping MCP server: {e}")
            raise
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information and status.
        
        Returns:
            Dictionary with server information
        """
        return {
            "server_name": self.server_name,
            "max_file_size": self.max_file_size,
            "allowed_extensions": self.allowed_extensions,
            "tools_count": 5,  # Fixed number of tools
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check of the server.
        
        Returns:
            Health check results
        """
        try:
            health_status = {
                "status": "healthy",
                "server_name": self.server_name,
                "timestamp": datetime.now().isoformat(),
                "checks": {}
            }
            
            # Check file system access
            try:
                test_path = settings.working_directory / ".health_check"
                test_path.touch()
                test_path.unlink()
                health_status["checks"]["filesystem"] = "ok"
            except Exception as e:
                health_status["checks"]["filesystem"] = f"error: {e}"
                health_status["status"] = "degraded"
            
            # Check memory usage
            try:
                import psutil
                memory = psutil.virtual_memory()
                health_status["checks"]["memory"] = {
                    "percent_used": memory.percent,
                    "status": "ok" if memory.percent < 90 else "warning"
                }
            except ImportError:
                health_status["checks"]["memory"] = "psutil not available"
            
            return health_status
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


async def main() -> None:
    """Main entry point for the MCP server with enhanced configuration."""
    try:
        # Create and configure server
        server = MCPServer("demo-chatbot-mcp")
        
        # Get configuration from settings
        host = settings.mcp_host
        port = settings.mcp_port
        
        logger.info(f"Demo Chatbot MCP Server starting...")
        logger.info(f"Configuration: {server.get_server_info()}")
        
        # Start server
        await server.start(host, port)
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        raise
    finally:
        logger.info("MCP server shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        import sys
        sys.exit(1)