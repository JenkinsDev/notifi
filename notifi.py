import click
import logging

from os import environ
from os.path import join, dirname
from twilio.rest import Client
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s: %(levelname)s/%(filename)s|%(lineno)s]: %(message)s'
)

logger = logging.getLogger(__name__)


def load_configuration(filename=".env"):
    load_dotenv(join(dirname(__file__), filename))


def text_notification(to_number, from_number, message):
    client = Client(environ.get('TWILIO_ACCOUNT_SID'),
                    environ.get('TWILIO_AUTH_TOKEN'))

    msg = client.messages.create(to=to_number, from_=from_number, body=message)
    logger.debug("Debugging text message. Message SID: {}".format(msg.sid))


def phone_to_us_national_format(phone):
    if not phone.startswith('+1'):
        return '+1%s' % phone

    return phone


@click.command()
@click.option("--should-text/--should-not-text", default=False, help="Send notification via text?")
@click.option("--sms-phone", default=None, help="Phone number to send SMS.")
@click.option("--notifi-msg", default="", help="Notification message to send.")
def notifi_handler(should_text, sms_phone, notifi_msg):
    logger.info("Loading configuration")
    load_configuration()

    if should_text and sms_phone:
        sms_phone = phone_to_us_national_format(sms_phone)
        from_phone = phone_to_us_national_format(
            environ.get('TWILIO_FROM_NUMBER'))

        logger.info('Sending text notification. Phone: {}, Msg: {}'.format(
            sms_phone, notifi_msg))

        text_notification(sms_phone, from_phone, notifi_msg)
    elif should_text and sms_phone == None:
        logger.error("Can't send notification. No --sms-number supplied. Msg: {}".format(
            notifi_msg))


if __name__ == "__main__":
    notifi_handler()
