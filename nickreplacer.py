import json

import weechat


def get_config_json(key):
    return json.loads(weechat.config_get_plugin(key))


def set_config_json(key, val):
    return weechat.config_set_plugin(key, json.dumps(val))


def change_nick(data, modifier, modifier_data, string):
    # only interesting thing is string
    if weechat.buffer_get_string(weechat.current_buffer(),
                                 'localvar_type') != 'channel':
        return string

    msg = weechat.info_get_hashtable("irc_message_parse", {"message": string})
    changes = get_config_json('changes')
    if msg.get('nick', '') in changes:
        return string.replace(msg['nick'], changes[msg['nick']])

    return string


def get_names(userlist):
    if not userlist:
        return []
    l = []
    while weechat.infolist_next(userlist):
        name = weechat.infolist_string(userlist, 'name')
        l.append(name)
    weechat.infolist_free(userlist)
    return l


def get_users_in_cb():
    cb = weechat.current_buffer()
    if weechat.buffer_get_string(cb, 'localvar_type') != 'channel':
        return [weechat.buffer_get_string(cb, 'localvar_channel')]
    users = weechat.infolist_get('nicklist', cb, '')
    return get_names(users)


def complete(data, completion_item, buffer, completion):
    weechat.prnt('', 'printo json')
    changes = get_config_json('changes')
    weechat.prnt('', str(changes))
    users = get_users_in_cb()
    weechat.prnt('', str(users))
    for old, new in changes.items():
        if old in users:
            weechat.hook_completion_list_add(completion, new.encode('utf-8'),
                                             0, weechat.WEECHAT_LIST_POS_SORT)
    return weechat.WEECHAT_RC_OK

weechat.register('nickreplacer', 'boyska', '0.1', 'AGPL3',
                 'Do you hate your mate\' new nick? Me too', '', '')
default_settings = {
    'changes': '{}'
}
for key in default_settings:
    if not weechat.config_is_set_plugin(key):
        weechat.config_set_plugin(key, default_settings[key])


def cmd_cb(data, buffer, args):
    args = args.split()
    if not args:
        return weechat.WEECHAT_RC_ERROR
    changes = get_config_json('changes')
    if args[0] == 'set':
        changes[args[1]] = args[2]
        set_config_json('changes', changes)
        weechat.prnt('', 'replacement for %s set' % args[1])
    elif args[0] == 'unset':
        del changes[args[1]]
    elif args[0] == 'list':
        weechat.prnt('', '%d replacements set:' % len(changes))
        for old, new in changes.items():
            weechat.prnt('', "  %s    %s" % (old, new))
    else:
        weechat.prnt('', 'Invalid subcommand: %s' % args[0])
        return weechat.WEECHAT_RC_ERROR
    return weechat.WEECHAT_RC_OK

weechat.hook_modifier('irc_in_privmsg', 'change_nick', '')
weechat.hook_command('nickreplacer', "Set replacement for nick",
                     '[list] | [set old new] | [unset old]',
                     'Use any subcommand',
                     'set old new'
                     'unset old',
                     'cmd_cb', '')
weechat.hook_completion('replacednicks', "Words in completion list.",
                        'complete', '')
