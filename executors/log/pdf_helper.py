from executors.models.edited_event import EditedEvent
from executors.models.event import Event
from executors.utils.stepline import generate_stepline_chart


async def generate_edit_request_report(current_event_list: [Event], edited_event_list: [EditedEvent]):
    current_signature = await generate_stepline_chart(current_event_list)
    edited_signature = await generate_stepline_chart(edited_event_list)

