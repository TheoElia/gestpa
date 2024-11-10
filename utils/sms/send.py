import requests as r
app_name = "Pharst Care"


class SMSNotification():
    def makeGhanaPhone(self, inp):
        ph = inp.strip()
        phone = ph.replace(" ","")
        if phone.startswith("+") and len(phone) == 13:
            newphone = phone.replace("+","",1)
        elif phone.startswith("0") and len(phone) == 10:
            # TODO: Remember to handle more countries here, let caller pass the country name in payload
            newphone = phone.replace("0","233",1)
        elif phone.startswith("O") and len(phone) == 10:
            # TODO: Remember to handle more countries here, let caller pass the country name in payload
            newphone = phone.replace("O","233",1)
        elif phone.startswith("233") and len(phone) == 12:
            newphone = phone
        elif phone == "None":
            newphone = ""
        elif len(phone) == 9:
            newphone = "233"+phone
        else:
             newphone = phone
        return newphone

    def send_infobip_whatsapp(self,data):
        import http.client
        import json
        conn = http.client.HTTPSConnection("mm46m9.api.infobip.com")
        '''send whatsapp notifications to given contacts'''
        phones = data.get("phones")
        order_id = data.get("order_id")
        urgency = data.get("urgency","Not Flagged")
        template = data.get("template","complaint")
        link = "doctor-consultation-room"
        if template == "customer_care_order_alert":
            link = "update-call-order"
        placeholders = data.get("placeholders",[urgency,f"{officialUrl}/health/{link}/{order_id}"])
        # "messageId": "e410492e-9309-4070-b089-dcdbe042ce42",
        messages = []
        for i in phones:
            message = {
                    "from": "447860041164",
                    "to": i,
                    "content": {
                        "templateName": template,
                        "templateData": {
                            "body": {
                                "placeholders": placeholders
                            }
                        },
                        "language": "en_GB"
                    }
                }
            messages.append(message)
        payload = json.dumps({
            "messages": messages
        })
        headers = {
            'Authorization': 'App 4a9c83a8be955ebb749481ffa4d9f6a8-c31d4b81-b513-46fa-bee2-51e5c73406be',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/whatsapp/1/message/template", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")


    def send_infobip_whatsapp_no_args(self,data):
        import http.client
        import json
        conn = http.client.HTTPSConnection("mm46m9.api.infobip.com")
        '''send whatsapp notifications to given contacts'''
        phones = data.get("phones")
        template = data.get("template","complaint")
        messages = []
        for i in phones:
            message = {
                    "from": "447860041164",
                    "to": i,
                    "content": {
                        "templateName": template,
                        "templateData": {
                            "body": {
                                "placeholders": []
                            }
                        },
                        "language": "en_GB"
                    }
                }
            messages.append(message)
        payload = json.dumps({
            "messages": messages
        })
        headers = {
            'Authorization': 'App 4a9c83a8be955ebb749481ffa4d9f6a8-c31d4b81-b513-46fa-bee2-51e5c73406be',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/whatsapp/1/message/template", payload, headers)
        res = conn.getresponse()
        data = res.read()
        f = open("whatsapp_sending_resp.txt","w+")
        f.write(data.decode("utf-8"))
        f.close()
        return data.decode("utf-8")


    def send_infopbip_sms(self,payload,sender_id=app_name):
        try:
            import http.client
            import json

            conn = http.client.HTTPSConnection("mm46m9.api.infobip.com")
            destinations = []
            for i,c in enumerate(payload['phone']):
                phone = self.makeGhanaPhone(c)
                phone_obj = {"to":phone}
                destinations.append(phone_obj)
            body = "From Pharstcare:\n"+ payload['body']
            # .replace("%","perc.").replace(" ","%20").replace("&","and").replace("$","doll.").replace("@","at.").replace("#","%23")
            # body = f"From Pharstcare:\n{body}"
            payload = json.dumps({
                "messages": [
                    {
                        "destinations": destinations,
                        "from": "447860041164",
                        "text": body
                    }
                ]
            })
            headers = {
                'Authorization': 'App 4a9c83a8be955ebb749481ffa4d9f6a8-c31d4b81-b513-46fa-bee2-51e5c73406be',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            conn.request("POST", "/sms/2/text/advanced", payload, headers)
            res = conn.getresponse()
            data = res.read()
        except Exception as e:
            raise e
        return data.decode("utf-8")


    def send_sms(self,payload,sender_id=app_name):
        # self.send_infopbip_sms(payload)
        '''send sms to given phone numbers using Pushr'''
        phones = ""
        error = ""
        for i,c in enumerate(payload['phone']):
            phone = self.makeGhanaPhone(c)
            if i == len(payload['phone'])-1:
                phones += str(phone)
            else:
                phones += str(phone) +","
        body = payload['body'].replace("%","perc.").replace(" ","%20").replace("&","and").replace("$","doll.").replace("@","at.").replace("#","%23")
        url = "https://pushr.pywe.org/bulksender/send-sms-view/?username=Akrasi&public_key=17ac95791e97c3e30cbac5fc99cdd9&sender={}&destination={}&message={}".format(sender_id,phones,body)
        try:
            raw = r.get(url=url)
        except Exception as e:
            error = str(e)
            return error
        else:
            error = raw.text
            resp = raw.json()
            if resp.get("success",False):
                return resp
            else:
                error = resp
                try:
                    self.send_infopbip_sms(payload)
                except Exception as e:
                    raise e
        return error
