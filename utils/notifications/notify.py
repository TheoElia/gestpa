from datetime import timezone
from core.models import BGTask
from utils.google_fcm import GoogleFcm


key = "AIzaSyAlcsHh85oz5GYsGMjM3Mgfcrv9-TIn_lI"
officialUrl = "https://www.pharst.care"
per_whatsapp_token = """EAATcxO6KxEcBO1jCWfrMS7jIAddS5cyVX1xcovXguzmzUZBeZBLjMvsVGjCGQZBOEWSHdFEAGF3iHe7G8HDS0HQe6DJtSuu7nkAUPc6LEOArewiy0P5ZCtSlxoiZCqOfQzYEjKFrUuZBZC05kahLuzahSCXCdZBkiGY7tiqM6cW750RuGJZA09fJZCop5EiTphJ2MVY75ZByaEnJl6w2ZBBwguuM"""
app_name = "Pharst Care"
whatsapp_token = per_whatsapp_token


def find_new_elements(new_list, old_list):
    # Convert the old list to a set for faster lookup
    set_old = set(old_list)
    # Find elements that are in new_list but not in old_list
    new_elements = [element for element in new_list if element not in set_old]

    return new_elements


def chunk_list_generator(input_list, n):
    # Yield successive n-sized chunks from the input list
    for i in range(0, len(input_list), n):
        yield input_list[i:i + n]


class Notify:
    def __init__(self):
        pass

    def send_fcm_notification(self,big_payload):
        fcm = GoogleFcm()
        app_name = "Ads"
        resp = {}
        payload = big_payload.get("payload")
        extra = big_payload.get("extra_args")
        tag = extra.get("topic",app_name)
        channel = extra.get("channel","low_priority")
        priority = extra.get("priority","normal")
        data = extra.get("data",{})
        message_title = payload.get('title')
        message_body = payload.get('body')
        message_image = payload.get('image')
        token = big_payload.get("user_token")
        notification = {
                "title":message_title,
                "body":message_body,
                "image":message_image
        }
        options = {
            "channel":channel,
            "tag":tag,
            "priority":priority
        }
        try:

            resp = fcm.send_to_token(registration_token=token,notification=notification,data=data,options=options)
        except Exception as e:
            return e
        return resp

    def send_fcm_notification_multiple(self,big_payload):
        app_name = "Ads"
        payload = big_payload.get("payload")
        reg_ids = big_payload.get("user_tokens")
        extra = big_payload.get("extra_args")
        tag = extra.get("topic",app_name)
        channel = extra.get("channel","low_priority")
        priority = extra.get("priority","normal")
        color = extra.get("color","#017CFF")
        data = extra.get("data",{})
        message_title = payload.get('title')
        message_body = payload.get('body')
        message_image = payload.get('image')
        reg_ids = [i for i in reg_ids if i.strip() != ""]
        notification = {
                "title":message_title,
                "body":message_body,
                "image":message_image
        }
        options = {
            "channel":channel,
            "tag":tag,
            "priority":priority,
            "color":color
        }
        # chunk and create BG Tasks for each
        tasks_created = 0
        chunked = chunk_list_generator(reg_ids, 500)
        for chunk in chunked:
            # args = {
            #     "registration_tokens":chunk,
            #     "notification":notification,
            #     "data":data,
            #     "options":options
            #     }
            try:
                BGTask.objects.create(
                    name='accounts.google_fcm.GoogleFcm.send_multicast',
                    args=[chunk, notification, data,options],  # Arguments for the function
                    execution_time=timezone.now(),  # Run immediately
                    priority='high',  # High priority task
                    max_retries=1,  # Maximum number of retries
                    log="Yet to start\n"
                )
            except Exception as e:
                return str(e)
            else:
                tasks_created += 1
        # try:
        #     resp = fcm.send_multicast(registration_tokens=reg_ids,notification=notification,data=data,options=options)
        # except Exception as e:
        #     return e
        return f"{tasks_created} tasks have been created for this"


    def send_fcm_notification_multiple_immediately(self,big_payload):
        fcm = GoogleFcm()
        app_name = "Ads"
        payload = big_payload.get("payload")
        reg_ids = big_payload.get("user_tokens")
        extra = big_payload.get("extra_args")
        tag = extra.get("topic",app_name)
        channel = extra.get("channel","low_priority")
        priority = extra.get("priority","normal")
        color = extra.get("color","#017CFF")
        data = extra.get("data",{})
        message_title = payload.get('title')
        message_body = payload.get('body')
        message_image = payload.get('image')
        reg_ids = [i for i in reg_ids if i.strip() != ""]
        notification = {
                "title":message_title,
                "body":message_body,
                "image":message_image
        }
        options = {
            "channel":channel,
            "tag":tag,
            "priority":priority,
            "color":color
        }
        try:
            resp = fcm.send_multicast(registration_tokens=reg_ids,notification=notification,data=data,options=options)
        except Exception as e:
            return e
        return resp