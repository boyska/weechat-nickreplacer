NickReplacer
==============

This is a script for weechat. It will make some nick appear as another nick,
and add the "proper" items to completion.

I don't think it could have other goals than bullying someone.

Installation
-------------

Apart from copying to `~/.weechat/python/autoload`, the completion must be
configured, adding `|%(replacednicks)` to
`weechat.completion.default_template`.

A sane command could be

```
/set weechat.completion.default_template "%(nicks)|%(irc_channels)|%(replacednicks)"
```


Usage
------

The `/nickreplacer` command is pretty simple to use: you can map old nicks to
"new" nicks, and every new message from _old_ will appear as if it was from
_new_.

