# -*- coding: utf-8 -*-
""""The main file of a project. Consists of main methods, including logging in as vk.com group"""

import data
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import user_actions
import time
from datetime import datetime, date
import pytz
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard:
    """
    Dedicated to creating keyboard
    """
    def __init__(self, response):
        self.response = response
        self.keyboard = VkKeyboard(one_time=False)

    def create_main(self):
        """
        Creates a keyboard for resending messages to chats
        """
        if self.response == '.логин 12681268':
            self.keyboard.add_button('Отправить сообщение в <Chat1>',
                                     color=VkKeyboardColor.PRIMARY, payload='2')
            self.keyboard.add_line()
            self.keyboard.add_button('Отправить сообщение в <Chat2>',
                                     color=VkKeyboardColor.PRIMARY, payload='3')
            self.keyboard.add_line()
            self.keyboard.add_button('Отмена',
                                     color=VkKeyboardColor.NEGATIVE, payload='1')
        self.keyboard = self.keyboard.get_keyboard()
        return self.keyboard


class Messages:
    """
    Processes messages. Re- and just sends them. Gets picture by using logging in as user
    """
    def __init__(self, peer_id=None, message=None, attachment=None, keyboard=None,
                 vk_session=None, text=None, num=None,
                 event=None,
                 response=None, admin=False):
        self.peer_id = peer_id
        self.message = message
        self.attachment = attachment
        self.keyboard = keyboard
        self.vk_session = vk_session
        self.text = text
        self.num = num
        self.event = event
        self.response = response
        self.admin = admin

    def send(self):
        """
        Sends messages
        """
        session_api.messages.send(peer_id=self.peer_id, message=self.message,
                                  attachment=self.attachment, random_id=random.randint(-2147483648, +2147483648),
                                  keyboard=self.keyboard)

    def resend(self):
        """
        Resends messages
        """
        if self.num == 1:  # Info chat
            return vk_session.method('messages.send', {'peer_id': 2000000003, 'message': self.text,
                                                       'random_id': random.randint(-2147483648, +2147483648)})
        elif self.num == 2:  # Main chat
            return vk_session.method('messages.send', {'peer_id': 2000000002, 'message': self.text,
                                                       'random_id': random.randint(-2147483648, +2147483648)})

    def name_determination(self):
        """
        Determines the first name of the person writing.
        """
        name = session_api.users.get(user_ids=str(self.event.object.message['from_id']))[0]['first_name']
        return name

    @staticmethod
    def payload_determination(event):
        """
        Determines and processes payload of the message
        """
        payload = int(event.message.payload)
        if payload == 1:
            keyboard = VkKeyboard.get_empty_keyboard()
            Messages(peer_id=<AdminId>, message='Выход выполнен', keyboard=keyboard).send()
        if payload == 2:
            keyboard = VkKeyboard.get_empty_keyboard()
            text = session_api.messages.getHistory(peer_id=<AdminId>)['items'][1]['text']
            Messages(peer_id=<AdminId>, message=f'Сообщение с текстом "{text}"'
                                                f' успешно отправлено в беседу СПИДИНФО', keyboard=keyboard).send()
            Messages(vk_session=vk_session, text=text, num=1).resend()
        if payload == 3:
            keyboard = VkKeyboard.get_empty_keyboard()
            text = session_api.messages.getHistory(peer_id=<AdminId>)['items'][1]['text']
            Messages(peer_id=<AdminId>, message=f'Сообщение с текстом "{text}"'
                                                f' успешно отправлено в беседу БАП1901', keyboard=keyboard).send()
            Messages(vk_session=vk_session, text=text, num=2).resend()

    @staticmethod
    def response_determination(admin, response, event, keyboard):
        """
        Determines responses and processes incoming messages
        """
        if admin is False:  # If not a private message from bot owner
            if response == '.команды':  # If not a private message from bot owner
                name = Messages(event=event).name_determination()
                Messages(peer_id=event.message.peer_id,
                         message=f'Привет, {name}! \nВот команды для бота, '
                                 f'их регистр не важен:'
                                 f'\n1) .команды - Список команд бота'
                                 f'\n2) .пара - Информация о текущей и следующих парах (если есть).'
                                 f'\n3) .расп - Актуальное расписание занятий.'
                                 f'\n4) .список - Актуальный список группы.'
                                 f'\n5) .мем - Убогий (смешной) мем'
                                 f'\n6) .дист - Актуальное расписание дистанционных занятий').send()

            elif response == '.пара':  # Sends informations about current and next class
                Messages(peer_id=event.message.peer_id, message=f'{Classes().processing()}').send()

            elif response == '.расп':  # Send a picture of timetable
                Messages(peer_id=event.message.peer_id,
                         message=f'Актуальное на '
                                 f'{DateAndTime().now_cls.strftime("%d.%m.%Y")} расписание ',
                         attachment=user_actions.Pictures.get_single('-' + data.home_id, user_actions.session_api,
                                                                     0)).send()

            elif response == '.список':  # Sends a picture of a group members list
                Messages(peer_id=event.message.peer_id,
                         message=f'Актуальный на {DateAndTime().now_cls.strftime("%d.%m.%Y")} список группы',
                         attachment=user_actions.Pictures.get_single('-' + data.home_id,
                                                                     user_actions.session_api, 1)).send()

            elif response == '.мем':  # Sends funny picture(s)
                Messages(peer_id=event.message.peer_id, message='Ваши мемы прибыли, капитан!',
                         attachment=user_actions.Pictures.get_multiple(user_actions.session_api)).send()

            elif response == '.дист':  # Temporary function. Sends a distance learning timetable
                Messages(peer_id=event.message.peer_id,
                         message=f'Расписание дистанционных занятий,'
                                 f' актуальное на {DateAndTime().now_cls.strftime("%d.%m.%Y")}',
                         attachment=user_actions.Pictures.get_single('-' + data.home_id,
                                                                     user_actions.session_api, 7)).send()

        elif admin is True:  # If the message is private from bot owner
            if response == '.логин 12681268':
                name = Messages(event=event).name_determination()
                Messages(peer_id=event.message.peer_id,
                         message=f'Добро пожаловать, {name}!\n'
                                 f'Чтобы отправить сообщение в одну из бесед, отправь его сюда, '
                                 f'а затем выбери необходимую беседу на клавиатуре',
                         keyboard=keyboard).send()


class DateAndTime:
    """"
    Processes date and time data
    """

    def __init__(self, element_id=None, start=False, time_param=None):
        self.id = element_id
        self.start = start
        self.now_cls = datetime.now(pytz.timezone('Europe/Moscow'))
        self.hour = None
        self.minute, self.hour = 0, 0
        self.current_date = date.today()
        self.time_param = time_param
        self.start_study = datetime.date(datetime.strptime(data.start_study, '%d.%m.%Y'))

    def week_counter(self):
        """
        Calculates the serial number of studying week. Important in my university
        """
        delta = self.current_date - self.start_study
        if delta.days >= 0:
            if int(delta.days) % 7 == 0:
                return int(delta.days / 7)
            elif int(delta.days % 7) != 0:
                return int(delta.days // 7 + 1)

    def get_hour(self):
        """"
        Gets hours count left to start or to the end of the class
        """
        if self.start is False:
            if datetime.strptime(data.end_time[int(self.id)], '%H:%M').replace(tzinfo=None).minute \
                    - self.time_param.replace(tzinfo=None).minute < 0:
                return datetime.strptime(data.end_time[int(self.id)], '%H:%M').replace(tzinfo=None).hour \
                       - self.time_param.replace(tzinfo=None).hour - 1
            else:
                return datetime.strptime(data.end_time[int(self.id)], '%H:%M').replace(tzinfo=None).hour \
                       - self.time_param.replace(tzinfo=None).hour
        else:
            if datetime.strptime(data.start_time[int(self.id)], '%H:%M').replace(tzinfo=None).minute \
                    - self.time_param.replace(tzinfo=None).minute < 0:
                return int(datetime.strptime(data.start_time[int(self.id)], '%H:%M').replace(tzinfo=None).hour) \
                       - self.time_param.replace(tzinfo=None).hour - 1
            else:
                return datetime.strptime(data.start_time[int(self.id)], '%H:%M').replace(tzinfo=None).hour \
                       - self.time_param.replace(tzinfo=None).hour

    def get_minute(self):
        """
        Gets minutes count left to start or to the end of the class
        """
        if self.start is False:
            self.delta_minute = datetime.strptime(data.end_time[int(self.id)], '%H:%M').replace(tzinfo=None).minute \
                                - self.time_param.replace(tzinfo=None).minute
            if self.delta_minute < 0:
                self.delta_minute = 60 - self.time_param.replace(tzinfo=None).minute \
                                    + datetime.strptime(data.end_time[int(self.id)], '%H:%M').replace(
                    tzinfo=None).minute
        else:
            self.delta_minute = datetime.strptime(data.start_time[int(self.id)], '%H:%M').replace(tzinfo=None).minute \
                                - self.time_param.replace(tzinfo=None).minute
            if self.delta_minute < 0:
                self.delta_minute = 60 - self.time_param.replace(tzinfo=None).minute \
                                    + datetime.strptime(data.start_time[int(self.id)],
                                                        '%H:%M').replace(tzinfo=None).minute
        return self.delta_minute

    def time_to(self):
        to_start, to_end = None, None
        if DateAndTime(time_param=self.time_param, start=True, element_id=self.id).get_hour() > 1:
            #  If more than 1 hour left till start
            to_start = True
        elif DateAndTime(start=True, time_param=self.time_param, element_id=self.id).get_hour() == 0 \
                and DateAndTime(time_param=self.time_param, start=True, element_id=self.id).get_minute() >= 0:
            #  If zero hour and more than or zero minutes left till start
            to_start = True
        elif DateAndTime(time_param=self.time_param, element_id=self.id).get_hour() > 0:
            #  If the start time had already passes and more than an hour left till the end
            to_end = True
        elif DateAndTime(time_param=self.time_param, element_id=self.id).get_hour() == 0 \
                and DateAndTime(time_param=self.time_param, element_id=self.id).get_minute() > 0:
            #  If the start time had already passed and less than the end left till start
            to_end = True
        return to_start, to_end


class Classes(DateAndTime):
    """
    Processes all the data, connected with timetable
    """
    def word_hour(self):
        """
        Sets a correct case for hours count
        """
        hour = Classes(time_param=self.time_param, element_id=self.id, start=self.start).get_hour()
        if hour in (1, 21):
            self.add_hour_str = 'час'
        elif hour in (2, 3, 4, 22, 23, 24):
            self.add_hour_str = 'часа'
        else:
            self.add_hour_str = 'часов'
        return str(hour) + ' ' + self.add_hour_str + ' '

    def word_minute(self):
        """
        Sets a correct case for minutes count
        """
        self.minute = Classes(time_param=self.time_param, element_id=self.id, start=self.start).get_minute()
        print(str(self.minute)[-1])
        if str(self.minute).endswith('1') and self.minute != 11:
            self.add_minute_str = 'минута'
        elif str(self.minute).endswith('2' or '3' or '4') and self.minute not in (12, 13, 14):
            self.add_minute_str = 'минуты'
        else:
            self.add_minute_str = 'минут'
        return str(self.minute) + ' ' + self.add_minute_str

    def hurry_up(self):
        """"
        Adds some additional words, depending on the time left to class' start or end
        """
        self.minute = Classes(time_param=self.time_param, element_id=self.id, start=self.start).get_minute()
        self.hour = Classes(time_param=self.time_param, element_id=self.id, start=self.start).get_hour()
        if self.start:
            if self.hour >= 1:
                return ' Врeмени хватает'
            elif 60 > self.minute >= 30:
                return ' Времени хватает. '
            elif 30 > self.minute >= 15:
                return ' Времени на раскачку нет. '
            elif 15 > self.minute >= 5:
                return ' Не прозевай начало. '
            elif 5 > self.minute >= 1:
                return ' Совсем скоро начнется'
            else:
                print(self.minute)
                return ' Осталось меньше минуты. Поторопись!'

        else:
            if self.hour >= 1:
                return 'Пара только началась.'
            elif 60 > self.minute >= 30:
                return 'Осталось совсем недолго!'
            elif 30 > self.minute >= 15:
                return 'Нужно немного подождать.'
            elif 15 > self.minute >= 5:
                return 'Идут последние минуты.'
            elif 5 > self.minute >= 1:
                return 'Остались считанные секунды'
            else:
                return 'Почему ты об этом спрашиваешь?'

    def word_total(self):
        """
        Returns time left till start or end and hurries up
        """
        return Classes(time_param=self.time_param, element_id=self.id, start=self.start).word_hour() +\
               Classes(time_param=self.time_param, element_id=self.id, start=self.start).word_minute() +\
               '. ' + Classes(time_param=self.time_param, element_id=self.id, start=self.start).hurry_up() + '.\n'

    def processing(self):
        """
        Processes the time and date finding out if there is a class right now, which one and which one will be the next
        """
        today = self.now_cls
        day_id = int(self.now_cls.isoweekday())
        start, start_true, end_true = None, False, False
        if DateAndTime().week_counter() <= data.study_weeks_count:
            odd = is_odd(self.week_counter())

            if day_id == (6 or 7):  # If it is saturday or sunday
                if is_odd(DateAndTime().week_counter()) is True:
                    return (f'Сегодня {data.day_names[day_id]}, '
                            f'следующая пара в {data.day_names[1]}. \n'
                            f'Это {data.classes[0]["list_of_classes"][0]}.\n'
                            f'Начнется в {data.start_time[data.classes[0]["num_of_classes"][0]]} \n'
                            f'Можно отдыхать.')
                else:
                    if self.week_counter() < 10:
                        return f'Сегодня {data.day_names[day_id]}, ' \
                               f'следующая пара в {data.day_names[1]}. \n' \
                               f'Это {data.classes[1]["list_of_classes"][1]}.\n' \
                               f'Начнется в {data.start_time[data.classes[1]["num_of_classes"][0]]} \n' \
                               f'Можно отдыхать.'
                    else:
                        return f'Сегодня {data.day_names[day_id]}, ' \
                               f'следующая пара в {data.day_names[1]}. \n' \
                               f'Это {data.classes[1]["list_of_classes"][1]}.\n' \
                               f'Начнется в {data.start_time[data.classes[1]["num_of_classes"][1]]} \n' \
                               f'Можно отдыхать.'

            if day_id == 1:  # If it is monday
                # This block determines the first class serial number starting from zero
                if odd is False:
                    start = 2
                if odd < 10 and is_odd(self.week_counter()) is True:
                    start = 0
                if odd > 9 and is_odd(self.week_counter()) is True:
                    start = 1

                for _ in range(start, len(data.classes[1]["num_of_classes"])):
                    start_true, end_true = DateAndTime(time_param=today, element_id=_).time_to()
                    if start_true or end_true is True:
                        break

                if start_true is True:
                    return f'Следующая пара: {data.classes[1]["list_of_classes"][_]}.\n' \
                           f'До ее начала осталось ' \
                           f'{Classes(time_param=today, element_id=_, start=True).word_total()}'
                elif end_true is True:
                    if _ < len(data.classes[1]["num_of_classes"]) - 1:
                        return f'Текущая пара: {data.classes[1]["list_of_classes"][_]}.\n' \
                               f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n' \
                               f'Следующая пара: {data.classes[1]["list_of_classes"][_ + 1]}.\n' \
                               f'Она начнется в {data.start_time[data.classes[1]["num_of_classes"][_ + 1]]}'
                    elif _ == len(data.classes[1]["num_of_classes"]) - 1:
                        return f'Текущая пара: {data.classes[1]["list_of_classes"][_]}.\n' \
                               f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n' \
                               f'Следующая пара: {data.classes[2]["list_of_classes"][0]}.\n' \
                               f'Завтра в {data.start_time[data.classes[2]["num_of_classes"][0]]}'
                else:
                    return f'На сегодня пары закончились.\n' \
                           f'Следующая пара: {data.classes[2]["list_of_classes"][0]}.\n' \
                           f'В {data.day_names[2]} ' \
                           f'в {data.start_time[data.classes[2]["num_of_classes"][0]]}\n' \
                           f'Можно отдыхать!'

            if day_id == 2:  # If it is tuesday
                start = 0

                for _ in range(start, len(data.classes[2]["num_of_classes"]), 1):
                    start_true, end_true = DateAndTime(time_param=today, element_id=_).time_to()
                    if start_true or end_true is True:
                        break

                if start_true is True:
                    return f'Следующая пара: {data.classes[2]["list_of_classes"][_]}.\n' \
                           f'До ее начала осталось {Classes(time_param=today, element_id=_, start=True).word_total()}'
                elif end_true is True:
                    if _ < len(data.classes[2]["num_of_classes"]) - 1:
                        return f'Текущая пара: {data.classes[2]["list_of_classes"][_]}.\n' \
                               f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n' \
                               f'Следующая пара: {data.classes[2]["list_of_classes"][_ + 1]}.\n' \
                               f'Она начнется в {data.start_time[data.classes[2]["num_of_classes"][_ + 1]]}'
                    elif _ == len(data.classes[2]["num_of_classes"]) - 1:
                        return f'Текущая пара: {data.classes[2]["list_of_classes"][_]}.\n' \
                               f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n' \
                               f'Следующая пара: {data.classes[3]["list_of_classes"][0]}.\n' \
                               f'Завтра в {data.start_time[data.classes[3]["num_of_classes"][0]]}'
                else:
                    return f'На сегодня пары закончились.\n' \
                           f'Следующая пара: {data.classes[3]["list_of_classes"][0]}.\n' \
                           f'Завтра в {data.start_time[data.classes[3]["num_of_classes"][0]]}'

            if day_id == 3:  # If it is wednesday
                start = 0

                if (odd is True and self.week_counter() > 11) or \
                        odd is False:
                    limit = 4
                else:
                    limit = 3
                for _ in range(start, limit):
                    start_true, end_true = DateAndTime(time_param=today, element_id=_).time_to()
                    if start_true or end_true is True:
                        break

                if start_true is True:
                    if odd is True:
                        return f'Следующая пара: {data.classes[4]["list_of_classes"][_]}.\n' \
                               f'До ее начала осталось ' \
                               f'{Classes(time_param=today, element_id=_, start=True).word_total()}'
                    else:
                        return f'Следующая пара: {data.classes[3]["list_of_classes"][_]}.\n' \
                               f'До ее начала осталось ' \
                               f'{Classes(time_param=today, element_id=_, start=True).word_total()}'
                if end_true is True:
                    if _ < limit - 1:
                        if odd is True:
                            return f'Текущая пара: {data.classes[4]["list_of_classes"][_]}.\n' \
                                   f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n' \
                                   f'Следующая пара: {data.classes[4]["list_of_classes"][_ + 1]}.\n' \
                                   f'Она начнется в {data.start_time[data.classes[4]["num_of_classes"][_ + 1]]}'
                        else:
                            return f'Текущая пара: {data.classes[3]["list_of_classes"][_]}.\n' \
                                   f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n' \
                                   f'Следующая пара: {data.classes[3]["list_of_classes"][_ + 1]}.\n' \
                                   f'Она начнется в {data.start_time[data.classes[4]["num_of_classes"][_ + 1]]}'
                    elif _ == limit - 1:
                        if odd is True:
                            if self.week_counter() < 6:
                                return f'Текущая пара: {data.classes[4]["list_of_classes"][_]}.\n' \
                                       f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n'\
                                       f'Следующая пара: {data.classes[5]["list_of_classes"][0]}.\n' \
                                       f'Завтра в {data.start_time[data.classes[5]["num_of_classes"][0]]}'
                            else:
                                return f'Текущая пара: {data.classes[4]["list_of_classes"][_]}.\n' \
                                       f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n'\
                                       f'Следующая пара: {data.classes[6]["list_of_classes"][0]}.\n' \
                                       f'Завтра в {data.start_time[data.classes[6]["num_of_classes"][0]]}'
                        else:
                            if self.week_counter() < 6:
                                return f'Текущая пара: {data.classes[3]["list_of_classes"][_]}.\n' \
                                       f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n'\
                                       f'Следующая пара: {data.classes[5]["list_of_classes"][0]}.\n' \
                                       f'Завтра в {data.start_time[data.classes[5]["num_of_classes"][0]]}'
                            else:
                                return f'Текущая пара: {data.classes[3]["list_of_classes"][_]}.\n' \
                                       f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n'\
                                       f'Следующая пара: {data.classes[6]["list_of_classes"][0]}.\n' \
                                       f'Завтра в {data.start_time[data.classes[6]["num_of_classes"][0]]}'

                else:
                    if self.week_counter() < 6:
                        return f'На сегодня пары закончились.\n' \
                               f'Следующая пара: {data.classes[5]["list_of_classes"][0]}.\n' \
                               f'Завтра в {data.start_time[data.classes[5]["num_of_classes"][0]]}'
                    else:
                        return f'На сегодня пары закончились.\n' \
                               f'Следующая пара: {data.classes[6]["list_of_classes"][0]}.\n' \
                               f'Завтра в {data.start_time[data.classes[6]["num_of_classes"][0]]}'

            if day_id == 4:  # If it is thursday
                start = 1
                for _ in range(start, len(data.classes[5]["num_of_classes"]), 1):
                    start_true, end_true = DateAndTime(time_param=today, element_id=_).time_to()
                    if start_true or end_true is True:
                        break

                if start_true is True:
                    if self.week_counter() < 6:
                        return f'Следующая пара: {data.classes[5]["list_of_classes"][_]}.\n' \
                               f'До ее начала осталось' \
                               f' {Classes(time_param=today, element_id=_, start=True).word_total()}'
                    else:
                        return f'Следующая пара: {data.classes[6]["list_of_classes"][_]}.\n' \
                               f'До ее начала осталось ' \
                               f'{Classes(time_param=today, element_id=_, start=True).word_total()}'
                if end_true is True:
                    if _ < len(data.classes[5]["num_of_classes"]) - 1:
                        if self.week_counter() < 6:
                            return f'Текущая пара: {data.classes[5]["list_of_classes"][_]}.\n' \
                                   f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n' \
                                   f'Следующая пара: {data.classes[5]["list_of_classes"][_ + 1]}.\n' \
                                   f'Она начнется в {data.start_time[data.classes[5]["num_of_classes"][_ + 1]]}'
                        else:
                            return f'Текущая пара: {data.classes[6]["list_of_classes"][_]}.\n' \
                                   f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n' \
                                   f'Следующая пара: {data.classes[6]["list_of_classes"][_ + 1]}.\n' \
                                   f'Она начнется в {data.start_time[data.classes[6]["num_of_classes"][_ + 1]]}'

                    elif _ == len(data.classes[5]["num_of_classes"]) - 1:
                        return f'Текущая пара: {data.classes[5]["list_of_classes"][_]}.\n' \
                               f'До ее конца осталось {Classes(time_param=today).word_total()}\n' \
                               f'Следующая пара: {data.classes[7]["list_of_classes"][0]}.\n' \
                               f'Завтра в {data.start_time[data.classes[7]["num_of_classes"][0]]}.'
                else:
                    return f'На сегодня пары закончились.\n' \
                           f'Следующая пара: {data.classes[7]["list_of_classes"][0]}.\n' \
                           f'Завтра в {data.start_time[data.classes[7]["num_of_classes"][0]]}.'

            if day_id == 5:  # If it is friday
                start = 0

                if (odd is True and self.week_counter() < 11) \
                        or (odd is False and 8 < self.week_counter() < 18):
                    limit = 4
                else:
                    limit = 3

                for _ in range(start, limit):
                    start_true, end_true = DateAndTime(time_param=today, element_id=_).time_to()
                    if start_true or end_true is True:
                        break

                if start_true is True:
                    if odd is True:
                        return f'Следующая пара: {data.classes[8]["list_of_classes"][_]}.\n' \
                               f'До ее начала осталось ' \
                               f'{Classes(time_param=today, element_id=_, start=True).word_total()}'
                    else:
                        return f'Следующая пара: {data.classes[7]["list_of_classes"][_]}.\n' \
                               f'До ее начала осталось ' \
                               f'{Classes(time_param=today, element_id=_, start=True).word_total()}'
                if end_true is True:
                    if _ < limit - 1:
                        if odd is True:
                            return f'Текущая пара: {data.classes[8]["list_of_classes"][_]}.\n' \
                                   f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n' \
                                   f'Следующая пара: {data.classes[8]["list_of_classes"][_ + 1]}.\n' \
                                   f'Она начнется в {data.start_time[data.classes[8]["num_of_classes"][_ + 1]]}'
                        else:
                            return f'Текущая пара: {data.classes[7]["list_of_classes"][_]}.\n' \
                                   f'До ее конца осталось {Classes(time_param=today, element_id=_).word_total()}\n' \
                                   f'Следующая пара: {data.classes[7]["list_of_classes"][_ + 1]}.\n' \
                                   f'Она начнется в {data.start_time[data.classes[7]["num_of_classes"][_ + 1]]}'
                    elif _ == limit - 1:
                        if self.week_counter() < 18:
                            if odd is True:
                                return f'Текущая пара: {data.classes[8]["list_of_classes"][_]}.\n' \
                                       f'До ее конца осталось' \
                                       f' {Classes(time_param=today, element_id=_).word_total()}\n' \
                                       f'Следующая пара: {data.classes[0]["list_of_classes"][0]}.\n' \
                                       f'Начнется в {data.day_names[1]} в ' \
                                       f'{data.start_time[data.classes[1]["num_of_classes"][0]]} \n' \
                                       f'Можно отдыхать.'
                            else:
                                return f'Текущая пара: {data.classes[7]["list_of_classes"][_]}.\n' \
                                       f'До ее конца осталось ' \
                                       f' {Classes(time_param=today, element_id=_).word_total()}\n' \
                                       f'Следующая пара: {data.classes[0]["list_of_classes"][0]}.\n' \
                                       f'Начнется в {data.day_names[1]} в ' \
                                       f'{data.start_time[data.classes[1]["num_of_classes"][0]]} \n' \
                                       f'Можно отдыхать.'
                        elif self.week_counter() == 18:
                            if odd is True:
                                return f'Текущая пара: {data.classes[8]["list_of_classes"][_]}.\n' \
                                       f'До ее конца осталось ' \
                                       f' {Classes(time_param=today, element_id=_).word_total()}\n' \
                                       f'Следующей пары не будет! Это последний учебный день! \n' \
                                       f'Впереди только каникулы и лето, полное открытий.'
                            else:
                                return f'Текущая пара: {data.classes[7]["list_of_classes"][_]}.\n' \
                                       f'До ее конца осталось ' \
                                       f' {Classes(time_param=today, element_id=_).word_total()}\n' \
                                       f'Следующей пары не будет! Это последний учебный день! \n' \
                                       f'Впереди только каникулы и лето, полное открытий.'
                        else:
                            return 'Да сегодня же каникулы! Ты чего? Отдыхай и радуйся жизни, пока молодой.'
                else:
                    if odd is False and self.week_counter() < 10:
                        return f'На сегодня пары закончились.\n' \
                               f'Следующая пара: {data.classes[1]["list_of_classes"][0]}.\n' \
                               f'В {data.day_names[1]} ' \
                               f'в {data.start_time[data.classes[1]["num_of_classes"][0]]}\n' \
                               f'Можно отдыхать!'

                    elif odd is False and self.week_counter() > 9:
                        return f'На сегодня пары закончились.\n' \
                               f'Следующая пара: {data.classes[1]["list_of_classes"][1]}.\n' \
                               f'В {data.day_names[1]} ' \
                               f'в {data.start_time[data.classes[1]["num_of_classes"][1]]}\n' \
                               f'Можно отдыхать!'

                    elif odd is True:
                        return f'На сегодня пары закончились.\n' \
                               f'Следующая пара: {data.classes[0]["list_of_classes"][0]}.\n' \
                               f'В {data.day_names[1]} ' \
                               f'в {data.start_time[data.classes[0]["num_of_classes"][0]]}\n' \
                               f'Можно отдыхать!'


def is_odd(param):  # Finds out if the parameter odd or not
    if param % 2 == 0:
        return True
    else:
        return False


def main(events):  # Main function
    try:
        for event in events.listen():

            if event.type == VkBotEventType.MESSAGE_NEW:  # For messages in chat
                response = event.message.text.lower()
                keyboard = Keyboard(response).create_main()
                if int(event.message.peer_id) != 233071173:
                    Messages().response_determination(admin=False, response=response, event=event, keyboard=keyboard)
                else:
                    Messages().response_determination(admin=True, response=response, event=event, keyboard=keyboard)
                if event.message.payload is not None:
                    Messages.payload_determination(event)
                time.sleep(1)
    except:
        time.sleep(1)
        return main(longpoll)


vk_session = vk_api.VkApi(token=data.token)
session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, data.home_id)
main(longpoll)
