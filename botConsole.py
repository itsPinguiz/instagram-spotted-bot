from __future__ import annotations
from typing import TYPE_CHECKING,List

if TYPE_CHECKING:
    from app import App

import shlex,os,csv,pandas
import threading as t
from utilities.commands import Command,CommandList
from getpass4 import getpass

from utilities.instagrapi.types import DirectMessage

IG_CREDENTIAL_PATH =".\\ig_settings.json"
LOGIN_PATH = ".\\login.csv"

"""
Console thread, manages user inputs
"""
class BotConsole(t.Thread):
    def __init__(self,name : str,app : App):
        #data
        super(BotConsole,self).__init__(name=name)
        self._name = name
        self._app = app
        self._running = True
        self._commandsList = CommandList(self)
    
    def run(self):
        """
        Overrides thread run, keeps checking input messages from the console and executes them.
        """
        started = True
        while self._app.getRunning():
            if started:
                print(self.name + " has been started")
                started = not started
            command, *arguments = shlex.split(input("$ "))
            commandReturnValue = self.runCommands(Command(command,arguments))
            if (commandReturnValue):
                print(commandReturnValue)
        print(self.name + " has been stopped")

    def login(self) -> List[str]:
        """
        TODO : console login with encrypted password
        """
        data = []
        with open(LOGIN_PATH,'r+') as f:
            csv_reader = csv.reader(f)
            df = pandas.read_csv(csv_reader) 
            if df.empty:
                print("============================")
                print("Instagram Login Credentials:")
                print("============================")
                user = input("\tUsername: ")
                passw = getpass("\tPassword: ")
                data.append([user,passw])
                df = pandas.DataFrame(data, columns=['User', 'Passw'])
                df.to_csv(LOGIN_PATH, sep=',')
                f.close()
            else:
                if os.path.exists(IG_CREDENTIAL_PATH):
                    self._app._botAPI.load_settings(IG_CREDENTIAL_PATH)
                    self._app._botAPI.login(df['User'][0],df['User'][1],"472185")
                else:
                    self._app._botAPI.login(user, passw,"472185")
                    self._app._botAPI.dump_settings(IG_CREDENTIAL_PATH)
        
        return (user,passw)

    def runCommands(self,command : Command):
        toRun = self._commandsList.getCommand(command.command)
        if toRun == -1:
            return "Command Not Found"
        else:
            try:
                if command.arguments:
                    return toRun[0](command.arguments)
                else:
                    return toRun[0]()
            except Exception as e:
                print(f"Command wasnt executed due to error:\n {e}")

    def getQueue(self) -> str:
        i = 0
        post = "Queue: \n"
        q = self._app.getQueue()
        for item in q.queue:
            post += f"[{str(i)}]  ({DirectMessage(item).id})'{DirectMessage(item).text}'\n"
            i += 1
        return post

    def getUserMessages(self):
        """
        TODO
        """
        pass

    def blockUser(self,username : str):
        """
        TODO
        """
        pass

    def forceMessagesPost(self):
        """
        TODO
        """
        pass

    def shutdown(self):
        """
        Truns off the bot
        """
        return self._app.shutdown()

    def toggleMessagePosting(self,s : str):
        """
        Toggles botPoster message posting
        """
        if s in "stop":
            self._app.setPosting(False)
            return "Posting Stopped"
        if s in "start":
            self._app.setPosting(True)
            return "Posting Started"
        return "Argument for command 'post' is not valid. Try :'stop','start'"

    def toggleUpdate(self,s : str):
        if s in "stop":
            self._app.setUpdate(False)
            return "Updating Stopped"
        if s in "start":
            self._app.setUpdate(True)
            return "Updating Started"
        return "Argument for command 'update' is not valid. Try :'stop','start'"

    def getCommandsList(self):
        post = "Commands: \n"
        for cmd,v in self._commandsList._commands.items():
            post += f"\t-{cmd} : {v[1]} \n"
        return post

    def getStatus(self):
        s = self._app.getBotsStatus()
        return f"Timer: {str(s[0])} \n Poster: {str(s[1])}"
    
    
    
    
