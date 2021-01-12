#!/usr/bin/env python3
# http://zetcode.com/python/click/

# pip install colorama click

import sys

try:
    import click
    import colorama
except ImportError:
    sys.exit("""You should run 'pip install colorama click' for this to work""")

import json
from colorama import Fore, Back
import os
import re

__author__ = "Lennard Voogdt"
__version__ = "1.0.1"

commands = []
commandsJsonFile = os.environ['HOME'] + '/ehh.json'


if(os.path.isfile(commandsJsonFile)):
    with open(commandsJsonFile) as f:
        commands = json.load(f)

def trunc(data, max, min = 0):
    return (data[:max] + (data[max:] and '…')).ljust(min)

for command in commands:
    if 'group' not in command:
        command['group'] = ''
    if 'alias' not in command:
        command['alias'] = ''

if (len(commands) > 0):
    maxSize = len(max([trunc(x['command'], 30) for x in commands], key = len))
    maxSizeAlias = len(max([trunc(x['alias'], 100) for x in commands], key = len))
else:
    maxSize = 10
    maxSizeAlias = 0


def groupCommands(cmds):
    values = set(map(lambda x: x['group'], cmds))
    return [[y for y in cmds if y['group']==x] for x in values]

@click.group()
@click.version_option(__version__)
def main():
    """
    Simple CLI for remembering commands
    """
    pass


def echoCommand(command, index):
    click.echo("  " + Fore.MAGENTA + str(index + 1).ljust(3) + " " + Fore.RESET + trunc(command['command'], 30, maxSize) + Fore.GREEN + "  " + command['alias'].ljust(maxSizeAlias) + " " + Fore.LIGHTBLUE_EX  + trunc(command['description'], 30) + "" + Fore.RESET)

def echoCommandBig(command, index):
    click.echo("Id: " + str(index))
    click.echo("Command: " + Fore.MAGENTA + command['command'] + Fore.RESET)
    click.echo("Description: " + Fore.LIGHTBLUE_EX + command['description'] + Fore.RESET)
    click.echo("Group: " + command['group'])
    click.echo("Alias: " + command['alias'])

def echoGroup(group):
    click.echo(" ")

    if (group == ''): return
    click.echo("  " + Fore.WHITE + group + Fore.RESET + ":")

    click.echo(" ")

def execCommand(match):
    command = match['command']

    click.echo("Running: " + Fore.MAGENTA + command + Fore.RESET)
    click.echo("Description: " + Fore.LIGHTBLUE_EX + match['description'] + Fore.RESET)
    click.echo("")

    commandVars = re.findall(r"\(:(.+?)\)",command)
    # Remove dups
    commandVars = list(dict.fromkeys(commandVars))

    for var in commandVars:
        answer = click.prompt(var)
        command = command.replace("(:" + var + ")", answer)

    os.system(command)

@main.command()
@click.argument('query', required=False, default=None)
def ls(query):
    """Find a command by query"""

    if (query != None):
        query = query.lower()

        # Search in commands return list of all matches
        matches = [x for x in commands if ( query in x['alias'].lower() or query in x['command'].lower() or query in x['description'].lower())]
    else:
        matches = commands

    grouped = groupCommands(matches)

    for group in grouped:
        if(len(group) > 0):
            echoGroup(group[0]['group'])
            for match in group:
                echoCommand(match, commands.index(match))
            click.echo(" ")

@main.command()
@click.argument('query')
@click.option('--confirmation/--no-confirmation', '-c/-C', default=None)
def run(query, confirmation):
    """Run commands by alias or id"""

    query = query.lower()

    if (query.isnumeric()):
        if (confirmation == None):
            confirmation = False

        matches = [commands[int(query) - 1]]
    else:
        if (confirmation == None):
            confirmation = False
        # Search in commands return list of all matches
        # matches = [x for x in commands if (query in x['command'].lower()) or (query in x['description'].lower())]
        matches = [x for x in commands if (query == x['alias'])]
    
    for match in matches:
        if (confirmation):
            answer = click.confirm('Run ' + Fore.MAGENTA + match['command'] + Fore.RESET, default=True)

        if (confirmation == False or answer):
            execCommand(match)
            break

@main.command()
def add():
    """Add a command"""

    command = click.prompt("Command")
    description = click.prompt("Description")
    alias = click.prompt("Alias (optional)", default="")

    group = click.prompt("Group (optional)", default="")

    commands.append({
        'command': command,
        'description': description,
        'group': group,
        'alias': alias
    })

    with open(commandsJsonFile, 'w+') as outfile:
        json.dump(commands, outfile, indent=4)

@main.command()
@click.argument('index', type = int)
def rm(index):
    """Remove a command by index"""

    match = commands[index - 1]

    answer = click.confirm('Remove ' + Fore.MAGENTA + match['command'] + Fore.RESET, default=True)

    if answer:
        del commands[index - 1]

    with open(commandsJsonFile, 'w+') as outfile:
        json.dump(commands, outfile, indent=4)


@main.command()
@click.argument('index', type = int)
def get(index):
    """Get a command by index"""

    match = commands[index - 1]

    echoCommandBig(match, index)

if (len(sys.argv) > 1):
    mainArg = sys.argv[1]
    if (mainArg.isnumeric()):
        run.callback(sys.argv[1], False)
        exit()
    else:
        if mainArg not in ["add", "get", "ls", "rm", "run", "--version", "--help"]:
            run.callback(sys.argv[1], False)
            exit()

    

if __name__ == "__main__":
    main()
    
