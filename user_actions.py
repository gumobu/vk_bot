# -*- coding: utf-8 -*-
# This file is dedicated to manage the difficulties with resending images, being logged as a group.
# The code in file includes logging in as vk.com user while being logged as a group in main.py

import data
import vk_api
import random

vk_session = vk_api.VkApi(login=data.data['login'], password=data.data['password'], app_id=2685278)
print('*' * 10 + '\n' + f'LOGGED AS USERWITH LOGIN {data.data["login"]}' + '\n' + '*' * 10)
vk_session.auth()
session_api = vk_session.get_api()


class Pictures:
    @staticmethod
    def get_single(group_id, sesson_api, offset):
        try:
            pictures = sesson_api.photos.get(owner_id=str(group_id), album_id='wall', count=1, offset=offset)['items']
            buf = []  # empty list for pictures links
            for element in pictures:
                buf.append('photo' + str(group_id) + '_' + str(element['id']))  # adds an element of list with the photo id
            attachment = ','.join(buf)
            return attachment
        except:
            return Pictures.get_single(group_id, sesson_api, offset)

    @staticmethod
    def get_multiple(session_api):
        try:
            attachment = ''
            group_id = random.randint(0, len(data.group_ids) - 1)
            max_num = session_api.photos.get(owner_id=data.group_ids[group_id],
                                             album_id='wall', count=0, offset=0)['count']
            # gets the amount of pictures on the public wall
            offset = random.randint(0, max_num)  # gets a pseudo random number for an offset
            pic_count = random.randint(1, 5)  # sets a pseudo random amount of pictures
            pictures = session_api.photos.get(owner_id=data.group_ids[group_id],
                                              album_id='wall', count=pic_count, offset=offset)['items']
            buf = []  # empty list for pictures links
            for element in pictures:
                buf.append('photo' + data.group_ids[group_id] + '_' + str(element['id']))
                # adds an element of list with the photo id
                attachment = ','.join(buf)
            return attachment
        except:
            return Pictures.get_multiple(session_api)
