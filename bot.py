import re
import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, VkChatEventType

# Переменные окружения
TOKEN = os.getenv('TOKEN')
GROUP_ID = os.getenv('GROUP_ID')

vk_session = vk_api.VkApi(token=TOKEN)
long_poll = VkLongPoll(vk_session)

ban_words = ['банворд', 'два', 'пидор']
str(ban_words)

# Роли пользователей в группе, на которых бот не реагирует
super_user_group_roles = ['administrator', 'creator', 'editor']


def send_message(id, text):
    vk_session.get_api().messages.send(chat_id=id, message=text, random_id=0)


def get_name(uid: int) -> str:
    data = vk_session.get_api().users.get(user_ids=uid)[0]
    return "{}".format(data["first_name"])


def is_group_admin(of_group_id, message_owner_id):
    managers = vk_session.get_api().groups.getMembers(group_id=of_group_id, filter='managers').get('items')
    for manager in managers:
        manager_id = manager.get('id')
        manager_role = manager.get('role')
        if manager_id == message_owner_id and manager_role in super_user_group_roles:
            return 1
    return 0


def remove_user_from_chat(from_chat_id, to_user_id):
    vk_session.get_api().messages.removeChatUser(chat_id=from_chat_id, user_id=to_user_id)


def is_group_member(of_group_id, user_id_to_check):
    is_member = vk_session.get_api().groups.isMember(group_id=of_group_id, user_id=user_id_to_check)
    return is_member


def parse_words(text):
    return re.split(r'\s+', text)


def delete_message(event, message_reply):
    vk_session.get_api().messages.delete(delete_for_all=1, message_ids=event.message_id)
    send_message(chat_id, message_reply)


for event in long_poll.listen():
    if event.type == VkEventType.CHAT_UPDATE:
        if event.update_type == VkChatEventType.USER_JOINED:
            joined_user_id = event.info.get('user_id')
            if not is_group_admin(GROUP_ID, joined_user_id):
                if not is_group_member(GROUP_ID, joined_user_id):
                    remove_user_from_chat(event.chat_id, joined_user_id)

    if event.type == VkEventType.MESSAGE_NEW:
        if event.from_chat:
            if not is_group_admin(GROUP_ID, event.user_id):
                chat_id = event.chat_id
                text = event.text.lower()
                words = parse_words(text)

                for word in words:
                    if word in ban_words:
                        delete_message(event,
                                       f'[id{event.user_id}|{get_name(event.user_id)}], вы произнесли слова, которые произносить не следовало. Сейчас мы сделали вид, что не заметили, но в следующий раз мы заберем вас с собой 👽')
                        break
