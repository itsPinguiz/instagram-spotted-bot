from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import App

from time import sleep
import threading as t

from utilities.instagrapi.types import DirectThread,DirectMessage

UPDATE_TIME = 60 # in seconds
KEY_WORD = "spotto" # only select messages with this keyword
MAX_TEXT = 300 # maximum text leght
THREADS_TO_CHECK = 10 # number of unseen threads to check

class BotTimer(t.Thread):
    def __init__(self,name : str,app : App):
        #data
        super(BotTimer,self).__init__(name=name)
        self._name = name
        self._app = app
        self._running = True
        self._updating = True

        #sync
        self._lock = t.Lock()
        self._updateEvent = t.Event()

    def run(self):
        """
        Overrides thread run, keeps updating the queue for new messages to post.
        """
        started = True
        while self._app.getRunning():
            if started:
                print(self.name + " has been started")
                started = not started
            if self._updating and not self._app._messagesToPost.full():
                self.parseNewMessages()
                sleep(UPDATE_TIME)
            else:
                self._updateEvent.wait()
        print(self.name + " has been stopped")

    def parseNewMessages(self):
        """
        Checks bot's unseen messages and filters
        the once we need
        """
        #get new threads
        new_threads = self._app.getUnseenThreads(THREADS_TO_CHECK)        

        #parse threads
        for thread in new_threads:
                message = thread.messages[0]
                # check for the KEY_WORD
                if(message.text and (len(message.text) < MAX_TEXT) and (KEY_WORD in message.text.lower())):
                    # check for banned words and select only the last message
                    if(self._app.checkBannedWords(message) and ((message) not in self._app._messagesToPost.queue)): 
                        self.addToQueue(message)   
    
    def addToQueue(self,d : DirectMessage):
        """
        Adds message to the queue
        """
        self._app._messagesToPost.put(d)
        print(f"Putting '{str(d.text)}' : {str(self._app._messagesToPost.qsize()) }  items in queue")
    
    def getUpdating(self):
        """
        Returns updater status of botTimer
        """
        isUpdating = -1
        self._lock.acquire()
        try:
            isPosting = self._updating
        finally:
            self._lock.release()
        return isUpdating
        
    
    def setUpdating(self,status : bool):
        """
        Sets updating status of botTimer
        """
        success = -1
        self._lock.acquire()
        try:
            self._updating = status
            success = 1
        finally:
            self._lock.release()
        return success
    


    