from time import sleep
#from django.core.mail import send_mail
from celery import shared_task
import json

import logging
import sys
import requests
import json

import datetime
import pytz

from telegram import __version__ as TG_VER

PATH_API = 'http://45.84.224.163:5085/api/rest_bot/rest_bot/api_1_0/'

ORG_ID = -1

w_dict = {}
u_dict = {}


w_day1 = {1: 'Понедельник',
         2: 'Вторник',
         3: 'Среда',
         4: 'Четверг',
         5: 'Пятница',
         6: 'Суббота',
         7: 'Воскресенье'}

w_day = {1: 'пон.',
         2: 'вт.',
         3: 'ср.',
         4: 'чт.',
         5: 'пят.',
         6: 'суб.',
         7: 'воскр.'}         

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler, filters
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES, GET_NAME_ROUTES, GET_PHONE_ROUTES, GET_EMAIL_ROUTES = range(5)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, GET_NAME, GET_PHONE, GET_EMAIL = range(11)


def get_org_note(org_id) -> str:
    session = requests.Session()    
    r = session.get(PATH_API+"get_org_note/"+str(org_id)+"/")    
    data_json = json.loads(r.text)    
    return data_json['note_text']

def get_hello_phrases(org_id) -> str:
    session = requests.Session()    
    r = session.get(PATH_API+"get_hello_phrases/"+str(org_id)+"/")    
    data_json = json.loads(r.text)    
    return data_json['hello_phrases']
    
def get_token(org_id) -> str:
    session = requests.Session()    
    r = session.get(PATH_API+"get_token/"+str(org_id)+"/")    
    data_json = json.loads(r.text)    
    return data_json['token']
    
def get_w(org_id) -> str:
    session = requests.Session()    
    r = session.get(PATH_API+"get_w/"+str(org_id)+"/")    
    data_json = json.loads(r.text)        
    return data_json['w']

def get_s(org_id, w_id) -> str:
    session = requests.Session()    
    r = session.get(PATH_API+"get_s/"+str(org_id)+"/"+str(w_id)+"/")    
    data_json = json.loads(r.text)        
    return data_json['s']

def get_free_time(w_id, d_string) -> str:
    session = requests.Session()    
    r = session.get(PATH_API+"get_free_time/"+str(w_id)+"/"+str(d_string)+"/")    
    data_json = json.loads(r.text)        
    return data_json['array_h']

def get_params_its_name(org_id) -> str:
    session = requests.Session()    
    r = session.get(PATH_API+"get_params/"+str(org_id)+"/")    
    data_json = json.loads(r.text)        
    return data_json['its_name']

def get_params_its_phone(org_id) -> str:
    session = requests.Session()    
    r = session.get(PATH_API+"get_params/"+str(org_id)+"/")    
    data_json = json.loads(r.text)        
    return data_json['its_phone']

def get_params_its_email(org_id) -> str:
    session = requests.Session()    
    r = session.get(PATH_API+"get_params/"+str(org_id)+"/")    
    data_json = json.loads(r.text)        
    return data_json['its_email']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    global u_dict
    user_id = int(update.message['chat']['id'])
    u_dict.update({user_id: {'data':{}}})
       
    user = update.message.from_user
    
    logger.info("User %s started the conversation.", user.first_name)
    #если сессия новая:
    keyboard = [
        [
            InlineKeyboardButton("ЗАПИСАТЬСЯ", callback_data=str(GET_NAME)),
            InlineKeyboardButton("О КОМПАНИИ", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    #await update.message.reply_text("Привет!\n\nНа связи студия красоты \"Лакшми\"\nВ этом боте ты можешь записаться на стрижку 😎", reply_markup=reply_markup)
    await update.message.reply_text(get_hello_phrases(ORG_ID), reply_markup=reply_markup)
    
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("ЗАПИСАТЬСЯ", callback_data=str(GET_NAME)),
            InlineKeyboardButton("О КОМПАНИИ", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text=get_hello_phrases(ORG_ID), reply_markup=reply_markup)
    #return START_ROUTES
    return START_ROUTES

async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("ЗАПИСАТЬСЯ", callback_data=str(THREE)),
            InlineKeyboardButton("О КОМПАНИИ", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=get_hello_phrases(ORG_ID), reply_markup=reply_markup
    )
    return START_ROUTES


async def two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("↩️ ГЛАВНОЕ МЕНЮ", callback_data=str(ONE))
            #InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    s = get_org_note(ORG_ID)
    await query.edit_message_text(s, reply_markup=reply_markup)
    
    return START_ROUTES


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""
    #if новая сессиия и галочка стоит получать
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="Вы впервые воспользовались нашим сервисом. Введите пожалуйста Ваше имя:", reply_markup=None
    )    
    return GET_NAME_ROUTES

async def get_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global u_dict
    
    print('email->name',update.message.text)    
    user_id = int(update.message['chat']['id'])        
    u_dict[user_id]['data'].update({'username_input': update.message.text})  
    
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)    
      
    reply_markup = None
    await update.message.reply_text('Введите пожалуйста Ваш телефон:' , reply_markup=reply_markup)
    
    return GET_PHONE_ROUTES

async def get_phone_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global u_dict
    
    print('email->phone',update.message.text)
    user_id = int(update.message['chat']['id'])        
    u_dict[user_id]['data'].update({'phone_input': update.message.text})  
    
    user = update.message.from_user    
    #query = update.callback_query
    #await query.answer()
    #await query.edit_message_text(
    #    text="Введите пожалуйста Ваш email:\n\n ", reply_markup=None
    #)    
    reply_markup = None
    await update.message.reply_text('Введите пожалуйста Ваш email:' , reply_markup=reply_markup)
    return GET_EMAIL_ROUTES

async def get_email_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global u_dict
    
    print('email->',update.message.text)
    user_id = int(update.message['chat']['id'])    
    u_dict[user_id]['data'].update({'email_input': update.message.text})  
    
    #update.message.text сохранить
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)    
    keyboard = [
        [
            InlineKeyboardButton("ПРОДОЛЖИТЬ", callback_data=str(THREE)),
            InlineKeyboardButton("↩️ ГЛАВНОЕ МЕНЮ", callback_data=str(ONE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    print('---->>>',u_dict)
    await update.message.reply_text('Приятно познакомиться: '+u_dict[user_id]['data']['username_input'], reply_markup=reply_markup)
    #await update.message.reply_text('Приятно познакомиться:', reply_markup=reply_markup)
    
    return START_ROUTES
    
async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""
    global w_dict
    
    query = update.callback_query
    await query.answer()
    
    w_dict = {}    
    w_temp = get_w(ORG_ID)
    for w in w_temp:
        w_dict[w['id']] = w['name'] 
    
    a_inline = []    
    for k,v in w_dict.items():
        a_inline.append([InlineKeyboardButton(v, callback_data='w_'+str(k))])
    a_inline.append([InlineKeyboardButton("↩️ ГЛАВНОЕ МЕНЮ", callback_data=str(ONE))])
    
    keyboard = a_inline
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выбор Специалиста:\n\n ", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return START_ROUTES


async def four(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""
    global u_dict
    global w_dict
    
    query = update.callback_query
    w_data = query['data']
    user_id = query['from']['id']
    #u_dict.update({user_id:{'data':{'w_id': int(query['data'].replace('w_',''))}}})
    u_dict[user_id]['data'].update({'w_id': int(query['data'].replace('w_',''))})  
    
    print('u_dict_step4_2-->',u_dict)
    
    await query.answer()
    
    s_dict = {}
    s_temp = get_s(ORG_ID, int(u_dict[user_id]['data']['w_id']))
    for s in s_temp:
        s_dict[s['id']] = s['name']
        
    a_inline = []
    for k, v in s_dict.items():
        a_inline.append([InlineKeyboardButton(v, callback_data='s_'+str(k))])
    a_inline.append([InlineKeyboardButton("↩️ ГЛАВНОЕ МЕНЮ", callback_data=str(ONE))])
    keyboard = a_inline
    reply_markup = InlineKeyboardMarkup(keyboard)
    print('w_dict__step5',w_dict)
    await query.edit_message_text(        
        text="Специалист "+w_dict[u_dict[user_id]['data']['w_id']]+" \n На какую услугу:", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return START_ROUTES
    
async def five(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    global u_dict
    global w_dict
    
    query = update.callback_query
    #
    w_data = query['data']
    user_id = query['from']['id']
    
    #u_dict[user_id]['data'].update({'s_id': int(query['data'].replace('s_',''))})  
    u_dict[user_id]['data'].update({'s_id': int(query['data'].replace('s_',''))})  
    print('u_dict_step5-->',u_dict)
    s_dict = {}
    s_temp = get_s(ORG_ID, int(u_dict[user_id]['data']['w_id']))
    for s in s_temp:
        s_dict[s['id']] = s['name']
        
    #
    naiveDate = datetime.datetime.today()
    utc = pytz.UTC
    time_zone = pytz.timezone('Europe/Moscow')
    localizedDate = utc.localize(naiveDate)

    w_d = localizedDate.weekday()+1

    array_day=[]
    array_day.append(localizedDate)
    for i in range(1,7-w_d+1):
        array_day.append(localizedDate + datetime.timedelta(days=i))    
    #
    a_inline = []
    for a in array_day:        
        a_inline.append([InlineKeyboardButton(w_day[a.weekday()+1] +' '+ a.strftime('%d.%m.%y'), callback_data='d_'+a.strftime('%Y_%m_%d'))])
    a_inline.append([InlineKeyboardButton("↩️ ГЛАВНОЕ МЕНЮ", callback_data=str(ONE))])
    #a_inline.append([InlineKeyboardButton("СЛЕД.НЕДЕЛЯ ➡️", callback_data='next_week_'+'0')])
    keyboard = a_inline
    
    await query.answer()
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Специалист "+w_dict[u_dict[user_id]['data']['w_id']]+"\n Услуга "+s_dict[u_dict[user_id]['data']['s_id']]+". \n На какую дату:", reply_markup=reply_markup
    )
    return START_ROUTES
    
    
async def six(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    global u_dict
    global w_dict
    
    query = update.callback_query
    await query.answer()
    
    w_data = query['data']
    user_id = query['from']['id']
    
    u_dict[user_id]['data'].update({'d': query['data'].replace('d_','')})  
    print('u_dict_step6-->',u_dict)
    #
    s_dict = {}
    s_temp = get_s(ORG_ID, int(u_dict[user_id]['data']['w_id']))
    for s in s_temp:
        s_dict[s['id']] = s['name']
    #
    array_h=[]
    g_f_t = get_free_time(int(u_dict[user_id]['data']['w_id']), u_dict[user_id]['data']['d'])
    
    for i in g_f_t:
        #array_h.append(str(i)+':00')
        array_h.append(i)
    print('array_h-->',array_h)
    a_inline = []
    for a in array_h:        
        a_inline.append([InlineKeyboardButton(a, callback_data='h_'+a.replace(":","_"))])
    a_inline.append([InlineKeyboardButton("↩️ ГЛАВНОЕ МЕНЮ", callback_data=str(ONE))])
    keyboard = a_inline

    reply_markup = InlineKeyboardMarkup(keyboard)
    d = u_dict[user_id]['data']['d']
    await query.edit_message_text(
        text="Специалист "+w_dict[u_dict[user_id]['data']['w_id']]+" \n Услуга "+s_dict[u_dict[user_id]['data']['s_id']]+". \n на "+d[8:11]+'.'+d[5:7]+'.'+d[0:4]+" \n На какое время:", reply_markup=reply_markup
    )
    return START_ROUTES

async def seven(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    global u_dict
    global w_dict
    
    query = update.callback_query
    await query.answer()
    w_data = query['data']
    user_id = query['from']['id']
    
    s_dict = {}
    s_temp = get_s(ORG_ID, int(u_dict[user_id]['data']['w_id']))
    for s in s_temp:
        s_dict[s['id']] = s['name']
        
    u_dict[user_id]['data'].update({'h': query['data'].replace('h_','')})    
    print('u_dict_step7-->',u_dict)
    
    keyboard = [
        [            
            InlineKeyboardButton("ПОДТВЕРДИТЬ", callback_data=str(EIGHT)),
            InlineKeyboardButton("НАЗАД", callback_data=str(ONE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    d = u_dict[user_id]['data']['d']
    h = u_dict[user_id]['data']['h'].replace("_",":")
    await query.edit_message_text(
        text="Проверьте, все ли правильно записали?\n\nСпециалист "+w_dict[u_dict[user_id]['data']['w_id']]+" \n Услуга "+s_dict[u_dict[user_id]['data']['s_id']]+" \n "+d[8:11]+'.'+d[5:7]+'.'+d[0:4]+"  на "+h, reply_markup=reply_markup
    )
    return START_ROUTES

async def eight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    global u_dict
    global w_dict
    
    query = update.callback_query
    await query.answer()
    
    w_data = query['data']
    user_id = query['from']['id']
    
    s_dict = {}
    s_temp = get_s(ORG_ID, int(u_dict[user_id]['data']['w_id']))
    for s in s_temp:
        s_dict[s['id']] = s['name']
        
    #print('data-->',query['message']['chat']['id'])
    
    #u_dict[user_id]['data'].update({'t_chat_id': query['message']['chat']['id']})  
    u_dict[user_id]['data'].update({'t_user_id': user_id})  

    
    d = u_dict[user_id]['data']['d']
    h = u_dict[user_id]['data']['h'].replace("_",":")
    #    
    session = requests.Session()        

    headers = {'Content-type': 'application/json'}
    r = session.post(PATH_API+'set_sheduler/', data=json.dumps(u_dict), headers = headers)
    r1_summ = r.text
    print('u_dict_step8-->',json.dumps(u_dict))
    print(r.text)
    #
    await query.edit_message_text(
        text="Вы записаны: \n\n Специалист "+w_dict[u_dict[user_id]['data']['w_id']]+" \n Услуга "+s_dict[u_dict[user_id]['data']['s_id']]+". \n "+d[8:11]+'.'+d[5:7]+'.'+d[0:4]+" \n на "+h+"\n Ждем Вас!\n\nПовторная запись:\n/start", 
    )
    return END_ROUTES    


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


    
def main(org_id: int) -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    #application = Application.builder().token("5135375033:AAHUNNaVu41rQ5atwvtrsvQgfs_tm-0xTeY").build()
    application = Application.builder().token(get_token(org_id)).build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                
                CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(get_name, pattern="^" + str(GET_NAME) + "$"),
                
                CallbackQueryHandler(three, pattern="^" + str(THREE) + "$"),
                #CallbackQueryHandler(four, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(four, pattern="^w_\d+$"),                
                #CallbackQueryHandler(five, pattern="^" + str(FIVE) + "$"),
                CallbackQueryHandler(five, pattern="^s_\d+$"),
                #CallbackQueryHandler(six, pattern="^" + str(SIX) + "$"),
                CallbackQueryHandler(six, pattern="^d_\d+_\d+_\d+$"),#d_2022_09_01
                #CallbackQueryHandler(seven, pattern="^" + str(SEVEN) + "$"),
                CallbackQueryHandler(seven, pattern="^h_\d+_\d+$"),                
                CallbackQueryHandler(eight, pattern="^" + str(EIGHT) + "$"),
                
            ],
            GET_NAME_ROUTES:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_name_input),
            ],
            GET_PHONE_ROUTES:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_input),
            ],
            GET_EMAIL_ROUTES:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_email_input),
            ],
            END_ROUTES:[
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                #CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(EIGHT) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)
    #application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


@shared_task()
def send_feedback_bot_task(org_id):
    global ORG_ID
    global w_dict
    print('org_id-->',org_id)    
    ORG_ID = int(org_id)
    w_dict = {}    
    w_temp = get_w(ORG_ID)
    for w in w_temp:
        w_dict[w['id']] = w['name']    
    main(ORG_ID)
    with open('out_task.txt', 'w') as f:
            json.dump({'org_id':org_id}, f, ensure_ascii=False)
