#!/usr/bin/env python3
"""
Backpack Agent Container System - Main Entry Point

This script provides the CLI interface for managing encrypted agent containers.
Run with --help to see available commands.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli import cli

if __name__ == '__main__':
    cli()