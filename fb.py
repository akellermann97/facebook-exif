import json
import datetime
from bs4 import BeautifulSoup
from exif import Image
from exif import DATETIME_STR_FORMAT
from typing import *

"""
In facebook files, there is a main index.html, which then has a bunch of links, one of
which is to "your_messages.html"

Date and times are stored in
<div class="pam _3-95 _2pi0 _2lej uiBoxWhite noborder"> // Major Div
<div class="_3-96 _2pio _2lek _2lel">JOHN SMITH</div> // UserName
<div class="_3-96 _2let"> // Beginning of Message
<img src="messages/stickers_used/47270791_937342239796388_4222599360510164992_n_167788116751808.png" class="_2yuc _3-96"/> // Image tags look like this

<div class="_3-94 _2lem"></div> 
"""


def main():
    apple: str
    image_no: int = 1
    filename = "facebook_dump/facebook/messages/your_messages.html"
    with open(filename, "rb") as facebookfile:
        soup = BeautifulSoup(facebookfile, 'html.parser')
        for div in soup.findAll("div", attrs={'class': 'pam _3-95 _2pi0 _2lej uiBoxWhite noborder'}):
            for link in div.findAll("a"):
                parse_message_threads(link.get("href"))
    return 0


def parse_message_threads(url):
    url = "facebook_dump/facebook/" + url
    photo_url = ""
    date = ""
    filetypes = ["jpg", "jpeg"]
    with open(url, "rb") as message:
        soup_message = BeautifulSoup(message, 'html.parser')
        for item in soup_message.findAll("div", attrs={'class': 'pam _3-95 _2pi0 _2lej uiBoxWhite noborder'}):
            for img in item.findAll("img"):
                photo_url = img.get('src')
                if photo_url is not None:
                    for img in item.findAll("div", attrs={'class': '_3-94 _2lem'}):
                        date = img.text
                        date_obj = datetime.datetime.strptime(
                            date, "%b %d, %Y, %I:%M %p"
                        )

                        if photo_url.split(".")[-1:][0] not in filetypes:
                            print(photo_url.split(".")[-1:][0])
                            print("not jpg.... skipping.")
                            break

                        print(photo_url)
                        print(date_obj)
                        photo_url = "facebook_dump/facebook/" + photo_url

                        try:
                            with open(photo_url, "rb") as image_file_raw:
                                image_file = Image(image_file_raw)

                                image_file.datetime_original = date_obj.strftime(
                                    DATETIME_STR_FORMAT
                                )
                                image_file.datetime_scanned = date_obj.strftime(
                                    DATETIME_STR_FORMAT
                                )
                                image_file.datetime_digitized = date_obj.strftime(
                                    DATETIME_STR_FORMAT
                                )

                                with open("saved_images/{}".format(photo_url.split("/")[-1:][0]), "wb") as new_image:
                                    new_image.write(image_file.get_file())

                        except:
                            pass


if __name__ == "__main__":
    main()
