from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start
from aiogram_dialog.widgets.text import Const

from slova_kotorykh_ne_khvatilo.handlers.pick_up_message import PickUpMessageSG

from .states import MainMenuSG

main_menu_dialog = Dialog(
    Window(
        Const(
            "😺 Привет!\n"
            "Тут ты можешь получить теплые слова оставленные людьми, а также оставить свои для других"
        ),
        Row(
            Start(
                Const("📬 Получить"),
                id="pick_up_message",
                state=PickUpMessageSG.main,
            ),
            Button(Const("📥 Оставить"), id="send_message"),
        ),
        state=MainMenuSG.main,
    ),
)
