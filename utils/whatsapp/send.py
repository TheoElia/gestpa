import requests as r

per_whatsapp_token = """EAATcxO6KxEcBO90NL45LHfzcjcejpsAOh295NZAxxZCUvhZB7LL5OrYl8tCZCzPrpj3ZADRDFyxg7ZAHAovIMDGoNnhFb9KBoZAD5ZAXbQqutfCrAp8pILcY2HYn6E0VtFfs4SdZBqgkbJFnm8BjzX2Q1yrjguUwIcqBaAMAEMA2ETDYttIosOMnoZBAEZCXu92SC97"""
app_name = "Pharst Care"
whatsapp_token = per_whatsapp_token
officialUrl = "https://www.pharst.care"



class WhatsappNotification():
    def send_whatsapp_messages(self,data):
        '''send whatsapp notifications to given contacts'''
        phones = data.get("phones")
        order_id = data.get("order_id")
        urgency = data.get("urgency","Not Flagged")
        template = data.get("template","complaint")
        link = "doctor-consultation-room"
        if template == "order":
            link = "update-call-order"
        url = "https://graph.facebook.com/v15.0/113910455140020/messages"
        headers = {"Authorization":f"Bearer {whatsapp_token}"}
        results = []
        for i in phones:
            params = {
              "messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": i,
              "type": "template",
              "template": {
                "name": template,
                "language": { "code": "en_US" },
                "components": [
                      {
                        "type": "body",
                        "parameters": [
                          {
                            "type": "text",
                            "text": f"{urgency}"
                          },
                          {
                            "type": "text",
                            "text": f"{officialUrl}/health/{link}/{order_id}/"
                          }
                        ]
                      }
                    ]

                }}
            try:
                resp = r.post(url,json=params,headers=headers)
            except Exception as e:
                results.append(e)
            else:
                try:
                    result = resp.json()
                except Exception as e:
                    results.append(e)
                else:
                    results.append(result)
        return results



    def send_otp_whatsapp_message(self,data):
        '''send OTP whatsapp message to new user'''
        phones = data.get("phones")
        otp = data.get("code")
        template = data.get("template","welcome_otp")
        url = "https://graph.facebook.com/v15.0/113910455140020/messages"
        headers = {"Authorization":f"Bearer {whatsapp_token}"}
        results = []
        for i in phones:
            params = {"messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": i,
              "type": "template",
              "template": {
                "name": template,
                "language": { "code": "en_US" },
                "components": [
                  {
                    "type": "body",
                    "parameters": [
                      {
                        "type": "text",
                        "text": otp
                      }
                    ]
                  },
                  {
                    "type": "button",
                    "sub_type": "url",
                    "index": "0",
                    "parameters": [
                      {
                        "type": "text",
                        "text": otp
                      }
                    ]
                  }
                ]

            }}
            try:
                resp = r.post(url,json=params,headers=headers)
            except Exception as e:
                results.append(e)
            else:
                try:
                    result = resp.json()
                except Exception as e:
                    results.append(e)
                else:
                    results.append(result)
        return results


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