#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["httpx>=0.24.1", "pydantic>=2.0.0", "python-dotenv>=1.0.0", "fire>=0.5.0", "rich>=13.6.0"]
# ///
# this_file: src/twat_search/web/cli.py

"""
CLI tool for performing web searches across multiple engines.

This tool allows you to search the web using various search engines and
displays the results in a formatted table.
"""

import asyncio
import os
import logging
import json as json_lib

# We need to ignore the missing stubs for fire
import fire  # type: ignore
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from twat_search.web.config import Config

# Set up console
console = Console()


class SearchCLI:
    """Web search CLI tool that displays results from multiple search engines."""

    def __init__(self) -> None:
        """Initialize SearchCLI with default logging setup."""
        # Set up logging with rich
        self.log_handler = RichHandler(rich_tracebacks=True)
        logging.basicConfig(
            level=logging.ERROR,  # Default to ERROR level
            format="%(message)s",
            handlers=[self.log_handler],
        )
        self.logger = logging.getLogger(__name__)

        # Load environment variables from .env file
        try:
            from dotenv import load_dotenv

            load_dotenv()
            self.logger.info("Loaded environment variables from .env file")
        except ImportError:
            self.logger.warning("python-dotenv not installed, skipping .env loading")

    def _configure_logging(self, verbose: bool = False) -> None:
        """Configure logging based on verbose flag.

        Args:
            verbose: Whether to show detailed logs
        """
        log_level = (
            logging.INFO if verbose else logging.CRITICAL
        )  # Use CRITICAL to hide all logs

        # Update logger levels
        logging.getLogger().setLevel(log_level)
        self.logger.setLevel(log_level)
        self.log_handler.level = log_level

        # Import modules after setting log level

    def _parse_engines(self, engines_arg: Any) -> list[str] | None:
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
        if isinstance(engines_arg, list | tuple):
            return [str(e).strip() for e in engines_arg if str(e).strip()]

        # Handle unexpected type by logging and returning None
        self.logger.warning(
            f"Unexpected engines type: {type(engines_arg)}. Using all available engines."
        )
        return None

    async def _run_search(
        self, query: str = "president of poland", engines: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """Run search across all available engines.

        Args:
            query: The search term to query
            engines: Optional list of specific engines to use

        Returns:
            List of result dictionaries with engine name, status, and results
        """
        # Import here to ensure logging is configured before import
        from twat_search.web.api import search

        self.logger.info(f"🔍 Searching for: {query}")

        try:
            results = await search(query, engines=engines)
            return self._process_results(results)
        except Exception as e:
            self.logger.error(f"❌ Search failed: {e}")
            return []

    def _process_results(self, results: list) -> list[dict[str, Any]]:
        """Process search results into a standardized format for display.

        Args:
            results: List of SearchResult objects

        Returns:
            Processed results with engine name, status, and formatted data
        """
        processed = []

        # Group results by engine
        engine_results: dict[str, list] = {}
        for result in results:
            # Get engine source from result metadata or use 'unknown'
            engine_name = getattr(result, "source", None) or "unknown"
            if engine_name not in engine_results:
                engine_results[engine_name] = []
            engine_results[engine_name].append(result)

        # Process each engine's results
        for engine, engine_results_list in engine_results.items():
            if not engine_results_list:
                processed.append(
                    {
                        "engine": engine,
                        "status": "❌ No results",
                        "url": "N/A",
                        "title": "N/A",
                        "snippet": "N/A",
                    }
                )
                continue

            # Get the first (top) result
            top_result = engine_results_list[0]
            # Convert URL to string if it's not already
            url = str(top_result.url)
            processed.append(
                {
                    "engine": engine,
                    "status": "✅ Success",
                    "url": url,
                    "title": top_result.title,
                    "snippet": top_result.snippet[:100] + "..."
                    if len(top_result.snippet) > 100
                    else top_result.snippet,
                }
            )

        return processed

    def _display_results(
        self, processed_results: list[dict[str, Any]], verbose: bool = False
    ) -> None:
        """Display search results in a rich table.

        Args:
            processed_results: List of processed result dictionaries
            verbose: Whether to show detailed information
        """
        if not processed_results:
            console.print("[bold red]No results found![/bold red]")
            return

        if verbose:
            # Detailed table for verbose mode
            table = Table(title="🌐 Web Search Results")
            table.add_column("Engine", style="cyan", no_wrap=True)
            table.add_column("Status", style="magenta")
            table.add_column("Title", style="green")
            table.add_column("URL", style="blue")

            for result in processed_results:
                table.add_row(
                    result["engine"], result["status"], result["title"], result["url"]
                )
        else:
            # Simplified table for normal mode - just engine and first result
            table = Table(title="🌐 Web Search Results")
            table.add_column("Engine", style="cyan", no_wrap=True)
            table.add_column("Result", style="green")

            for result in processed_results:
                # Skip failed results in non-verbose mode
                if "❌" in result["status"]:
                    continue

                table.add_row(result["engine"], result["title"])

        console.print(table)

    def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:
        """Display search results in JSON format.

        Args:
            processed_results: List of processed result dictionaries
        """
        # Organize results by engine
        results_by_engine = {}
        for result in processed_results:
            engine = result["engine"]
            results_by_engine[engine] = {
                "status": "success" if "✅" in result["status"] else "error",
                "url": result["url"] if result["url"] != "N/A" else None,
                "title": result["title"] if result["title"] != "N/A" else None,
                "snippet": result["snippet"]
                if result.get("snippet") != "N/A"
                else None,
            }

        # Print JSON output
        console.print(json_lib.dumps(results_by_engine, indent=2))

    def _display_errors(self, error_messages: list[str]) -> None:
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

    def q(
        self,
        query: str = "president of poland",
        engines: Any = None,
        verbose: bool = False,
        json: bool = False,
    ) -> None:
        """Search the web using multiple search engines.

        Args:
            query: The search term (default: "president of poland")
            engines: Search engines to use, specified as a comma-separated string:
                     --engines="brave,google,tavily"
                     If not provided, all available engines will be used.
            verbose: Show detailed information about the search process
            json: Output results in JSON format
        """
        # Configure logging based on verbose flag
        self._configure_logging(verbose)

        # Parse engines argument
        engine_list = self._parse_engines(engines)

        # Run search
        with console.status(f"[bold green]Searching for '{query}'...[/bold green]"):
            results = asyncio.run(self._run_search(query, engine_list))

        # Display results based on format preference
        if json:
            self._display_json_results(results)
        else:
            self._display_results(results, verbose)

        # Print API key information only in verbose mode
        if verbose:
            api_keys = {
                "BRAVE_API_KEY": "✅" if os.environ.get("BRAVE_API_KEY") else "❌",
                "SERPAPI_API_KEY": "✅" if os.environ.get("SERPAPI_API_KEY") else "❌",
                "TAVILY_API_KEY": "✅" if os.environ.get("TAVILY_API_KEY") else "❌",
                "PERPLEXITYAI_API_KEY": "✅"
                if os.environ.get("PERPLEXITYAI_API_KEY")
                else "❌",
                "YOU_API_KEY": "✅" if os.environ.get("YOU_API_KEY") else "❌",
            }

            key_table = Table(title="🔑 API Keys Status")
            key_table.add_column("Service", style="cyan", no_wrap=True)
            key_table.add_column("Status", style="magenta")

            for key, status in api_keys.items():
                key_table.add_row(key.replace("_API_KEY", ""), status)

            console.print(key_table)

    def info(self, engine: str | None = None) -> None:
        """
        Display information about search engines.

        Args:
            engine: Optional specific engine to show details for.
                   If not provided, lists all available engines.
        """
        try:
            # Import here to ensure logging is configured
            from twat_search.web.config import Config

            # Create a temporary config to see available engines
            config = Config()

            if engine is None:
                # List all engines
                self._list_all_engines(config)
            else:
                # Show details for specific engine
                self._show_engine_details(engine, config)

        except Exception as e:
            self.logger.error(f"❌ Failed to display engine information: {e}")

    def _list_all_engines(self, config: "Config") -> None:
        """List all available search engines."""
        table = Table(title="🔎 Available Search Engines")
        table.add_column("Engine", style="cyan", no_wrap=True)
        table.add_column("Enabled", style="magenta")
        table.add_column("API Key Required", style="yellow")

        # Try to get registered engines for more accurate API key requirements
        try:
            from twat_search.web.engines.base import get_registered_engines

            registered_engines = get_registered_engines()
        except ImportError:
            registered_engines = {}

        for engine, engine_config in config.engines.items():
            # First check if the config has an API key set
            api_key_required = (
                hasattr(engine_config, "api_key") and engine_config.api_key is not None
            )

            # If not, check if the engine class has env_api_key_names
            if not api_key_required and engine in registered_engines:
                engine_class = registered_engines.get(engine)
                if engine_class and hasattr(engine_class, "env_api_key_names"):
                    # If the class has non-empty env_api_key_names, it requires an API key
                    api_key_required = bool(engine_class.env_api_key_names)

            table.add_row(
                engine,
                "✅" if engine_config.enabled else "❌",
                "✅" if api_key_required else "❌",
            )

        console.print(table)
        console.print(
            "\n[italic]Run 'info ENGINE_NAME' for more details about a specific engine.[/italic]"
        )

    def _show_engine_details(self, engine_name: str, config: "Config") -> None:
        """Show detailed information about a specific engine."""
        # Check if engine exists in config
        if engine_name not in config.engines:
            console.print(f"[bold red]Engine '{engine_name}' not found![/bold red]")
            console.print("\nAvailable engines:")
            for name in config.engines:
                console.print(f"- {name}")
            return

        # Get engine configuration
        engine_config = config.engines[engine_name]

        # Default API key requirement check
        api_key_required = (
            hasattr(engine_config, "api_key") and engine_config.api_key is not None
        )

        # Try to import the engine class to get more details
        try:
            # Import base engine module
            from twat_search.web.engines.base import get_engine, get_registered_engines

            # Get registered engines to access the class
            registered_engines = get_registered_engines()
            engine_class = registered_engines.get(engine_name)

            # Update API key requirement based on class information
            if (
                not api_key_required
                and engine_class
                and hasattr(engine_class, "env_api_key_names")
            ):
                api_key_required = bool(engine_class.env_api_key_names)

            # Display detailed information
            console.print(f"\n[bold cyan]🔍 Engine: {engine_name}[/bold cyan]")
            console.print(
                f"[bold]Enabled:[/bold] {'✅' if engine_config.enabled else '❌'}"
            )
            console.print(
                f"[bold]API Key Required:[/bold] {'✅' if api_key_required else '❌'}"
            )

            # Show API key environment variables
            if engine_class and hasattr(engine_class, "env_api_key_names"):
                console.print(f"\n[bold]API Key Environment Variables:[/bold]")
                for env_name in engine_class.env_api_key_names:
                    value_status = "✅" if os.environ.get(env_name) else "❌"
                    console.print(f"  {env_name}: {value_status}")

            # Show default parameters
            console.print(f"\n[bold]Default Parameters:[/bold]")
            if engine_config.default_params:
                for param, value in engine_config.default_params.items():
                    console.print(f"  {param}: {value}")
            else:
                console.print("  No default parameters specified")

            # Show function information if available
            try:
                # Determine module name - handle special cases like brave-news → brave
                base_engine = engine_name.split("-")[0]
                module_name = f"twat_search.web.engines.{base_engine}"

                # Try to import the module
                import importlib

                engine_module = importlib.import_module(module_name)

                # Check for function with matching name
                function_name = engine_name.replace("-", "_")
                if hasattr(engine_module, function_name):
                    func = getattr(engine_module, function_name)
                    console.print(f"\n[bold]Function Interface:[/bold]")
                    console.print(
                        f"  [green]{function_name}()[/green] - {func.__doc__.strip().split('\\n')[0]}"
                    )

                    # Show example usage
                    console.print(f"\n[bold]Example Usage:[/bold]")
                    console.print(
                        f"  [italic]from {module_name} import {function_name}[/italic]"
                    )
                    console.print(
                        f'  [italic]results = await {function_name}("your search query")[/italic]'
                    )
            except (ImportError, AttributeError, IndexError):
                # Function might not exist or have different structure
                pass

        except (ImportError, AttributeError) as e:
            # Fallback to basic information if we can't get detailed info
            console.print(
                f"[bold yellow]Could not load detailed engine information: {e}[/bold yellow]"
            )
            console.print("\n[bold]Basic Configuration:[/bold]")
            console.print(f"Enabled: {'✅' if engine_config.enabled else '❌'}")
            console.print(f"Has API Key: {'✅' if engine_config.api_key else '❌'}")
            console.print(f"Default Parameters: {engine_config.default_params}")


def main() -> None:
    """Entry point for the CLI."""
    fire.Fire(SearchCLI())


if __name__ == "__main__":
    main()
