# - *- coding: utf-8 -* -
data = {'login': '<YourLogin>',
        'password': 'YourPassword'}# Login and password of vk.com account
group_ids = ('GroupId1',
             'GroupId2',
             'GroupId3',
             'GroupId4',
             'GroupId5')  # Id's of groups to take memes from (IN NEGATIVE FORM)

token = 'YourGroupToken'  # Token of the group
home_id = 'YourGroupId'  # Your group id. Sometimes used with '-' added before
start_study = '02.02.2020'  # Date the semester starts at
study_weeks_count = 18  # The number of studying weeks

start_time = ('9:30',
              '11:15',
              '13:00',
              '15:15')  # time the classes beginning at
end_time = ('11:05',
            '12:50',
            '14:35',
            '16:45')  # time the classes ending at

day_names = {
    1: 'понедельник',
    2: 'вторник',
    3: 'среда',
    4: 'четверг',
    5: 'пятница',
    6: 'суббота',
    7: 'воскресенье'
}

classes = (
    #  0
    {'day_name': 'Понедельник нечетной недели',  # odd monday
     'list_of_classes': ('ТерМех Пр.з. кабинет 520',
                         'Философия Пр.з. кабинет 318'),
     'num_of_classes': (2, 3)
     # here and further - the serial number of the classes students have this day. Starts from zero
     },
    #  1
    {'day_name': 'Понедельник четной недели',  # even monday
     'list_of_classes': ('ТерМех Лекция кабинет 226',  # only on weeks 1-10
                         'Философия Лекция кабинет 227',
                         'ТерМех Пр.з. кабинет 520',
                         'Философия Пр.з. кабинет 318'),
     'num_of_classes': (0, 1, 2, 3)
     },
    #  2
    {'day_name': 'Вторник',  # tuesday
     'list_of_classes': ('Teхнологии WEB-прогр. Пр.з. Л-506',
                         'Teхнологии WEB-прогр. Лекция кабинет 318'),
     'num_of_classes': (0, 1)
     },
    #  3
    {'day_name': 'Среда нечетной недели',  # odd wednesday
     'list_of_classes': ('Физкультура',
                         'ТерМех Лекция кабинет 226',
                         'Физика Лаб. кабинет 338',
                         'Ин.яз Пр.з. кабинет 216Б'),
     'num_of_classes': (0, 1, 2, 3)
     },
    #  4
    {'day_name': 'Среда четной недели',  # even wednesday
     'list_of_classes': ('Физкультура',
                         'Физика Лекция кабинет 226',
                         'Физика Пр.з. кабинет 515 ',
                         'ТерМех Пр.з. кабинет 509'),  # only on the weeks 12, 14, 16, 18
     'num_of_classes': (0, 1, 2, 3)
     },
    #  5
    {'day_name': 'Четверг 1-5 недели',  # only for the weeks 1-5 thursday
     'list_of_classes': ('Этика дел.общ. Лекция кабинет 227',
                         'Высш.мат. Пр.з. кабинет 314',
                         'Доп.главы мат.анализа кабинет 314'),
     'num_of_classes': (1, 2, 3)
     },
    #  6
    {'day_name': 'Четверг 5+ недели',  # only for the weeks 6-18 thursday
     'list_of_classes': ('Этика дел.общ. Лекция кабинет 227 ',
                         'Высш.мат Пр.з. кабинет 314',
                         'Доп.главы мат.анализа кабинет 314'),
     'num_of_classes': (1, 2, 3)
     },
    #  7
    {'day_name': 'Пятница нечетной недели',  # odd friday
     'list_of_classes': ('Физкультура',
                         'Доп.главы мат.анализа кабинет 308',
                         'Ин.яз Пр.з. кабинет 324',
                         'Доп.главы мат.анализа Пр.з. кабинет 308'),  # only for weeks 9, 11, 13, 15, 17 fridays
     'num_of_classes': (0, 1, 2, 3)
     },
    #  8
    {'day_name': 'Пятница четной недели',  # even friday
     'list_of_classes': ('Физкультура',
                         'Высш.мат Лекция кабинет 504а',
                         'Ин.яз Пр.з. кабинет 324',
                         'Доп.главы мат.анализа Пр.з кабинет 308'),  # only for weeks 2, 4, 6, 8, 10 fridays
     'num_of_classes': (0, 1, 2, 3)
     }
)
