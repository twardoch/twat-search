#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["httpx>=0.24.1", "pydantic>=2.0.0", "python-dotenv>=1.0.0", "fire>=0.5.0", "rich>=13.6.0"]
# ///
# this_file: src/twat_search/web/example.py

"""
CLI tool for performing web searches across multiple engines.

This tool allows you to search the web using various search engines and 
displays the results in a formatted table.
"""

import asyncio
import os
import logging
# We need to ignore the missing stubs for fire
import fire  # type: ignore
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler
from typing import List, Optional, Dict, Any, Union, Sequence, Iterable

# Set up logging with rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Loaded environment variables from .env file")
except ImportError:
    logger.warning("python-dotenv not installed, skipping .env loading")

# Import the search API
from twat_search.web.api import search
from twat_search.web.models import SearchResult
from twat_search.web.config import Config, EngineConfig

# Set up console
console = Console()

class SearchCLI:
    """Web search CLI tool that displays results from multiple search engines."""

    def _parse_engines(self, engines_arg: Any) -> Optional[List[str]]:
        """Parse engines argument into a list of engine names.
        
        Handles various formats:
        - String (comma-separated): "brave,google"
        - Tuple or List of strings: ("brave", "google")
        - None: Returns None (use default engines)
        
        Args:
            engines_arg: The engines argument from the command line
            
        Returns:
            List of engine names or None
        """
        if engines_arg is None:
            return None
            
        # Handle string input (from --engines="brave,google")
        if isinstance(engines_arg, str):
            return [e.strip() for e in engines_arg.split(",") if e.strip()]
            
        # Handle tuple/list input (from --engines brave google)
        if isinstance(engines_arg, (list, tuple)):
            return [str(e).strip() for e in engines_arg if str(e).strip()]
            
        # Handle unexpected type by logging and returning None
        logger.warning(f"Unexpected engines type: {type(engines_arg)}. Using all available engines.")
        return None

    async def _run_search(self, query: str = "president of poland", engines: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Run search across all available engines.
        
        Args:
            query: The search term to query
            engines: Optional list of specific engines to use
            
        Returns:
            List of result dictionaries with engine name, status, and results
        """
        logger.info(f"🔍 Searching for: {query}")
        
        try:
            results = await search(query, engines=engines)
            return self._process_results(results)
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def _process_results(self, results: list[SearchResult]) -> List[Dict[str, Any]]:
        """Process search results into a standardized format for display.
        
        Args:
            results: List of SearchResult objects
            
        Returns:
            Processed results with engine name, status, and formatted data
        """
        processed = []
        
        # Group results by engine
        engine_results: Dict[str, List[SearchResult]] = {}
        for result in results:
            # Get engine source from result metadata or use 'unknown'
            engine_name = getattr(result, 'source', None) or 'unknown'
            if engine_name not in engine_results:
                engine_results[engine_name] = []
            engine_results[engine_name].append(result)
        
        # Process each engine's results
        for engine, engine_results_list in engine_results.items():
            if not engine_results_list:
                processed.append({
                    "engine": engine,
                    "status": "❌ No results",
                    "url": "N/A",
                    "title": "N/A",
                    "snippet": "N/A"
                })
                continue
                
            # Get the first (top) result
            top_result = engine_results_list[0]
            # Convert URL to string if it's not already
            url = str(top_result.url)
            processed.append({
                "engine": engine,
                "status": "✅ Success",
                "url": url,
                "title": top_result.title,
                "snippet": top_result.snippet[:100] + "..." if len(top_result.snippet) > 100 else top_result.snippet
            })
            
        return processed
    
    def _display_results(self, processed_results: List[Dict[str, Any]]) -> None:
        """Display search results in a rich table.
        
        Args:
            processed_results: List of processed result dictionaries
        """
        if not processed_results:
            console.print("[bold red]No results found![/bold red]")
            return
            
        table = Table(title="🌐 Web Search Results")
        table.add_column("Engine", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")
        table.add_column("Title", style="green")
        table.add_column("URL", style="blue")
        
        for result in processed_results:
            table.add_row(
                result["engine"],
                result["status"],
                result["title"],
                result["url"]
            )
            
        console.print(table)
    
    def _display_errors(self, error_messages: List[str]) -> None:
        """Display error messages in a rich table.
        
        Args:
            error_messages: List of error messages
        """
        if not error_messages:
            return
            
        table = Table(title="❌ Search Errors")
        table.add_column("Error", style="red")
        
        for error in error_messages:
            table.add_row(error)
            
        console.print(table)
    
    def search(self, query: str = "president of poland", engines: Any = None) -> None:
        """Search the web using multiple search engines.
        
        Args:
            query: The search term (default: "president of poland")
            engines: Search engines to use, specified as a comma-separated string:
                     --engines="brave,google,tavily"
                     If not provided, all available engines will be used.
        """
        # Parse engines argument
        engine_list = self._parse_engines(engines)
        
        # Run search
        with console.status(f"[bold green]Searching for '{query}'...[/bold green]"):
            results = asyncio.run(self._run_search(query, engine_list))
            
        # Display results
        self._display_results(results)
        
        # Print API key information
        api_keys = {
            "BRAVE_API_KEY": "✅" if os.environ.get("BRAVE_API_KEY") else "❌",
            "SERPAPI_API_KEY": "✅" if os.environ.get("SERPAPI_API_KEY") else "❌",
            "TAVILY_API_KEY": "✅" if os.environ.get("TAVILY_API_KEY") else "❌",
            "PERPLEXITYAI_API_KEY": "✅" if os.environ.get("PERPLEXITYAI_API_KEY") else "❌",
            "YOUCOM_API_KEY": "✅" if os.environ.get("YOUCOM_API_KEY") else "❌",
        }
        
        key_table = Table(title="🔑 API Keys Status")
        key_table.add_column("Service", style="cyan", no_wrap=True)
        key_table.add_column("Status", style="magenta")
        
        for key, status in api_keys.items():
            key_table.add_row(key.replace("_API_KEY", ""), status)
            
        console.print(key_table)

    def list_engines(self) -> None:
        """List all available search engines."""
        try:
            # Create a temporary config to see available engines
            config = Config()
            
            table = Table(title="🔎 Available Search Engines")
            table.add_column("Engine", style="cyan", no_wrap=True)
            table.add_column("Enabled", style="magenta")
            table.add_column("API Key Required", style="yellow")
            
            for engine, engine_config in config.engines.items():
                # Check if API key is required by checking if the api_key attribute exists
                api_key_required = hasattr(engine_config, 'api_key') and engine_config.api_key is not None
                
                table.add_row(
                    engine,
                    "✅" if engine_config.enabled else "❌",
                    "✅" if api_key_required else "❌"
                )
                
            console.print(table)
            
        except Exception as e:
            logger.error(f"❌ Failed to list engines: {e}")


def main() -> None:
    """Entry point for the CLI."""
    fire.Fire(SearchCLI())


if __name__ == "__main__":
    main()
