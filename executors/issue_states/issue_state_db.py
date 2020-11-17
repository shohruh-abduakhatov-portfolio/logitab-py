from executors.models.issue_state import IssueState
from modules.core.Connector import db


async def db_add(data: IssueState):
    terminal = (await db.query(
        'INSERT INTO issue_states (title, alias) '
        'VALUES ($1, $2) '
        'returning id, current_timestamp ;',
        (data.title, data.alias)))
    return terminal


async def db_modify(data):
    terminal = (
        await db.query(
            "UPDATE issue_states "
            "SET "
            "title = $2, alias = $3 "
            "WHERE id = $1 "
            "returning id, current_timestamp;",
            (data.id, data.title, data.alias, data.id)
        )
    )
    return terminal


async def db_remove(id):
    terminal = await db.query(
        'DELETE FROM issue_states where id={} returning id, current_timestamp'
            .format(id))
    return terminal


async def db_get_one(data):
    result = (await db.query('select *, current_timestamp from issue_states '
                             'where id=$1;', data.id))
    return result


async def get_all():
    result = await db.list("select * from issue_states;")
    return result