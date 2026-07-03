"""
Module untuk Helper.

Module ini menyediakan fungsi-fungsi helper umum.
"""

import os
from typing import Any


def clear_screen() -> None:
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str) -> None:
    """
    Print formatted header.
    
    Args:
        title: Title to display
    """
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50)


def print_separator() -> None:
    """Print separator line."""
    print("-" * 50)


def pause() -> None:
    """Pause and wait for user input."""
    input("\nTekan Enter untuk melanjutkan...")


def get_input(prompt: str, default: str = None) -> str:
    """
    Get user input with optional default value.
    
    Args:
        prompt: Input prompt
        default: Default value if user presses Enter
        
    Returns:
        User input string
    """
    if default:
        value = input(f"{prompt} [{default}]: ").strip()
        return value if value else default
    return input(f"{prompt}: ").strip()


def get_int_input(prompt: str, default: int = None) -> int:
    """
    Get integer input from user.
    
    Args:
        prompt: Input prompt
        default: Default value
        
    Returns:
        Integer value
        
    Raises:
        ValueError: If input is not a valid integer
    """
    if default is not None:
        value = input(f"{prompt} [{default}]: ").strip()
        if not value:
            return default
        return int(value)
    return int(input(f"{prompt}: ").strip())


def confirm(prompt: str) -> bool:
    """
    Ask user for yes/no confirmation.
    
    Args:
        prompt: Confirmation prompt
        
    Returns:
        True if user confirms, False otherwise
    """
    response = input(f"{prompt} (y/t): ").strip().lower()
    return response in ['y', 'yes', 'ya', 't']


def format_table(data: list[dict[str, Any]], headers: list[str] = None) -> str:
    """
    Format data as a table.
    
    Args:
        data: List of dictionaries to display
        headers: List of column headers (default: dict keys)
        
    Returns:
        Formatted table string
    """
    if not data:
        return "Tidak ada data"
    
    try:
        from tabulate import tabulate
        return tabulate(data, headers="keys" if not headers else headers, tablefmt="grid")
    except ImportError:
        if not headers:
            headers = list(data[0].keys())
        
        col_widths = {h: len(h) for h in headers}
        for row in data:
            for h in headers:
                col_widths[h] = max(col_widths[h], len(str(row.get(h, ""))))
        
        separator = "+" + "+".join(["-" * (col_widths[h] + 2) for h in headers]) + "+"
        header_row = "|" + "|".join([f" {h:<{col_widths[h]}} " for h in headers]) + "|"
        
        result = [separator, header_row, separator]
        for row in data:
            data_row = "|" + "|".join([f" {str(row.get(h, '')):<{col_widths[h]}} " for h in headers]) + "|"
            result.append(data_row)
        result.append(separator)
        
        return "\n".join(result)
