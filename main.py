import requests
import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption
from telebot.types import InputMediaPhoto, InputMediaVideo
import re
import json
import base64
from binascii import a2b_base64
import urllib
from gh import dororroo


chat_id = []


bot = telebot.TeleBot('5340148482:AAFT4YjSp9Ak-NICmbnLQ_SvsYW8wijqm_I')






encoded = base64.b64encode(open("jfssflss.jpg", "rb").read())
encoded = str(encoded)




encoded = bytes(encoded, encoding="raw_unicode_escape")
encoded = encoded[2:-1]

binary_data = a2b_base64(encoded)

fd = open('vid.mp4', 'wb')
fd.write(binary_data)

fd.close()











def get_level(number):
    with open('levels.json') as le:
        data = dict(json.load(le))
    return data[number][0], data[number][1]


def write_level(m, m1):
    with open('levels.json') as levels:
        data = dict(json.load(levels))
        data['4'] = (m, m1)
    with open('levels.json', 'w') as lv:
        json.dump(data, lv)







@bot.message_handler(commands=["start"])
def start(message, res=False):
    with open('users.json') as le:
        data = dict(json.load(le))
    if not str(message.chat.id) in data.keys():
        data[f'{message.chat.id}'] = {'all_positions': {},
                                      'total_price': 0}
        with open('users.json', 'w') as lv:
            json.dump(data, lv)


    print(message.chat.id)
    res = requests.get('https://serverfor10000.herokuapp.com/api/sorted_keys')
    # res = {'q': [',fyfys', 'заборы', 'дома', 'груши']}
    categ = res.json()['q']
    print(categ)

    markup_category = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup_category.add(types.KeyboardButton('Посмотреть корзину'))

    for i in categ:
        markup_category.add(types.KeyboardButton(i))

    r = bot.send_message(message.chat.id, 'Выберити категорию', reply_markup=markup_category)

    bot.register_next_step_handler(r, caregory_check, categ)



markup_registration = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_r = types.KeyboardButton("Создать анкету")
markup_registration.add(btn_r)

markup_position = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_pos1 = types.KeyboardButton('\ud83d\udd39 \ud83d\uded2 Добавить в корзину \ud83d\uded2 \ud83d\udd39')
btn_pos2 = types.KeyboardButton('\ud83d\udec2 Вернутся к позициям \ud83d\udec2')
btn_pos3 = types.KeyboardButton('\ud83d\udec2 Вернутся к выбору категории \ud83d\udec2') #	&#128259;     &#128260;
markup_position.add(btn_pos1)
markup_position.add(btn_pos2)
markup_position.add(btn_pos3)


markup_chek = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_chek = types.KeyboardButton('Посмотреть анкету')
markup_chek.add(btn_chek)



markup_send = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_send1 = types.KeyboardButton("Отправить на проверку")
btn_send2 = types.KeyboardButton("Создать заново")
markup_send.add(btn_send1, btn_send2)


markup_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1_admin = types.KeyboardButton('Добавить анкету')
btn2_admin = types.KeyboardButton('Отклонить анкету')
markup_admin.add(btn2_admin, btn1_admin)





@bot.message_handler(content_types=["text"])
def func(message):
    if message.text == '\ud83d\udec2 Вернутся к выбору категории \ud83d\udec2':
        start(message.chat.id)




def caregory_check(message, categories):
    if message.text in categories:
        res = requests.get(f'https://serverfor10000.herokuapp.com/api/get_position/{message.text}').json()['position']


        #res = {'Банан': '32524545', 'Кола': '54345345', 'Яблоки': '5435', 'Чай': '234324', 'Жопаа': '534345', 'Кефир': '234234234', 'Соль': '324234', 'Перец': '543345', 'Ноги': '545'}
        markup_position = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_position.add(types.KeyboardButton('\ud83d\udec2 Вернутся к выбору категории \ud83d\udec2'))
        markup_position.add(types.KeyboardButton('Посмотреть корзину'))
        for i in res.keys():
            markup_position.add(types.KeyboardButton(i))
        r = bot.send_message(message.chat.id, text="Выберети позицию которую хотите просмотреть", reply_markup=markup_position)
        bot.register_next_step_handler(r, position_chek, message, categories, res.keys())
    elif message.text == 'Посмотреть корзину':
        basket(message)
    else:
        start(message)


def position_chek(message, old_message, cat, position):
    print(message.text)
    if message.text == '🛂 Вернутся к выбору категории 🛂':
        start(message)
    elif message.text == 'Посмотреть корзину':
        basket(message)
    elif message.text in position:
        res = requests.get(f'https://serverfor10000.herokuapp.com/api/get_info/{old_message.text}/{message.text}').json()['info']
        # res = {'Банан': {"photo": dororroo, "description": '"description"', "cost": 200},
        #        'Кола': {"photo": dororroo, "description": '"description"', "cost": 23},
        #        'Яблоки': {"photo": dororroo, "description": '"description"', "cost": 674},
        #        'Чай': {"photo": dororroo, "description": "'description'", "cost": 22},
        #        'Жопаа': {"photo": dororroo, "description": '"description"', "cost": 111},
        #        'Кефир': {"photo": dororroo, "description": '"description"', "cost": 568},
        #        'Соль': {"photo": dororroo, "description": "'description'", "cost": 1000},
        #        'Перец': {"photo": dororroo, "description": "'description'", "cost": 2222},
        #        'Ноги': {"photo": dororroo, "description": '"description"', "cost": 15}}
        print(res)
        pos = res
        encoded = bytes(pos['photo'], encoding="raw_unicode_escape")
        encoded = encoded[2:-1]
        print(len(encoded))
        print(type(encoded))

        binary_data = a2b_base64(encoded)

        fd = open('img.jpg', 'wb')
        fd.write(binary_data)

        fd.close()

        pho = open("img.jpg", "rb")


        r = bot.send_photo(message.chat.id, pho, caption=pos['description'], reply_markup=markup_position)
        bot.register_next_step_handler(r, position_check, message.text, pos, old_message, cat)
    else:
        caregory_check(old_message, cat)



def position_check(message, name, info, old_message, cat):
    print(message.text)
    if message.text == '🛂 Вернутся к позициям 🛂':
        caregory_check(old_message, cat)
    elif message.text == '🛂 Вернутся к выбору категории 🛂':
        start(message)
    elif message.text == '🔹 🛒 Добавить в корзину 🛒 🔹':
        # with open('users.json') as le:
        #     data = dict(json.load(le))
        #
        # if name in data[f'{message.chat.id}']['all_positions']:
        #     data[f'{message.chat.id}']['all_positions'][name] = {'cost': info['cost'],
        #                                                      'count': data[f'{message.chat.id}']['all_positions'][name]['count'] + 1}
        # else:
        #     data[f'{message.chat.id}']['all_positions'][name] = {'cost': info['cost'],
        #                                                          'count': 1}
        # data[f'{message.chat.id}']['total_price'] += int(info['cost'])
        # with open('users.json', 'w') as lv:
        #     json.dump(data, lv)
        #     bot.send_message(message.chat.id, text='Товар успешно добавлен в корзину')
        #     caregory_check(old_message, cat)\
        markup_count = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_count.add(types.KeyboardButton('Ввести своё число'))
        for i in range(1, 16):
            markup_count.add(types.KeyboardButton(f'{i}'))

        r = bot.send_message(message.chat.id, 'Ввидите количество', reply_markup=markup_count)
        bot.register_next_step_handler(r, count_check, message, name, info, old_message, cat)
    elif message.text == 'Посмотреть корзину':
        basket(message)

def count_check(message, message_old, name, info, old_message, cat):
    if message.text == 'Ввести своё число':
        r = bot.send_message(message.chat.id, 'Введите число')
        bot.register_next_step_handler(r, count_check, message_old, name, info, old_message, cat)
    elif not message.text.isdigit():
        bot.send_message(message.chat.id, 'Неправельный формат ввода')
        position_check(message_old, name, info, old_message, cat)

    elif message.text[0] == '0':
        bot.send_message(message.chat.id, 'Неправельный формат ввода')
        position_check(message_old, name, info, old_message, cat)

    else:
        with open('users.json') as le:
            data = dict(json.load(le))

        if name in data[f'{message.chat.id}']['all_positions']:
            data[f'{message.chat.id}']['all_positions'][name] = {'cost': info['cost'],
                                                             'count': data[f'{message.chat.id}']['all_positions'][name]['count'] + int(message.text)}
        else:
            data[f'{message.chat.id}']['all_positions'][name] = {'cost': info['cost'],
                                                                 'count': int(message.text)}
        data[f'{message.chat.id}']['total_price'] += int(info['cost']) * int(message.text)
        with open('users.json', 'w') as lv:
            json.dump(data, lv)
            bot.send_message(message.chat.id, text='Товар успешно добавлен в корзину')
            caregory_check(old_message, cat)


markup_basket = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_basket.add(types.KeyboardButton('Редактировать корзину'))
markup_basket.add(types.KeyboardButton('Заказать'))

def basket(message):
    with open('users.json') as le:
        data = dict(json.load(le))
    pos = [x for x in data[str(message.chat.id)]["all_positions"].keys()]
    string = ''
    for i in pos:
        string += f'{i}: {data[str(message.chat.id)]["all_positions"][i]["cost"]} × {data[str(message.chat.id)]["all_positions"][i]["count"]}\n'
    string += f'Общая стоимость: {data[str(message.chat.id)]["total_price"]}'

    r = bot.send_message(message.chat.id, string, reply_markup=markup_basket)
    bot.register_next_step_handler(r, check_order)



markup_editor = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_editor.add(types.KeyboardButton('Изменить количество'))
markup_editor.add(types.KeyboardButton('Удалить позицию'))


def check_order(message):
    if message.text == 'Редактировать корзину':
        r = bot.send_message(message.chat.id, 'Выберити опцию', reply_markup=markup_editor)
        bot.register_next_step_handler(r, edit_order)
    else:
        buy(message.chat.id)



def edit_order(message):
    if message.text == 'Изменить количество':
        with open('users.json') as le:
            data = dict(json.load(le))
        pos = [x for x in data[str(message.chat.id)]["all_positions"].keys()]
        markup_pos = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in pos:
            markup_pos.add(i)
        r = bot.send_message(message.chat.id, 'Выбирите позицию у которой хотите изменить количество', reply_markup=markup_pos)
        bot.register_next_step_handler(r, change_count_1, pos)

    elif message.text == 'Удалить позицию':
        with open('users.json') as le:
            data = dict(json.load(le))
        pos = [x for x in data[str(message.chat.id)]["all_positions"].keys()]
        markup_pos = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in pos:
            markup_pos.add(i)
        r = bot.send_message(message.chat.id, 'Выберити позицию которую хотите удолить из корзины', reply_markup=markup_pos)
        bot.register_next_step_handler(r, delete_position, pos)


def delete_position(message, positions):
    if message.text in positions:
        with open('users.json') as le:
            data = dict(json.load(le))
        data[str(message.chat.id)]['total_price'] -= data[str(message.chat.id)]['all_positions'][message.text]['cost'] * data[str(message.chat.id)]['all_positions'][message.text]['count']
        del data[str(message.chat.id)]['all_positions'][message.text]
        with open('users.json', 'w') as lv:
            json.dump(data, lv)
        bot.send_message(message.chat.id, 'Изменения успешно внесены')
        basket(message)

def change_count_1(message, pos):
    if message.text in pos:
        r = bot.send_message(message.chat.id, 'Введите новое количество', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(r, change_count, message, pos)

def change_count(message, name, pos):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Неправельный формат ввода')
        change_count_1(name, pos)
    else:
        with open('users.json') as le:
            data = dict(json.load(le))
        data[str(message.chat.id)]['total_price'] -= data[str(message.chat.id)]['all_positions'][name.text]['cost'] * data[str(message.chat.id)]['all_positions'][name.text]['count']
        data[str(message.chat.id)]['all_positions'][name.text]['count'] = int(message.text)
        data[str(message.chat.id)]['total_price'] += data[str(message.chat.id)]['all_positions'][name.text]['cost'] * data[str(message.chat.id)]['all_positions'][name.text]['count']
        with open('users.json', 'w') as lv:
            json.dump(data, lv)
        bot.send_message(message.chat.id, 'Изменения успешно внесены')
        basket(message)


def buy(chat_id):  #TODO
    with open('users.json') as le:
        data = dict(json.load(le))
    am = data[str(chat_id)]['total_price']


    provider_token = '381764678:TEST:38070'  # @BotFather -> Bot Settings -> Payments


    # More about Payments: https://core.telegram.org/bots/payments

    prices = [LabeledPrice(label='Working Time Machine', amount=am)]





    bot.send_message(chat_id,
                         "Real cards won't work with me, no money will be debited from your account."
                         " Use this test card number to pay for your Time Machine: `1111 1111 1111 1026, 12/22, CVC 000.`"
                         "\n\nThis is your demo invoice:")
    bot.send_invoice(
            chat_id,  # chat_id
            'Working Time Machine',  # title
            ' Want to visit your great-great-great-grandparents? Make a fortune at the races? Shake hands with Hammurabi and take a stroll in the Hanging Gardens? Order our Working Time Machine today!',
            # description
            'HAPPY FRIDAYS COUPON',  # invoice_payload
            provider_token,  # provider_token
            'rub',  # currency
            prices,  # prices
            photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
            photo_height=512,  # !=0/None or picture won't be shown
            photo_width=512,
            photo_size=512,
            is_flexible=False,  # True If you need to set up Shipping Fee
            start_parameter='time-machine-example')

@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    shipping_options = [
        ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
        ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                                  error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                      error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                    " try to pay again in a few minutes, we need a small rest.")

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                         'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
                         'Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!'.format(
                             message.successful_payment.total_amount / 100, message.successful_payment.currency),
                         parse_mode='Markdown')



bot.polling(none_stop=True, interval=0)