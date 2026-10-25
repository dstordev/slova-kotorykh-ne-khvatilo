from typing import Any

from aiogram import html
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format, Multi

from slova_kotorykh_ne_khvatilo.db.repositories import MessageRepository

from .states import PickUpMessageSG


async def get_random_message(
    dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    message_repository: MessageRepository = dialog_manager.middleware_data[
        "message_repository"
    ]
    random_message = await message_repository.get_random_message()
    random_message_text = random_message.text if random_message else "none"

    return {"random_message_text": html.quote(random_message_text)}


pick_up_message_dialog = Dialog(
    Window(
        Multi(
            Const("📬 <b>Послание</b>:"),
            Format("<blockquote>{random_message_text}</blockquote>"),
        ),
        Cancel(Const("◀️")),
        state=PickUpMessageSG.main,
        getter=get_random_message,
    )
)
