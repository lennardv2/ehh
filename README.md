# ehh
Commandline tool for remembering linux/terminal commands. It stores you favorite commands in ```~/ehh.json``` in your homedir and provides an interface for searching and running commands. Provides support for filling in arguments ```(:name)```.

# Installation

```
wget https://raw.githubusercontent.com/lvoogdt/ehh/main/ehh.py && chmod +x ehh.py
```

Add it to your user bin for example:
```
sudo ln -s $(pwd)/ehh.py /usr/local/bin/ehh
```

# Example

```
$ ehh add
> Command: sudo usermod -a -G (:group) (:user)
> Description: Add a user to a group
> Group (optional):

$ ehh ls
> 1   sudo usermod -a -G (:group) (:user)     Add a user to a group

$ ehh run 1
> user: john
> group: docker
(Command sudo usermod -a -G docker john is ran)

```

# Docs

```
$ ehh add
```

Enter the command you want to store, a description and an optional group.

```
$ ehh ls QUERY?
```

List your commands with an index and description. Add an optional QUERY to filter the list.

```
$ ehh run INDEX|QUERY
```

Run your command by index. It's also possible to use a query, it will loop through the matches and ask for it to be run.

```
$ ehh get INDEX
```

Get all the details of the command

