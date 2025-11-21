import logging
from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '../../.env'))
# maybe move these to config file?
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
import datetime

logger = logging.getLogger(__name__)


class twilioBase(object):
    def __init__(self, account_sid=TWILIO_SID, auth_token=TWILIO_TOKEN, to_number=None):
        self.client = None
        self.to_number = to_number
        try:
            self.client = Client(account_sid, auth_token)
        except Exception as e:
            logger.error("twilio creation error: {}".format(e))
            return None

    def get_recent_messages(
        self,
        to_number=None,
        text_search=None,
        after_date=None,
        before_date=None,
        msg_count_max=5,
    ):
        if to_number == None:
            to_number = self.to_number
            # search_direction='inbound'
        else:
            self.to_number = to_number
        if not "+" in str(self.to_number):
            search_to_number = "+" + str(self.to_number)
        messages = self.client.messages.list(
            to=search_to_number,
            date_sent=after_date.date(),
            # date_sent_before=before_date,
            limit=msg_count_max,
        )
        print(f"date to check {after_date}")
        messages_returned = []
        timestamped = datetime.datetime.now(datetime.UTC)
        messages = twilioB.get_recent_messages()
        for sms_message in messages:
            if text_search:
                if not text_search in sms_message.body:
                    continue
            if to_number:
                if not sms_message.direction == "inbound":
                    continue
            if sms_message.date_sent < after_date: # .astimezone()
                print(f"date  not after input {sms_message.date_sent}--{sms_message.date_sent.astimezone()}")
                continue
            # messages_returned.append(vars(sms_message)['_properties'])
            messages_returned.append(sms_message.__dict__)
        try:
            sorted_messages = sorted(
                messages_returned, key=lambda x: x["date_sent"], reverse=True
            )
        except:
            sorted_messages = []
        return sorted_messages