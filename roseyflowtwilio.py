# twilio code to send text messages
# pylint: disable-all

#   https://www.twilio.com/docs/twilio-cli/getting-started/install
from flask import Flask, render_template, request
from twilio.rest import Client
import pandas as pd
import math
import csv
from datetime import datetime, timedelta
import time

df = pd.read_csv(r"csv/users.csv")
phone_numbers = df['phoneno'].tolist()
period_dates = df['lastperiod'].tolist()
concat_data = zip(phone_numbers, period_dates)

def message(messageType):
    #messageType = 0;
    # bodyM = "You are entering your Menstruation phase of your Rosey Cycle! Right now, your estrogen and progesterone are low. Don't be afraid to pamper yourself right now...drink herbal teas and limit intake of alcohol, caffeine, and fatty/salty foods. Use slow movements for exercise and get plenty of rest, you deserve it!"
    # bodyF = "You are now entering the Follicular phase of your Rosey Cycle! Right now, your estrogen and progesterone levels are rising. You might notice that you are more energetic and optimistic. Introduce some sprouted and fermented foods into your diet; broccoli and kimchi might do the trick! You might still have some low stamina...light cardio will be your friend!"
    # bodyO = "You are entering the Ovulation phase of your Rosey Cycle! Right now, your estrogen and testosterone levels have peaked. You may feel a range of emotions. Try to eat anti-inflammatory foods and those that promote liver support. Take advantage of the energy that your hormones provide you and try a high intensity workout!"
    #bodyL = "You are now entering your Luteal phase of your Rosey Cycle! Right now, your hormone levels wax and wane; progesterone will increase and testosterone and estrogen will deacrease in the days before your menstruation. You might feel moody or even gross, just know it is all apart of the cycle. Eat foods that will help your seretonin and magnesium levels, like leafy greens and dark chocolate. Try some strength training or intensive yoga to keep up with your changing energy levels!"
    # messages sent to users

    account_sid = 'ACd016caf76c2dd97cf59fb451878f6687'
    auth_token = '5f01cfc1ba93a20a39b7378694714d92'
    client = Client(account_sid, auth_token)

    if messageType == 0:
        message = client.messages.create(
            messaging_service_sid='MGa16982c12b45511c6547beb7e9797ee6',
            body="Thank you for signing up for Rosey Flow! We will track your Rosey Cycle so you don't have to. You'll hear from us when the next phase of your cycle starts! Reply STOP at any time to unsubscribe.",
            to=phone_numbers
        )
        # above is the introduction message

    elif messageType == 1:

        message = client.messages.create(
            messaging_service_sid='MGa16982c12b45511c6547beb7e9797ee6',
            body="You are entering your Menstruation phase of your Rosey Cycle! Right now, your estrogen and progesterone are low. Don't be afraid to pamper yourself right now...drink herbal teas and limit intake of alcohol, caffeine, and fatty/salty foods. Use slow movements for exercise and get plenty of rest, you deserve it!",
            to=phone_numbers
        )
        # above is to send a text message during the Menstruation phase

    elif messageType == 2:
        message = client.messages.create(
            messaging_service_sid='MGa16982c12b45511c6547beb7e9797ee6',
            body="You are now entering the Follicular phase of your Rosey Cycle! Right now, your estrogen and progesterone levels are rising. You might notice that you are more energetic and optimistic. Introduce some sprouted and fermented foods into your diet; broccoli and kimchi might do the trick! You might still have some low stamina...light cardio will be your friend!",
            to=phone_numbers
        )
        # above is to send a text message during the Follicular phase

    elif messageType == 3:

        message = client.messages.create(
            messaging_service_sid='MGa16982c12b45511c6547beb7e9797ee6',
            body="You are entering the Ovulation phase of your Rosey Cycle! Right now, your estrogen and testosterone levels have peaked. You may feel a range of emotions. Try to eat anti-inflammatory foods and those that promote liver support. Take advantage of the energy that your hormones provide you and try a high intensity workout!",
            to=phone_numbers
        )
        # above is to send a text message during the Ovulation phase

    elif messageType == 4:
        message = client.messages.create(
            messaging_service_sid='MGa16982c12b45511c6547beb7e9797ee6',
            body="You are now entering your Luteal phase of your Rosey Cycle! Right now, your hormone levels wax and wane; progesterone will increase and testosterone and estrogen will deacrease in the days before your menstruation. You might feel moody or even gross, just know it is all apart of the cycle. Eat foods that will help your seretonin and magnesium levels, like leafy greens and dark chocolate. Try some strength training or intensive yoga to keep up with your changing energy levels!",
            to=phone_numbers
        )
        # above is to send a text message during the Luteal phase

        print(message.sid)

def next_date_28_days_after(start_date, random_date):
    days_since_start = (random_date - start_date).days
    next_date = random_date + timedelta(days=28 - (days_since_start % 28))
    return next_date

def is_same_day(date):
    today = date.today().strftime("%y-%m-%d")
    return date == today

def main_thread():
    global concat_data # this is bad practice but no time

    while True:
      for data in concat_data:
        datetime_object = datetime.strftime(data[1], '%y-%m-%d')

        current_day = datetime.now()

        next_period = next_date_28_days_after(datetime_object, current_day)

        if is_same_day(next_period): #m
          message(1)
        elif is_same_day(next_period - timedelta(days=23)): #f
          message(2)
        elif is_same_day(next_period - timedelta(days=14)): #o
          message(3)
        elif is_same_day(next_period - timedelta(days=10)): #l
          message(4)

        time.sleep(3600)

# def main():
#   #we need to replace these variables with the user inputed values
#   yy = input("Enter the year you started your last period: ")
#   mm = input("Enter the month you started your last period: ")
#   dd = input("Enter the day you started your last period: ")

#   periodStartDay = currentDay(int(yy), int(mm), int (dd))
#   sendFirstMessage = datetime.datetime.now().timetuple().tm_yday

#   while True: #continuously update current time
#     currentDay = datetime.datetime.now().timetuple().tm_yday
#     time.sleep(1)

#   if sendFirstMessage == currentDay: #welcome to roseyflow
#     message(0)
#   elif (currentDay - periodStartDay)%30 == 0: #m
#     message(1)
#   elif (currentDay - periodStartDay)%30 == 5: #f
#     message(2)
#   elif (currentDay - periodStartDay)%30 == 14: #o
#     message(3)
#   elif (currentDay - periodStartDay)%30 == 15: #l
#     message(4)

# # Finding day of year
# #https://www.mytecbits.com/internet/python/day-of-year
# def currentDay(yy, mm, dd):
#   day_of_year = date(yy, mm, dd).timetuple().tm_yday
#   return day_of_year

if __name__ == "__main__":
    main_thread()
