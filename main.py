import json

from cryptography.fernet import Fernet
import  requests

API_TOKEN = "<YOUR TOKEN>"
BOT_UPDATE = f"https://api.telegram.org/bot{API_TOKEN}/getUpdates"
BOT_SEND_MESSAGE = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"

while True:
    data = requests.get(BOT_UPDATE).json()
    message_id = data['result'][-1]['message']['message_id']
    from_id = data['result'][-1]['message']['from']['id']
    user_name = data['result'][-1]['message']['from']['username']
    text = data['result'][-1]['message']["text"]


    try:
        with open("messageid.txt",mode="r") as f:
            last_message_id = int(f.readline())
            if last_message_id != message_id:
                f = open("messageid.txt", mode="w")
                f.write(str(message_id))
                f.close()

                try:
                    with open("user_data.json", mode="r") as userdata:
                        udata = json.load(userdata)
                        if (text == "/start"):
                            params = {
                                "chat_id": from_id,
                                "text": "To Encrypt /encrypt \nTo Decrypt /decrypt\n"
                                        "select one of the option bellow.....",
                                "reply_markup":json.dumps({
                                    "keyboard":[
                                        [{"text" : "encrypt"}],
                                        [{"text" : "decrypt"}]
                                    ],
                                    "resize_keyboard" : True
                                })
                            }
                            requests.get(BOT_SEND_MESSAGE,params=params)

                        elif(text == "/encrypt" or text == "encrypt" or text == "/decrypt" or text == "decrypt" ):
                            with open("user_data.json",mode="w") as updata:
                                udata = {from_id:{
                                                "id":str(from_id),
                                                "uname": user_name,
                                                "command": text
                                            }
                                         }
                                json.dump(udata, updata)
                        else:

                            if str(from_id) in udata:
                                command = udata[str(from_id)]["command"]


                                if (command == "encrypt" or command=="/encrypt"):
                                    key = b'<YOUR KEY>'
                                    f = Fernet(key)
                                    en = f.encrypt(bytes(text, 'utf-8'))

                                    params = {
                                        "chat_id": from_id,
                                        "text": str(en)
                                    }
                                    requests.get(BOT_SEND_MESSAGE,params=params)
                                if (command == "decrypt" or command == "/decrypt"):
                                    key = b'<YOUR KEY>'
                                    f = Fernet(key)
                                    try:
                                        de = f.decrypt(bytes(text[1:], 'utf-8'))
                                    except:
                                        de = "invalid command \n" \
                                             "you chose wrong command among /encrypt and /decrypt \n" \
                                             "it was not encrypted by us"

                                    params = {
                                        "chat_id": from_id,
                                        "text": str(de)
                                    }
                                    requests.get(BOT_SEND_MESSAGE, params=params)
                                    # print(en)
                                    # print(text)
                                    # print(en)



                except FileNotFoundError:
                    with open("user_data.json",mode="w") as userdata:
                        sendmessage = f"Welcom {user_name} \n" \
                                      f"To Encrypt /encrypt \nTo Decrypt /decrypt \n" \
                                    f"send the text you want to encrypt or decrypt."
                        params = {
                            "chat_id": from_id,
                            "text": sendmessage,
                            "reply_markup": json.dumps( {
                                "keyboard": [
                                    [{"text": "encrypt"}],
                                    [{"text": "decrypt"}]
                                ],
                                "resize_keyboard": True
                            })
                        }
                        requests.get(BOT_SEND_MESSAGE, params=params)

                        udata = {from_id: {
                            "id": str(from_id),
                            "uname": user_name,
                            "command": ""
                        }
                        }
                        json.dump(udata,userdata)
            else:
                pass

    except FileNotFoundError:
        with open("messageid.txt", mode="w") as f:
            f.write(message_id)
            f.close()






