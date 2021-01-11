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

commands = []
commandsJsonFile = os.environ['HOME'] + '/ehh.json'


if(os.path.isfile(commandsJsonFile)):
    with open(commandsJsonFile) as f:
        commands = json.load(f)

def trunc(data, max, min = 0):
    return (data[:max] + (data[max:] and '…')).ljust(min)

if (len(commands) > 0):
    maxSize = len(max([trunc(x['command'], 40) for x in commands], key = len))
else:
    maxSize = 10

for command in commands:
    if 'group' not in command:
        command['group'] = ''


def groupCommands(cmds):
    values = set(map(lambda x: x['group'], cmds))
    return [[y for y in cmds if y['group']==x] for x in values]

@click.group()
def main():
    """
    Simple CLI for remembering commands
    """
    pass


def echoCommand(command, index):
    click.echo("  " + Fore.MAGENTA + str(index + 1).ljust(3) + " " +  Fore.RESET + trunc(command['command'], 40, maxSize) + Fore.LIGHTBLUE_EX + "    " + trunc(command['description'], 40) + "" + Fore.RESET)

def echoCommandBig(command, index):
    click.echo("Id: " + str(index))
    click.echo("Command: " + Fore.MAGENTA + command['command'] + Fore.RESET)
    click.echo("Description: " + command['description'])
    click.echo("Group: " + command['group'])

def echoGroup(group):
    click.echo(" ")

    if (group == ''): return
    click.echo("  " + Fore.WHITE + group + Fore.RESET + ":")

    click.echo(" ")

def execCommand(command):
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
        matches = [x for x in commands if (query in x['command'].lower()) or (query in x['description'].lower())]
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
    """Run commands by argument or id"""

    query = query.lower()

    if (query.isnumeric()):
        if (confirmation == None):
            confirmation = False

        matches = [commands[int(query) - 1]]
    else:
        if (confirmation == None):
            confirmation = True
        # Search in commands return list of all matches
        matches = [x for x in commands if (query in x['command'].lower()) or (query in x['description'].lower())]
    
    for match in matches:
        if (confirmation):
            answer = click.confirm('Run ' + Fore.MAGENTA + match['command'] + Fore.RESET, default=True)

        if (confirmation == False or answer):
            execCommand(match['command'])
            break

@main.command()
def add():
    """Ad a command"""

    command = click.prompt("Command")
    description = click.prompt("Description")
    group = click.prompt("Group (optional)")

    commands.append({
        'command': command,
        'description': description,
        'group': group
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

if (len(sys.argv) > 1 and sys.argv[1].isnumeric()):
    run.callback(sys.argv[1], False)

    exit()

if __name__ == "__main__":
    main()
    
