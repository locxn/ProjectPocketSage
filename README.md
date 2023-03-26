# ProjectPocketTrainer
An activity tracker and motivator to count your calories and track your workouts. It helps you track your progress towards these goals, and once you have reached them, it will send them an encouraging message.
This program is written with a Python base.
New trained data from lobe can be used to replace current tensorflow files.

TO RUN CODE, PLEASE RUN "MainUI.py"

Install:
Twilio - pip3 install twilio
Tkinter - pip install tkinter
lobe - pip install lobe

Import:
import math
from datetime import datetime, timedelta
import os
from twilio.rest import Client
import tkinter
from Pil import Image
import re
from love import ImageModel

Sources:

Site used for formula to calculate recommended daily calorie intake.
https://www.medicalnewstoday.com/articles/245588#daily_needs

Both sites used to calculate oxygen consumption while exercising.
https://www.collegesportsscholarships.com/measure-oxygen-consumption.htm
https://www.whoop.com/thelocker/resting-heart-rate-by-age-and-gender/

Contributors: Loc Nguyen, Justin Vu, Tae Min, Alan Nguyen
