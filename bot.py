import vk_api
import random
import re
from vk_api.longpoll import VkLongPoll, VkEventType
from config import token

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)

banwords = ['банворд', 'два', 'пидор']
str(banwords)


def sender(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})


def get_name(uid: int) -> str:
    data = vk_session.method("users.get", {"user_ids": uid})[0]
    return "{}".format(data["first_name"])


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.from_chat:
            id = event.chat_id
            msg = event.text.lower()
            if msg in list(banwords):
                max_messages = vk_session.get_api().messages.getHistory(user_id=event.peer_id)['count']
                text = []
                for i in range(0, max_messages, 200):
                    mess = vk_session.get_api().messages.getHistory(user_id=event.peer_id, count=1, offset=i)['items']
                    for element in mess:
                        if element.get('action') == None:
                            text.append(str(element['id']))
                text = ','.join(text)
                print(text)
                vk_session.get_api().messages.delete(delete_for_all=1, message_ids=text)
                sender(id,
                       f'[id{event.user_id}|{get_name(event.user_id)}],в этот раз только предупреждаю, в следующий раз дам БАН)')
