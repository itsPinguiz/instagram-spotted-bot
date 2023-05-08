import os,csv
import threading as t
from cryptography.fernet import Fernet

from botConsole import BotConsole
from botTimer import BotTimer
from botPoster import BotPoster
from utilities.bannedWords import BannedWords

from typing import Dict,List
from queue import Queue

from utilities.instagrapi import Client
from utilities.instagrapi.types import UserShort,DirectThread,DirectMessage

IG_USERNAME = "user" # ig passw
IG_PASSWORD = "passw" # ig login
IG_CREDENTIAL_PATH =".\\ig_settings.json" # instagram login specifications
QUEUE_SIZE = 10 # size of the shared queue of messages

"""
Main thread, manages botTimer, botPoster, botConsole
"""
class App:
    def __init__(self):       
        # data
        self._botAPI = Client()
        self._messagesToPost = Queue(QUEUE_SIZE)
        self._botTimer = BotTimer("Timer",self)
        self._botConsole = BotConsole("Console",self)
        self._botPoster= BotPoster("Poster",self)
        self._bannedWords = BannedWords()
        self._running = True

        # sync
        self._botTimerThread = t.Thread(target=self._botTimer.run)
        self._botPosterThread = t.Thread(target=self._botPoster.run)
        self._botConsoleThread = t.Thread(target=self._botConsole.run)
        self._lock = t.Lock()
        
        # login
        if os.path.exists(IG_CREDENTIAL_PATH):
            self._botAPI.load_settings(IG_CREDENTIAL_PATH)
            self._botAPI.login(IG_USERNAME,IG_PASSWORD,"472185")
        else:
            self._botAPI.login(IG_USERNAME,IG_PASSWORD,"472185")
            self._botAPI.dump_settings(IG_CREDENTIAL_PATH)
        
    def run(self):
        # start threads
        self._botTimerThread.start()
        self._botPosterThread.start()
        self._botConsoleThread.start()        
        
        self._botTimerThread.join()
        self._botPosterThread.join()
        self._botConsoleThread.join()

    def getFollowers(self, amount: int = 0) -> Dict[int, UserShort]:
        """
        Get bot's followers
        """
        return self._botAPI.user_followers(self._botAPI.user_id, amount=amount)
    
    def getFollowersUsernames(self, amount: int = 0) -> List[str]:
        """
        Get bot's followers usernames
        """
        followers = self._botAPI.user_followers(self._botAPI.user_id, amount=amount)
        return [user.username for user in followers.values()]

    def getFollowing(self, amount: int = 0) -> Dict[int, UserShort]:
        """
        Get bot's followed users
        """
        return self._botAPI.user_following(self._botAPI.user_id, amount=amount)
    
    def getFollowingUsernames(self, amount: int = 0) -> List[str]:
        """
        Get bot's followed usernames
        """
        following = self._botAPI.user_following(self._botAPI.user_id, amount=amount)
        return [user.username for user in following.values()]

    def getUnseenThreads(self, amount: int = 0) -> List[DirectThread]:
        """
        Get bot's recived messages
        """

        direct = self._botAPI.direct_threads(amount,selected_filter="unread") + self._botAPI.direct_pending_inbox(amount)
        
        for d in direct: # iterate direct threads  
            self._botAPI.direct_send_seen(d.id)
        return direct

    def checkBannedWords(self,message : DirectMessage):
        """
        Checks if there are banned words in the passed string
        """
        toPost = True
        for words in message.text.split():
            if self._bannedWords.isBanned(words):
                toPost = False
        if toPost == False:
            print(f"[{message.user_id}] = was blocked cause message '{message.text}' contains a banned word.")
        return toPost
    
    def setUpdate(self,b : bool) -> bool:
        """
        Starts the botTimer updater
        """
        status = self._botTimer.setUpdating(b)
        if b:
            self._botTimer._updateEvent.set()
        return True if (status == 1) else False

    def postMessages(self):
        """
        After getting a list of read messages lets you
        decide what messages to force the post of
        """
        pass
    
    def setPosting(self,b : bool):
        """
        Enables and Disables botPoster posting
        """
        self._botPoster.setPosting(b)
        if b:
            self._botPoster._updateEvent.set()

    def getBotsStatus(self) -> bool:
        """
        Returns botTimer and botPoster running status
        """
        return (self._botTimer.getRunning(),self._botPoster.getRunning())
    
    def getQueue(self) -> Queue:
        """
        Returns the queue of messages that have to be posted
        """
        return self._messagesToPost

    def shutdown(self):
        """
        Shuts down the whole bot.
        """
        self.setRunning(False)
    
    def getRunning(self):
        """
        Returns universal running state
        """
        isRunning = -1
        self._lock.acquire()
        try:
            isRunning = self._running
        finally:
            self._lock.release()
        return isRunning

    def setRunning(self,status : bool):
        """
        Sets universal running state
        """
        success = -1
        self._lock.acquire()
        try:
            self._running = status
            success = 1
        finally:
            self._lock.release()
        return success
if __name__ == '__main__':
    bot = App()
    bot.run()