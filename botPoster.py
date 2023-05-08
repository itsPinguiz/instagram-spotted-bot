from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import App

import threading as t
import time,os,io,textwrap
from PIL import Image, ImageDraw, ImageFont

from utilities.instagrapi.types import DirectMessage

TMP_IMG_PATH = "images\\bg_tmp.jpg"
BG_IMG_PATH = "images\\bg.jpg"
FONT = "utilities\\Roboto-Bold.ttf"

class BotPoster(t.Thread):
    def __init__(self,name : str,app : App):
        #data
        super(BotPoster,self).__init__(name=name)
        self._name = name
        self._app = app
        self._running = True
        self._posting = True

        #sync
        self._lock = t.Lock()
        self._updateEvent = t.Event()
        
    def run(self):
        """
        Overrides thread run, keeps posting messages from the queue.
        """
        started = True
        while self._app.getRunning():
            if started:
                print(self.name + " has been started")
                started = not started
            if self._posting:
                if not self._app._messagesToPost.empty():
                    item = self._app._messagesToPost.get()
                    print(f"Posting '{str(item.text)}' : {str(self._app._messagesToPost.qsize()) }  items in queue")
                    # create image from direct text and post it
                    self.text_on_img(text=item.text)
                    self._app._botAPI.photo_upload(os.path.join(os.path.dirname(__file__), TMP_IMG_PATH),"")
                    time.sleep(2)
            else:
                self._updateEvent.wait()
        print(self.name + " has been stopped")

    def text_on_img(self,text : str,filename= BG_IMG_PATH):
        """
        Draw a text on an Image, and saves it
        """
        # find path
        fullPath = os.path.join(os.path.dirname(__file__), filename)
        fullPathTmp = os.path.join(os.path.dirname(__file__), TMP_IMG_PATH)
        fullFontPath = os.path.join(os.path.dirname(__file__), FONT)

        # open files
        fontFile = open(fullFontPath, "rb")
        img = Image.open(fullPath)
        bytesFont = io.BytesIO(fontFile.read())

        #wrap text
        para = textwrap.wrap(text, width=35)

        # create the image with text
        MAXW, _ = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(bytesFont,min(40,int(40*(200/len(text)))))

        currentH, pad = (100 + 10*(200/len(text))), 10
        for line in para:
            w, h = draw.textsize(line, font=font)
            draw.text(((MAXW - w) / 2, currentH), line, font=font)
            currentH += h + pad
        img.save(fullPathTmp)
        return fullPathTmp
    

    def getPosting(self) -> bool:
        """
        Returns posting status
        """
        isPosting = -1
        self._lock.acquire()
        try:
            isPosting = self._posting
        finally:
            self._lock.release()
        return isPosting

    def setPosting(self,status : bool):
        """
        Enables or Disables posting
        """
        success = -1
        self._lock.acquire()
        try:
            self._posting = status
            success = 1
        finally:
            self._lock.release()
        return success
