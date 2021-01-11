# ehh
Commandline tool for remembering linux/terminal commands. It stores you favorite commands in ```~/ehh.json``` in your homedir and provides an interface for searching and running commands. Provides support for filling in arguments with variables in an interactive way ```(:name)```.

# Installation

```
curl https://raw.githubusercontent.com/lvoogdt/ehh/main/ehh.py -o ehh.py && chmod +x ehh.py
```

Add it to your path:
```
sudo ln -s $(pwd)/ehh.py /usr/local/bin/ehh
```

Install python libs:
```
pip install colorama click
```

If you want to start with some commands you can use the example ehh.json. The commands in this file are linux based.

```
curl https://raw.githubusercontent.com/lvoogdt/ehh/main/ehh.json -o ehh.json && mv ehh.json ~/ehh.json
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
OR
$ ehh INDEX (less typing)
```

Run your command by index. It's also possible to use a query, it will loop through the matches and ask for it to be run.

```
$ ehh get INDEX
```

Get all the details of the command


```
$ ehh rm INDEX
```

Remove command by index
