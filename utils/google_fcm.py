# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import time
from random import uniform
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
# [START get_service_account_tokens]
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


cred = credentials.Certificate(BASE_DIR / 'pharst-care-firebase.json')
access_token_info = cred.get_access_token()

access_token = access_token_info.access_token
expiration_time = access_token_info.expiry

# Attach access_token to HTTPS request in the "Authorization: Bearer" header
# After expiration_time, you must generate a new access token
# [END get_service_account_tokens]

# print('The access token {} expires at {}'.format(access_token, expiration_time))

default_app = firebase_admin.initialize_app(cred)



MAX_RETRIES = 3  # Define the maximum number of retries

# Exponential backoff with jitter
def exponential_backoff(retry_count, min_delay=1.0, max_delay=2.0):
    """Wait with an exponential backoff between retries."""
    delay = min_delay * (2 ** retry_count) + uniform(0, max_delay)
    time.sleep(delay)

def chunk_list_generator(input_list, n):
    # Yield successive n-sized chunks from the input list
    for i in range(0, len(input_list), n):
        yield input_list[i:i + n]


class GoogleFcm():
    def __init__(self):
        pass

    def send_to_token(self, registration_token, notification=None, data=None, options={}):
        # [START send_to_token]
        # This registration token comes from the client FCM SDKs.
        # registration_token = 'YOUR_REGISTRATION_TOKEN'

        # See documentation on defining a message payload.
        # message = messaging.Message(
        #     data={
        #         'score': '850',
        #         'time': '2:45',
        #     },
        #     token=registration_token,
        # )
        message = messaging.Message(
            notification=messaging.Notification(
                        title=notification.get("title"),
                        body=notification.get("body"),
                        image=notification.get("image")
                    ),
                    data=data,
                    android=messaging.AndroidConfig(
                        priority=options.get("priority", "high"),
                        notification=messaging.AndroidNotification(
                            tag=options.get("tag", "ads"),
                            channel_id=options.get("channel", "low_priority"),
                            color=options.get("color"),
                            image=options.get("image"),
                            click_action=options.get("click_action"),
                            icon=options.get("icon")
                        ),
                        ttl=options.get("ttl", 3600)
                    ),
                    apns=messaging.APNSConfig(
                        payload=messaging.APNSPayload(
                            aps=messaging.Aps(
                                sound='high_priority_sound.m4a'
                            )
                        )
                    ),
                    token=registration_token,
        )


        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        # [END send_to_token]
        return response


    def send_to_topic(self,topic):
        # [START send_to_topic]
        # The topic name can be optionally prefixed with "/topics/".
        # topic = 'highScores'

        # See documentation on defining a message payload.
        message = messaging.Message(
            data={
                'score': '850',
                'time': '2:45',
            },
            topic=topic,
        )

        # Send a message to the devices subscribed to the provided topic.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        # [END send_to_topic]
        return response


    def send_to_condition(self):
        # [START send_to_condition]
        # Define a condition which will send to devices which are subscribed
        # to either the Google stock or the tech industry topics.
        condition = "'stock-GOOG' in topics || 'industry-tech' in topics"

        # See documentation on defining a message payload.
        message = messaging.Message(
            notification=messaging.Notification(
                title='$GOOG up 1.43% on the day',
                body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
            ),
            condition=condition,
        )

        # Send a message to devices subscribed to the combination of topics
        # specified by the provided condition.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        # [END send_to_condition]


    def send_dry_run(self):
        message = messaging.Message(
            data={
                'score': '850',
                'time': '2:45',
            },
            token='token',
        )

        # [START send_dry_run]
        # Send a message in the dry run mode.
        response = messaging.send(message, dry_run=True)
        # Response is a message ID string.
        print('Dry run successful:', response)
        # [END send_dry_run]


    def android_message(self):
        # [START android_message]
        message = messaging.Message(
            android=messaging.AndroidConfig(
                ttl=datetime.timedelta(seconds=3600),
                priority='normal',
                notification=messaging.AndroidNotification(
                    title='$GOOG up 1.43% on the day',
                    body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
                    icon='stock_ticker_update',
                    color='#f45342'
                ),
            ),
            topic='industry-tech',
        )
        # [END android_message]
        return message


    def apns_message(self):
        # [START apns_message]
        message = messaging.Message(
            apns=messaging.APNSConfig(
                headers={'apns-priority': '10'},
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        alert=messaging.ApsAlert(
                            title='$GOOG up 1.43% on the day',
                            body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
                        ),
                        badge=42,
                    ),
                ),
            ),
            topic='industry-tech',
        )
        # [END apns_message]
        return message


    def webpush_message(self):
        # [START webpush_message]
        message = messaging.Message(
            webpush=messaging.WebpushConfig(
                notification=messaging.WebpushNotification(
                    title='$GOOG up 1.43% on the day',
                    body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
                    icon='https://my-server/icon.png',
                ),
            ),
            topic='industry-tech',
        )
        # [END webpush_message]
        return message


    def all_platforms_message(self):
        # [START multi_platforms_message]
        message = messaging.Message(
            notification=messaging.Notification(
                title='$GOOG up 1.43% on the day',
                body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
            ),
            android=messaging.AndroidConfig(
                ttl=datetime.timedelta(seconds=3600),
                priority='normal',
                notification=messaging.AndroidNotification(
                    icon='stock_ticker_update',
                    color='#f45342'
                ),
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(badge=42),
                ),
            ),
            topic='industry-tech',
        )
        # [END multi_platforms_message]
        return message


    def subscribe_to_topic(self,topic,registration_tokens):
        # topic = 'highScores'
        # [START subscribe]
        # These registration tokens come from the client FCM SDKs.
        # registration_tokens = [
        #     'YOUR_REGISTRATION_TOKEN_1',
        #     # ...
        #     'YOUR_REGISTRATION_TOKEN_n',
        # ]

        # Subscribe the devices corresponding to the registration tokens to the
        # topic.
        response = messaging.subscribe_to_topic(registration_tokens, topic)
        # See the TopicManagementResponse reference documentation
        # for the contents of response.
        string = f'{response.success_count}tokens were subscribed successfully'
        return string
        # [END subscribe]


    def unsubscribe_from_topic(self,registration_tokens):
        topic = 'highScores'
        # [START unsubscribe]
        # These registration tokens come from the client FCM SDKs.
        # registration_tokens = [
        #     'YOUR_REGISTRATION_TOKEN_1',
        #     # ...
        #     'YOUR_REGISTRATION_TOKEN_n',
        # ]

        # Unubscribe the devices corresponding to the registration tokens from the
        # topic.
        response = messaging.unsubscribe_from_topic(registration_tokens, topic)
        # See the TopicManagementResponse reference documentation
        # for the contents of response.
        print(response.success_count, 'tokens were unsubscribed successfully')
        # [END unsubscribe]


    def send_all(self,registration_token):
        # registration_token = 'YOUR_REGISTRATION_TOKEN'
        # [START send_all]
        # Create a list containing up to 500 messages.
        messages = [
            messaging.Message(
                notification=messaging.Notification('Price drop', '5% off all electronics'),
                token=registration_token,
            ),
            # ...
            messaging.Message(
                notification=messaging.Notification('Price drop', '2% off all books'),
                topic='readers-club',
            ),
        ]

        response = messaging.send_all(messages)
        # See the BatchResponse reference documentation
        # for the contents of response.
        print('{0} messages were sent successfully'.format(response.success_count))
        # [END send_all]




    def send_multicast(self, registration_tokens=[], notification=None, data=None, options={}):
        try:
            responses = []
            chunked = chunk_list_generator(registration_tokens, 500)

            for chunk in chunked:
                message = messaging.MulticastMessage(
                    notification=messaging.Notification(
                        title=notification.get("title"),
                        body=notification.get("body"),
                        image=notification.get("image")
                    ),
                    data=data,
                    android=messaging.AndroidConfig(
                        priority=options.get("priority", "high"),
                        notification=messaging.AndroidNotification(
                            tag=options.get("tag", "ads"),
                            channel_id=options.get("channel", "low_priority"),
                            color=options.get("color"),
                            image=options.get("image"),
                            click_action=options.get("click_action"),
                            icon=options.get("icon")
                        ),
                        ttl=options.get("ttl", 3600)
                    ),
                    apns=messaging.APNSConfig(
                        payload=messaging.APNSPayload(
                            aps=messaging.Aps(
                                sound='high_priority_sound.m4a'
                            )
                        )
                    ),
                    tokens=chunk,
                )

                # Use send_each_for_multicast to send the message to each token individually
                batch_response = messaging.send_each_for_multicast(message)

                failed_tokens = []
                ids = []
                for idx, resp in enumerate(batch_response.responses):
                    if resp.success:
                        ids.append(resp.message_id)
                    else:
                        failed_tokens.append(chunk[idx])  # Add failed tokens to retry list
                        ids.append(None)

                responses.append({
                    "success": batch_response.success_count,
                    "failure": batch_response.failure_count,
                    "ids": ids
                })

                # Retry logic for failed tokens
                retry_count = 0
                while failed_tokens and retry_count < MAX_RETRIES:
                    retry_message = messaging.MulticastMessage(
                        notification=messaging.Notification(
                            title=notification.get("title"),
                            body=notification.get("body"),
                            image=notification.get("image")
                        ),
                        data=data,
                        android=messaging.AndroidConfig(
                            priority=options.get("priority", "high"),
                            notification=messaging.AndroidNotification(
                                tag=options.get("tag", "ads"),
                                channel_id=options.get("channel", "low_priority"),
                                color=options.get("color"),
                                image=options.get("image"),
                                click_action=options.get("click_action"),
                                icon=options.get("icon")
                            ),
                            ttl=options.get("ttl", 3600)
                        ),
                        apns=messaging.APNSConfig(
                            payload=messaging.APNSPayload(
                                aps=messaging.Aps(
                                    sound='high_priority_sound.m4a'
                                )
                            )
                        ),
                        tokens=failed_tokens,  # Resend to failed tokens
                    )

                    retry_batch_response = messaging.send_each_for_multicast(retry_message)

                    # Update failed tokens and retry count
                    failed_tokens = [
                        failed_tokens[i] for i, resp in enumerate(retry_batch_response.responses) if not resp.success
                    ]
                    retry_count += 1

                    retry_ids = [resp.message_id if resp.success else None for resp in retry_batch_response.responses]
                    responses.append({
                        "retry_success": retry_batch_response.success_count,
                        "retry_failure": retry_batch_response.failure_count,
                        "retry_ids": retry_ids
                    })

            return responses
        except Exception as e:
            version = firebase_admin.__version__
            return {"error": str(e) + f"--version: {version}"}




    def send_multicast_and_handle_errors(self,registration_tokens):
        # [START send_multicast_error]
        # These registration tokens come from the client FCM SDKs.
        # registration_tokens = [
        #     'YOUR_REGISTRATION_TOKEN_1',
        #     # ...
        #     'YOUR_REGISTRATION_TOKEN_N',
        # ]

        message = messaging.MulticastMessage(
            data={'score': '850', 'time': '2:45'},
            tokens=registration_tokens,
        )
        response = messaging.send_multicast(message)
        if response.failure_count > 0:
            responses = response.responses
            failed_tokens = []
            for idx, resp in enumerate(responses):
                if not resp.success:
                    # The order of responses corresponds to the order of the registration tokens.
                    failed_tokens.append(registration_tokens[idx])
            print('List of tokens that caused failures: {0}'.format(failed_tokens))
        # [END send_multicast_error]