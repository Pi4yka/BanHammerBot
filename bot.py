import re

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import token, group_id

vk_session = vk_api.VkApi(token=token)
long_poll = VkLongPoll(vk_session)

ban_words = ['банворд', 'два', 'пидор']
str(ban_words)

# Роли пользователей в группе, на которых бот не реагирует
super_user_group_roles = ['administrator', 'creator']


def send_message(id, text):
    vk_session.get_api().messages.send(chat_id=id, message=text, random_id=0)


def get_name(uid: int) -> str:
    data = vk_session.get_api().users.get(user_ids=uid)[0]
    return "{}".format(data["first_name"])


def is_group_admin(group_id, message_owner_id):
    managers = vk_session.get_api().groups.getMembers(group_id=group_id, filter='managers').get('items')
    for manager in managers:
        manager_id = manager.get('id')
        manager_role = manager.get('role')
        if manager_id == message_owner_id and manager_role in super_user_group_roles:
            return 1
    return 0


def parse_words(text):
    return re.split(r'\s+', text)


def delete_message(event, message_reply):
    vk_session.get_api().messages.delete(delete_for_all=1, message_ids=event.message_id)
    send_message(chat_id, message_reply)


for event in long_poll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.from_chat:
            if not is_group_admin(group_id, event.user_id):
                chat_id = event.chat_id
                text = event.text.lower()
                words = parse_words(text)

                for word in words:
                    if word in ban_words:
                        delete_message(event,
                                       f'[id{event.user_id}|{get_name(event.user_id)}], вы произнесли слова, которые произносить не следовало. Сейчас мы сделали вид, что не заметили, но в следующий раз мы заберем вас с собой 👽')
                        break
