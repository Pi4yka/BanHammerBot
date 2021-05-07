import vk_api
from vk_api.longpoll import VkLongPoll,VkEventType
from config import token
vk_session = vk_api.VkApi(token = token)
longpoll = VkLongPoll(vk_session)


def sender(id, text):
    vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'random_id' : 0})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.from_chat:
                user_id = event.user_id
                msg = event.text.lower()
                id = event.chat_id
                
                if msg in ['банворд']:
                    sender(id,f'{user_id},в этот раз только предупреждаю, в следующий раз дам БАН)')