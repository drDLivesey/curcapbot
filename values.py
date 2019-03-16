currency_url = "https://api.coinmarketcap.com/v1/ticker/"

time_value = 10  # секунды до запуска проверки сигналов по базе
max_amount = 19  # допустимое количество сигналов на одного пользователя


t = {  # словарь ответов пользователю
    "? cur": "Specify the currency",
    "? tar_type": "Select target type:",
    "? %value": "\U0001F4CC   Set the percentage value",
    "? value": "\U0001F4CC   Set value",

    "! limit": "\U00002757 <b>You've exceeded your limit.</b>\n\n Try removing unnecessary entries\n                   "
               "                 \U000025AB /show \U000025AB",

    "! no targets": "\U00002757 <b>You haven't targets.</b> \n\n        You can set with\n          "
                  "        \U000025AB /t \U000025AB",

    "! reached_1": "\n\n  \U000025ABThe target   <b>",
    "! reached_2": "</b>\n                                 has been reached\U000025AB\n\n",

    "! attention": "<b>\U0001F6A8    Attention!</b>   ",

    "! done": "\U00002705   <b>DONE</b>",
    "! tar_del": "\U0001F6AE   <b>Your target has been deleted:</b>\n         ",
    "! your_tar": "<b>Your targets:</b>",


    ". show_cur_list": "show currency list",


    "1h": "% in 1 hour",
    "24h": "% in 24 hours",
    "7d": "% in 7 days",
    "tar_line": "target line",
    "choose": "CHOOSE"

}

