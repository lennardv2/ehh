# ehh

## Remember linux commands
Tired of forgetting bash/linux/osx commands?

Store any command inside ehh. Now you can always find in by typing ```ehh```. It's bash aliasing on steriods.

## Features
https://user-images.githubusercontent.com/168357/185811288-a5767eb8-3da9-46eb-a9a7-5b45fab97513.mp4

* Store commands like ``sudo lsof -iTCP -sTCP:LISTEN -n -P`` (osx) under an alias like ``sys.ports``
* Add a description to your command ``Check Listening Ports``
* Run the command by alias ``ehh sys.ports`` or by index ``ehh 23``
* Show a list of all stored commands by typing ``ehh``
* Filter the list of stored commands by typing ``ehh {query}``. ``ehh sys`` will show all commands in the sys namespace.

https://user-images.githubusercontent.com/168357/185811458-d383212a-dc37-4f46-9abe-bcf708509496.mp4

* Add vars to a commmand by using ``(:var_name)``. For example: ``find "$(pwd)" -name (:search) 2>/dev/null`` will prompt for a search query to search in the current directory (osx)
* All commands are stored inside ``~/ehh.yaml``

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

[![thanks2](https://user-images.githubusercontent.com/168357/104341960-a3b46d80-54fa-11eb-90a4-4295bb815818.png)](https://useplink.com/payment/nJtx7eWuU7QL7QO6czIF/)

# Example

```
$ ehh add
> Command: sudo usermod -a -G (:group) (:user)
> Description: Add a user to a group
> Group (optional):
> Alias (optional): user.group

$ ehh    # Get a list
> 1   sudo usermod -a -G (:group) (:user)     user.group          Add a user to a group

$ ehh 1
> user: john
> group: docker
(Command sudo usermod -a -G docker john is ran)

$ ehh user.group     # Using the lias
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
$ ehh run INDEX|ALIAS
OR
$ ehh INDEX (less typing)
OR
$ ehh ALIAS

if ehh INDEX|ALIAS fails, it return the list filtered by query
```

Run your command by index. It's also possible to use an alias, it will loop through the matches and ask for it to be run.

```
$ ehh get INDEX
```

Get all the details of the command


```
$ ehh rm INDEX
```

Remove command by index


[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Flvoogdt%2Fehh&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
