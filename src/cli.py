"""
Command-line interface for Backpack Agent Container System.

This module provides CLI commands for managing agents, keys, and running
agents with JIT variable injection.
"""

import click
import os
import sys
from typing import Dict, Any
from .agent_lock import AgentLock
from .keychain import store_key, get_key, list_keys, register_key, delete_key

@click.group()
def cli():
    """
    Backpack Agent Container CLI.
    
    A secure system for managing AI agents with encrypted state,
    credentials, and personality configurations.
    """
    pass

@cli.command()
@click.option('--credentials', help='Comma-separated list of required credentials (e.g., OPENAI_API_KEY,TWITTER_TOKEN)')
@click.option('--personality', help='Agent personality prompt')
def init(credentials, personality):
    """
    Initialize a new agent.lock file.
    
    Creates an encrypted agent.lock file with credential placeholders
    and personality configuration. This file can be committed to version
    control and shared with your team.
    """
    creds = {}
    if credentials:
        for cred in credentials.split(','):
            creds[cred.strip()] = f"placeholder_{cred.strip().lower()}"
    
    personality_data = {
        "system_prompt": personality or "You are a helpful AI assistant.",
        "tone": "professional"
    }
    
    agent_lock = AgentLock()
    agent_lock.create(creds, personality_data)
    click.echo(f"Created agent.lock with {len(creds)} credential placeholders")

@cli.command()
@click.argument('script_path')
def run(script_path):
    """
    Run an agent with JIT variable injection.
    
    Reads the agent.lock file, prompts for user consent to inject credentials
    from the keychain, and runs the agent script with all variables injected
    into the environment.
    
    Args:
        script_path: Path to the agent Python script to run
    """
    agent_lock = AgentLock()
    agent_data = agent_lock.read()
    
    if not agent_data:
        click.echo("No agent.lock found. Run 'backpack init' first.")
        return
    
    # JIT Variable Injection
    env_vars = {}
    required_keys = agent_lock.get_required_keys()
    
    for key_name in required_keys:
        stored_key = get_key(key_name)
        if stored_key:
            if click.confirm(f"This agent requires access to {key_name}. Allow access?"):
                env_vars[key_name] = stored_key
            else:
                click.echo(f"Access denied for {key_name}. Agent may not function properly.")
        else:
            click.echo(f"Key {key_name} not found in vault. Add it with 'backpack key add {key_name}'")
    
    # Inject personality into environment
    env_vars['AGENT_SYSTEM_PROMPT'] = agent_data['personality']['system_prompt']
    env_vars['AGENT_TONE'] = agent_data['personality']['tone']
    
    # Run the script with injected environment
    for key, value in env_vars.items():
        os.environ[key] = value
    
    click.echo(f"Running {script_path} with {len(env_vars)} injected variables...")
    os.system(f"python {script_path}")

@cli.group()
def key():
    """Manage keys in personal vault"""
    pass

@key.command('add')
@click.argument('key_name')
@click.option('--value', prompt=True, hide_input=True, help='Key value')
def add_key(key_name, value):
    """
    Add a key to personal vault.
    
    Stores a credential in the OS keychain for later use by agents.
    The value is prompted securely (hidden input).
    """
    store_key(key_name, value)
    register_key(key_name)
    click.echo(f"Added {key_name} to vault")

@key.command('list')
def list_keys_cmd():
    """
    List keys in personal vault.
    
    Displays all credential keys registered in the keychain.
    """
    keys = list_keys()
    if keys:
        click.echo("Keys in vault:")
        for key_name in keys:
            click.echo(f"  - {key_name}")
    else:
        click.echo("No keys in vault")

@key.command('remove')
@click.argument('key_name')
def remove_key(key_name):
    """
    Remove a key from personal vault.
    
    Deletes a credential from the OS keychain and registry.
    """
    try:
        delete_key(key_name)
        click.echo(f"Removed {key_name} from vault")
    except Exception as e:
        click.echo(f"Error removing key: {e}")

if __name__ == '__main__':
    cli()