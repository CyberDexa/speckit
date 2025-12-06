"""
Utility functions and classes for Speckit.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
import re

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @classmethod
    def disable(cls):
        """Disable colors for non-TTY output."""
        cls.HEADER = cls.BLUE = cls.CYAN = cls.GREEN = ''
        cls.YELLOW = cls.RED = cls.MAGENTA = cls.BOLD = ''
        cls.DIM = cls.UNDERLINE = cls.END = ''


# Check if we're in a TTY
if not sys.stdout.isatty():
    Colors.disable()


def print_header(text: str, emoji: str = ""):
    """Print a styled header."""
    prefix = f"{emoji} " if emoji else ""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {prefix}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.END}\n")


def print_subheader(text: str, emoji: str = ""):
    """Print a styled subheader."""
    prefix = f"{emoji} " if emoji else ""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'─' * 40}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}  {prefix}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'─' * 40}{Colors.END}\n")


def print_section(text: str, emoji: str = "▸"):
    """Print a section title."""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{emoji} {text}{Colors.END}")


def print_tip(text: str):
    """Print a helpful tip."""
    print(f"{Colors.DIM}  💡 {text}{Colors.END}")


def print_info(text: str):
    """Print info text."""
    print(f"{Colors.CYAN}  ℹ️  {text}{Colors.END}")


def print_success(text: str):
    """Print success message."""
    print(f"\n{Colors.GREEN}✓ {text}{Colors.END}")


def print_warning(text: str):
    """Print warning message."""
    print(f"\n{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_error(text: str):
    """Print error message."""
    print(f"\n{Colors.RED}✗ {text}{Colors.END}")


def print_progress(current: int, total: int, label: str = ""):
    """Print a progress indicator."""
    percentage = (current / total) * 100
    filled = int(percentage / 5)
    bar = "█" * filled + "░" * (20 - filled)
    print(f"\r{Colors.CYAN}  [{bar}] {percentage:.0f}% {label}{Colors.END}", end="", flush=True)
    if current == total:
        print()


def get_input(prompt: str, required: bool = True, multiline: bool = False, 
              default: Optional[str] = None, validator: Optional[callable] = None) -> str:
    """Get input from user with validation support."""
    if default:
        prompt = f"{prompt} [{Colors.DIM}{default}{Colors.END}]"
    
    print(f"{Colors.BLUE}{prompt}{Colors.END}")
    
    if multiline:
        print(f"{Colors.DIM}  (Enter an empty line to finish){Colors.END}")
        lines = []
        while True:
            try:
                line = input("  ")
                if line == "":
                    break
                lines.append(line)
            except EOFError:
                break
        value = "\n".join(lines)
    else:
        try:
            value = input("  → ").strip()
        except EOFError:
            value = ""
    
    if not value and default:
        return default
    
    if required and not value:
        print_error("This field is required. Please try again.")
        return get_input(prompt, required, multiline, default, validator)
    
    if validator and value:
        is_valid, error_msg = validator(value)
        if not is_valid:
            print_error(error_msg)
            return get_input(prompt, required, multiline, default, validator)
    
    return value


def get_choice(prompt: str, options: List[str], allow_multiple: bool = False, 
               default: Optional[int] = None) -> Any:
    """Get a choice from a list of options."""
    print(f"\n{Colors.BLUE}{prompt}{Colors.END}")
    for i, option in enumerate(options, 1):
        default_marker = f" {Colors.DIM}(default){Colors.END}" if default == i else ""
        print(f"  {Colors.CYAN}{i}.{Colors.END} {option}{default_marker}")
    
    if allow_multiple:
        print(f"{Colors.DIM}  (Enter numbers separated by commas, e.g., 1,3,4){Colors.END}")
        try:
            choices = input("  → ").strip()
            if not choices and default:
                return [options[default - 1]]
            indices = [int(x.strip()) - 1 for x in choices.split(",")]
            return [options[i] for i in indices if 0 <= i < len(options)]
        except (ValueError, IndexError):
            return [options[0]] if options else []
    else:
        try:
            choice_input = input("  → ").strip()
            if not choice_input and default:
                return options[default - 1]
            choice = int(choice_input) - 1
            return options[choice] if 0 <= choice < len(options) else options[0]
        except (ValueError, IndexError):
            return options[default - 1] if default else options[0]


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Get a yes/no answer."""
    default_str = "Y/n" if default else "y/N"
    print(f"{Colors.BLUE}{prompt} [{default_str}]{Colors.END}")
    try:
        answer = input("  → ").strip().lower()
    except EOFError:
        answer = ""
    if not answer:
        return default
    return answer in ('y', 'yes', 'true', '1')


def get_rating(prompt: str, max_rating: int = 5) -> int:
    """Get a numerical rating."""
    print(f"{Colors.BLUE}{prompt} (1-{max_rating}){Colors.END}")
    try:
        rating = int(input("  → ").strip())
        return max(1, min(max_rating, rating))
    except (ValueError, EOFError):
        return 3


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


def estimate_complexity(features: List[str], constraints: List[str]) -> str:
    """Estimate project complexity based on features and constraints."""
    score = len(features) + len(constraints) * 0.5
    
    # Check for complexity indicators
    complexity_keywords = ['auth', 'payment', 'real-time', 'sync', 'api', 
                          'database', 'oauth', 'websocket', 'encryption']
    for feature in features:
        feature_lower = feature.lower()
        for keyword in complexity_keywords:
            if keyword in feature_lower:
                score += 2
    
    if score < 5:
        return "Simple"
    elif score < 10:
        return "Moderate"
    elif score < 20:
        return "Complex"
    else:
        return "Enterprise"


def estimate_timeline(complexity: str, phases: int) -> Dict[str, str]:
    """Estimate timeline based on complexity."""
    base_days = {
        "Simple": 1,
        "Moderate": 3,
        "Complex": 7,
        "Enterprise": 14
    }
    
    days_per_phase = base_days.get(complexity, 3)
    total_days = days_per_phase * phases
    
    return {
        "per_phase": f"{days_per_phase} day(s)",
        "total": f"{total_days} day(s)",
        "buffer": f"{int(total_days * 0.2)} day(s)",
        "with_buffer": f"{int(total_days * 1.2)} day(s)"
    }


def format_list(items: List[str], bullet: str = "-", indent: int = 0) -> str:
    """Format a list with bullets."""
    if not items:
        return f"{'  ' * indent}_None defined_"
    prefix = "  " * indent
    return "\n".join(f"{prefix}{bullet} {item}" for item in items)


def format_checklist(items: List[str], indent: int = 0) -> str:
    """Format a checklist with checkboxes."""
    if not items:
        return f"{'  ' * indent}_None defined_"
    prefix = "  " * indent
    return "\n".join(f"{prefix}- [ ] {item}" for item in items)


def format_table(headers: List[str], rows: List[List[str]]) -> str:
    """Format data as a Markdown table."""
    if not headers or not rows:
        return ""
    
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))
    
    # Build table
    lines = []
    header_line = "| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |"
    separator = "| " + " | ".join("-" * w for w in widths) + " |"
    lines.append(header_line)
    lines.append(separator)
    
    for row in rows:
        cells = [str(cell).ljust(widths[i]) if i < len(widths) else str(cell) 
                 for i, cell in enumerate(row)]
        lines.append("| " + " | ".join(cells) + " |")
    
    return "\n".join(lines)


def load_json(filepath: Path) -> Dict[str, Any]:
    """Load JSON file safely."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json(filepath: Path, data: Dict[str, Any], indent: int = 2):
    """Save data to JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def get_timestamp() -> str:
    """Get current timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def get_date() -> str:
    """Get current date string."""
    return datetime.now().strftime("%Y-%m-%d")
