#!/usr/bin/env python3
# http://zetcode.com/python/click/

# pip install colorama click

import sys
try:
    import click
    import colorama
    import yaml
except ImportError:
    sys.exit("""You should run 'pip install colorama click' for this to work""")

import json
from colorama import Fore, Back, Style
import os
import re

__author__ = "Lennard Voogdt"
__version__ = "1.1.0"

commands = []
commandsYamlFile = os.environ['HOME'] + '/ehh.yaml'
commandsJsonFile = os.environ['HOME'] + '/ehh.json'

if(os.path.isfile(commandsYamlFile)):
    commandsFile = commandsYamlFile
else:
    commandsFile = commandsJsonFile

if (len(sys.argv) > 1 and sys.argv[1] == "--source"):
    if (len(sys.argv) > 2):
        commandsFile = sys.argv[2]
        del sys.argv[1]
        del sys.argv[1]


if(os.path.isfile(commandsFile)):
    with open(commandsFile) as f:
        if ".yaml" in commandsFile:
            commands = yaml.safe_load(f)
        if ".json" in commandsFile:
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
    values = sorted(values)
    cmds = sorted(cmds, key=lambda x:x['alias'])
    groups = [[y for y in cmds if y['group']==x] for x in values]

    return groups

@click.group()
@click.version_option(__version__)
@click.option('--source', help="Path to the ehh.json source", default=None)
def main(source = None):
    """
    Simple CLI for remembering commands
    """
    
    pass


def echoCommand(command, index):
    click.echo("  " + Fore.MAGENTA + str(index + 1).ljust(3) + " " + Fore.RESET + trunc(command['command'], 30, maxSize) + Fore.GREEN + "  " + command['alias'].ljust(maxSizeAlias) + " " + Fore.LIGHTBLUE_EX  + trunc(command['description'], 30) + "" + Fore.RESET)

def echoDefinition(string):
    return Style.DIM + string.ljust(16) + Style.RESET_ALL

def echoCommandBig(command, index):
    click.echo(echoDefinition("Group: ") + command['group'])
    click.echo(echoDefinition("Id: ") + Fore.MAGENTA + str(index) + Fore.RESET)
    click.echo(echoDefinition("Command: ") + Fore.WHITE + command['command'] + Fore.RESET)
    click.echo(echoDefinition("Alias: ") + Fore.GREEN + command['alias'] + Fore.RESET)
    click.echo(echoDefinition("Description: ") + Fore.LIGHTBLUE_EX + command['description'] + Fore.RESET)

def echoGroup(group):
    click.echo(" ")

    if (group == ''): return
    click.echo("  " + Fore.WHITE + group + Fore.RESET + ":")

    click.echo(" ")

def execCommand(match):
    command = match['command']

    click.echo(echoDefinition("Running: ") + Fore.MAGENTA + command + Fore.RESET)
    click.echo(echoDefinition("Description: ") + Fore.LIGHTBLUE_EX + match['description'] + Fore.RESET)
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
def ls(query = None):
    """Find a command by query"""

    if (query != None):
        query = query.lower()

        # Search in commands return list of all matches
        matches = [x for x in commands if (query in x['command'].lower()) 
            or (query in x['description'].lower()) 
            or (query in x['group'].lower()) 
            or (query in x['alias'].lower())]
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
            return
    
    ls.callback(query)
    
  

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

    with open(commandsFile, 'w+') as outfile:
        if ".yaml" in commandsFile:
            yaml.dump(commands, outfile)
        if ".json" in commandsFile:
            json.dump(commands, outfile, indent=4)
        

@main.command()
@click.argument('index', type = int)
def rm(index):
    """Remove a command by index"""

    match = commands[index - 1]

    answer = click.confirm('Remove ' + Fore.MAGENTA + match['command'] + Fore.RESET, default=True)

    if answer:
        del commands[index - 1]

    with open(commandsFile, 'w+') as outfile:
        if ".yaml" in commandsFile:
            yaml.dump(commands, outfile)
        if ".json" in commandsFile:
            json.dump(commands, outfile, indent=4)


@main.command()
@click.argument('index', type = int)
def get(index):
    """Get a command by index"""

    match = commands[index - 1]

    echoCommandBig(match, index)

@main.command()
def help():
    """Get the help"""
    with click.Context(main) as ctx:
        click.echo(main.get_help(ctx))
    return

if (len(sys.argv) > 1):
    mainArg = sys.argv[1]
    if (mainArg.isnumeric()):
        run.callback(sys.argv[1], False)
        exit()
    else:
        if mainArg in ["--version", "--help", "--source"]:
            args = sys.argv[2:]
            main()
        elif mainArg in ["add", "help", "get", "ls", "rm", "run"]:
            args = sys.argv[2:]

            for index, arg in enumerate(args):
                if (arg.isnumeric()):
                    args[index] = int(arg)

            globals()[mainArg].callback(*args)
            exit()
        else:
            run.callback(sys.argv[1], False)
            exit()

if __name__ == "__main__":
    ls()
    
