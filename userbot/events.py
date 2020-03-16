
""" Javes module for managing events.
 One of the main components of the javes. """

import sys
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from os import remove
from time import gmtime, strftime
from traceback import format_exc

from telethon import events

from userbot import bot, BOTLOG_CHATID, LOGSPAMMER

def command(**args):
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    if 1 == 0:
        return print("stupidity at its best")
    else:
        pattern = args.get("pattern", None)
        allow_sudo = args.get("allow_sudo", None)
        allow_edited_updates = args.get('allow_edited_updates', False)
        args["incoming"] = args.get("incoming", False)
        args["outgoing"] = True
        if bool(args["incoming"]):
            args["outgoing"] = False

        try:
            if pattern is not None and not pattern.startswith('(?i)'):
                args['pattern'] = '(?i)' + pattern
        except:
            pass

        reg = re.compile('(.*)')
        if not pattern == None:
            try:
                cmd = re.search(reg, pattern)
                try:
                    cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
                except:
                    pass

                try:
                    CMD_LIST[file_test].append(cmd)
                except:
                    CMD_LIST.update({file_test: [cmd]})
            except:
                pass

        if allow_sudo:
            args["from_users"] = list(Var.SUDO_USERS)
            # Mutually exclusive with outgoing (can only set one of either).
            args["incoming"] = True
        del allow_sudo
        try:
            del args["allow_sudo"]
        except:
            pass

        if "allow_edited_updates" in args:
            del args['allow_edited_updates']

        def decorator(func):
            if allow_edited_updates:
                bot.add_event_handler(func, events.MessageEdited(**args))
            bot.add_event_handler(func, events.NewMessage(**args))
            try:
                LOAD_PLUG[file_test].append(func)
            except:
                LOAD_PLUG.update({file_test: [func]})
            return func

        return decorator


def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import userbot.utils
        import sys
        import importlib
        from pathlib import Path
        path = Path(f"userbot/plugins/{shortname}.py")
        name = "userbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Successfully (re)imported "+shortname)
    else:
        import userbot.utils
        import sys
        import importlib
        from pathlib import Path
        path = Path(f"userbot/plugins/{shortname}.py")
        name = "userbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = bot
        mod.tgbot = bot.tgbot
        mod.Var = Var
        mod.command = command
        mod.logger = logging.getLogger(shortname)
        # support for uniborg
        sys.modules["uniborg.util"] = userbot.utils
        mod.Config = Config
        mod.borg = bot
        # support for paperplaneextended
        sys.modules["userbot.events"] = userbot.utils
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["userbot.plugins."+shortname] = mod
        print("Successfully (re)imported "+shortname)

def register(**args):
    """ Register a new event. """
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    groups_only = args.get('groups_only', False)
    trigger_on_fwd = args.get('trigger_on_fwd', False)
    disable_errors = args.get('disable_errors', False)

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    if "disable_edited" in args:
        del args['disable_edited']

    if "groups_only" in args:
        del args['groups_only']

    if "disable_errors" in args:
        del args['disable_errors']

    if "trigger_on_fwd" in args:
        del args['trigger_on_fwd']

    def decorator(func):
        async def wrapper(check):
            if not LOGSPAMMER:
                send_to = check.chat_id
            else:
                send_to = BOTLOG_CHATID

            if not trigger_on_fwd and check.fwd_from:
                return

            if groups_only and not check.is_group:
                await check.respond("`I don't think this is a group.`")
                return

            try:
                await func(check)

            # Thanks to @kandnub for this HACK.
            # Raise StopPropagation to Raise StopPropagation
            # This needed for AFK to working properly

            except events.StopPropagation:
                raise events.StopPropagation
            # This is a gay exception and must be passed out. So that it doesnt spam chats
            except KeyboardInterrupt:
                pass
            except BaseException:

                # Check if we have to disable it.
                # If not silence the log spam on the console,
                # with a dumb except.

                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**USERBOT ERROR REPORT**\n"
                    text += "Nothing is logged except the fact of error and date\n"

                    ftext = "========== DISCLAIMER =========="
                    ftext += "\nThis file uploaded ONLY here,"
                    ftext += "\nwe logged only fact of error and date,"
                    ftext += "\nwe respect your privacy,"
                    ftext += "\nyou may not report this error if you've"
                    ftext += "\nany confidential data here, no one will see your data\n"
                    ftext += "================================\n\n"
                    ftext += "--------BEGIN JAVES TRACEBACK LOG--------\n"
                    ftext += "\nDate: " + date
                    ftext += "\nChat ID: " + str(check.chat_id)
                    ftext += "\nSender ID: " + str(check.sender_id)
                    ftext += "\n\nEvent Trigger:\n"
                    ftext += str(check.text)
                    ftext += "\n\nTraceback info:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nError text:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------END JAVES TRACEBACK LOG--------"

                    command = "git log --pretty=format:\"%an: %s\" -10"

                    ftext += "\n\n\nLast 10 commits:\n"

                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("error.log", "w+")
                    file.write(ftext)
                    file.close()

                    if LOGSPAMMER:
                        await check.respond("`Javes: Error 404 check log chat!)

                    await check.client.send_file(send_to,
                                                 "error.log",
                                                 caption=text)
                    remove("error.log")
            else:
                pass

        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator
