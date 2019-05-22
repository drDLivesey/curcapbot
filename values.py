COINMARKETCAP_URL = "https://api.coinmarketcap.com/v1/ticker/"
TRAIDINGVIEW_CRYPTO_URL = "https://scanner.tradingview.com/crypto/scan"

TIME_VALUE = 1  # минуты до запуска проверки сигналов по базе
MAX_AMOUNT = 19  # допустимое количество сигналов на одного пользователя
MAX_BUTTONS = 16  # максимально возможное количество выводимых кнопок
MAX_USER_BUTTONS = 8  # максимально возможное количество выводимых кнопок


eng_text = {  # словарь ответов пользователю
    "? market": "Specify the market",
    "? cur": "Specify the currency",
    "? 2 cur": "Specify the second currency",
    "? tar_type": "Select target type:",
    "? %value": "\U0001F4CC   Set the percentage value",
    "? value": "\U0001F4CC   Set value",
    "? sure": "Are you sure?",

    "! target_limit": "\U00002757 <b>You've exceeded your targets limit.</b>\n\n Try removing unnecessary targets\n" +
                      " "*50 + "\U000025AB /show \U000025AB",

    "! button_limit": "\U00002757 <b>You've exceeded your buttons limit.</b>\n\n Try removing unnecessary buttons\n" +
                      " "*50 + "\U000025AB /my \U000025AB",

    "! no_targets": "\U00002757 <b>You haven't targets.</b> \n\n        You can set with\n          "
                  "        \U000025AB /t \U000025AB",

    "! no_buttons": "\U00002757 <b>You haven't buttons.</b> \n\n" + " "*8 + "You can create your button with\n"
                    + " "*40 + "\U000025AB \U0001F4CE \U000025AB",

    "! reached_1": "\n\n  \U000025ABThe target   <b>",
    "! reached_2": "</b>\n                                 has been reached\U000025AB\n\n",

    "! attention": "<b>\U0001F6A8    Attention!</b>   ",

    "! done": "\U00002705   <b>DONE</b>",
    "! tar_del": "\U0001F6AE   <b>Your target has been deleted:</b>\n         ",
    "! done_button": "\U00002705     <b>Done!</b> \nYou can now view your new button in \n"
                     + " "*44 + "\U000025AB/my\U000025AB",


    ". your_tar": "<b>Your targets:</b>",
    ". your_but": "<b>Your buttons:</b>",
    ". select_but_to_del": "<b>Select button to delete:</b>",
    ". del_but": "\U0000274C  delete button",
    ". show_cur_list": "show currency list",
    ". show_more": "\U0001F53B show more",
    ". create_target": "\U0001F4CC",
    ". create_button": "\U0001F4CE",
    ". show_all": "\U0001F4C4",
    ". comparison": "\U0001F19A",
    ". info": "info",
    ". ok": "OK",
    ". cancel": "Cancel",
    ". back": "\U0001F519",


    "... info": "\U0001F4CC  -  create a target\n              "
                "you will receive a message when you reach your target\n\n"
                "\U0001F4CE  -  create your button\n              "
                "you will be able to have quick access to this place\n\n"                
                "\U0001F19A  -  will compare this position with another\n\n"
                "\U0001F4C4  -  will show you all the information on this position\n",
    
    "1h": "% in 1 hour ",
    "24h": "% in 24 hours ",
    "7d": "% in 7 days ",
    "tar_line": "target line",
    "more": "\U0001F53B more",
    "choose": "CHOOSE",
    "now": "Now ",
    "recommend": "Recommendation : ",
    "strong_buy": "Strong buy \U0001F684",
    "buy": "Buy \U00002197",
    "strong_sell": "Strong sell \U0001F6AE",
    "sell": "Sell \U00002198",
    "delete": "Delete",

}

ru_text = {  # словарь ответов пользователю

}