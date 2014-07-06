'''
Created on 06-Jul-2014

@author: rahul

@summary: Command that will be triggered by our Cron job to find twitter
          updates
'''
from django.core.management.base import BaseCommand
from album.core import SyncService
from album.notification import EmailNotification
from django.conf import settings


class Command(BaseCommand):
    help = 'Updates the #carnival tagged feeds, since last success'

    def handle(self, *args, **options):
        '''
            Handles the update operation. This just triggers and delegate
            its work to SyncService.
        '''
        media_count = SyncService.sync()
        self.notify_updates(media_count)

    def notify_updates(self, media_count):
        '''
            Controls whether to notify the media updates.
        '''
        smtp = settings.SMTP_CONF

        # Connection details
        host = smtp["HOST"]
        port = smtp["PORT"]
        sender = smtp["SENDER"]
        password = smtp["PASSWORD"]

        # Message details
        from_name = smtp["FROM"]
        from_email = smtp["FROM_EMAIL"]
        subject = smtp["SUBJECT"]
        message = smtp["MESSAGE"]
        to = smtp["TO"]
        bcc = smtp["BCC"]

        client = EmailNotification(host, port, sender, password)
        client.send(subject, message, from_name, from_email, to, bcc,
                    count=media_count)
