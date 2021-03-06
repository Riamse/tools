#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python 3.3
# HexChat 2.9.6

__module_name__ = "ZNC Buffextras"
__module_version__ = "1.1"
__module_description__ = "Displays the *buffextra lines from ZNC Buffextra " \
    "module nicely. Python implementation."

import hexchat
hexchat.emit_print("Generic Message", "Loading", "{} {} - {}".format(
                   __module_name__, __module_version__,
                   __module_description__))


def privmsg(word, word_eol, userdata, attrs):

    def send(*args, **kwargs):
        if attrs.time:
            kwargs.setdefault("time", attrs.time)
        return hexchat.emit_print(*args, **kwargs)

    bprefix = word[0]
    if bprefix[0:1] != ':':
        return hexchat.EAT_NONE

    bprefix = bprefix[1:]
    bnick, _, bhost = split_prefix(bprefix)

    if bnick == '*buffextras':
        channel = word[2]
        prefix = word[3][1:]
        _type = word[4]
        args = word_eol[5] if word[5:] else ''

        nick, user, host = split_prefix(prefix)

        if _type == 'set':
            send("Channel Modes", channel, args[6:])
        elif _type == 'joined':
            send("Join", nick, channel, user + "@" + host)
        elif _type == 'parted':
            if args.startswith('with message: ['):
                send("Part with Reason", nick, user + "@" + host, channel,
                                   args[15:-1])
            else:
                send("Part", nick, user + "@" + host, channel)
        elif _type == 'is':
            send("Change Nick", nick, args[13:])
        elif _type == 'quit':
            send("Quit", nick, args[15:-1], user + "@" + host)
        elif _type == 'kicked':
            send("Kick", nick, word[5], channel,
                               word_eol[6][9:-1])
        elif _type == 'changed':
            send("Topic Change", nick, args[14:], channel)
        else:
            send("Server Error", "Unhandled *buffextras event:")
            send("Server Error",
                               "    {}".format(word_eol[3][1:]))
        return hexchat.EAT_HEXCHAT

    return hexchat.EAT_NONE


# extra tools
def split_prefix(prefix):

    if '!' in prefix:
        nick, _, userhostpart = prefix.partition('!')
        user, _, host = userhostpart.partition('@')
    else:
        nick, _, host = prefix.partition('@')
        user = ''

    return (nick, user, host)


hexchat.hook_server_attrs('PRIVMSG', privmsg)
