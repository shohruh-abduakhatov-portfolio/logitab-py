from executors.models.user import User
from modules.core.Connector import db


async def db_add(data: User):
    params = data
    driver = (await db.query("INSERT INTO users (username, password, role, organization_id, "
                             "first_name, last_name, status, phone, email) "
                             "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) returning id, current_timestamp;",
                             (data.username, data.password, data.role,
                              data.organization_id, data.first_name, data.last_name, data.status,
                              data.phone, data.email)))

    return driver


async def db_modify(data):
    driver = (
        await db.query("UPDATE users "
                       "SET username =$1, password =$2, role =$3, organization_id =$4, "
                       "first_name =$5, last_name =$6, status=$7, phone=$8, email=$9 "
                       "WHERE id = $10 returning id, current_timestamp;",
                       (data.username, data.password, data.role, data.organization_id,
                        data.first_name, data.last_name, data.status, data.phone,
                        data.email, data.id))
    )
    return driver


async def db_remove(data):
    driver = await db.query('DELETE FROM users where id={} returning current_timestamp'.format(data['id']))
    return driver


async def db_get_by_id(data):
    result = (await db.query('select *, current_timestamp from users '
                             'where id=$1;', data["id"]))
    return result


async def db_set_status(data):
    driver = (
        await db.query("UPDATE users "
                       "SET status =$1 "
                       "WHERE id = $2 returning id, current_timestamp;",
                       (data['status'], data['id']))
    )
    return driver


async def get_all():
    result = await db.list("select * from users;")
    return result
