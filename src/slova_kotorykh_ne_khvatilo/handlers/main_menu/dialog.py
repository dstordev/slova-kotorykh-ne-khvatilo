from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from .states import MainMenuSG

main_menu_dialog = Dialog(
    Window(
        Const(
            "😺 Привет!\n"
            "Тут ты можешь получить теплые слова оставленные людьми, а также оставить свои для других"
        ),
        Row(
            Button(Const("📬 Получить"), id="pick_up_message"),
            Button(Const("📥 Оставить"), id="send_message"),
        ),
        state=MainMenuSG.main,
    ),
)
