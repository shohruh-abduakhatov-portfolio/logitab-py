from .views.drivers import driver
from .views.driving_event import driving_event
from .views.eld import eld
from .views.fuel_type import fuel_type
from .views.groups import groups
from .views.issue_state import issue_state
from .views.ping import test2
from .views.terminal import terminal
from .views.unit import unit
from .views.user import user_view
from .views.vehicle import vehicle
from .views_mobile.auth import auth
from .views_mobile.event import event_mobile
from .views_mobile.file_upload import file_upload_mobile
from .views_mobile.inspection import inspection_mobile
from .views_mobile.log import log_mobile
from .views_mobile.log_edit_request import log_edit_request
from .views_mobile.vehicle import vehicle as m_vehicle


url_prefix = '/api/v1'
url_mob = '/api/v1/mob'


def setup_routes(app):
    # token
    app.router.add_route("POST", url_prefix + '/user/token', user_view.login)  # get token
    app.router.add_route("POST", url_prefix + '/user/is_authorized', user_view.is_authorized)
    app.router.add_route("POST", url_prefix + '/user/{user_id}/activate', user_view.activate)
    app.router.add_route("POST", url_prefix + '/user/{user_id}/deactivate', user_view.deactivate)
    # drivers
    app.router.add_route("GET", url_prefix + '/drivers', driver.get_driver_list)
    app.router.add_route("POST", url_prefix + '/drivers', driver.create_driver)
    app.router.add_route("GET", url_prefix + '/drivers/search', driver.search)
    app.router.add_route("GET", url_prefix + '/drivers/{driver_id}', driver.get_driver_info)
    # app.router.add_route("DELETE", url_prefix + '/drivers/{driver_id}', driver.delete_driver)
    app.router.add_route("PUT", url_prefix + '/drivers/{driver_id}', driver.update_driver)
    app.router.add_route("PUT", url_prefix + '/drivers/{driver_id}/status', driver.change_status)
    # terminals
    app.router.add_route("GET", url_prefix + '/terminals', terminal.get_list)
    app.router.add_route("POST", url_prefix + '/terminals', terminal.create)
    app.router.add_route("GET", url_prefix + '/terminals/{terminal_id}', terminal.get_info)
    app.router.add_route("DELETE", url_prefix + '/terminals/{terminal_id}', terminal.delete)
    app.router.add_route("PUT", url_prefix + '/terminals/{terminal_id}', terminal.update)
    # vehicles
    app.router.add_route("GET", url_prefix + '/vehicles', vehicle.get_vehicle_list)
    app.router.add_route("POST", url_prefix + '/vehicles', vehicle.create_vehicle)
    app.router.add_route("GET", url_prefix + '/vehicles/search', vehicle.search)
    app.router.add_route("GET", url_prefix + '/vehicles/{vehicle_id}', vehicle.get_vehicle_info)
    app.router.add_route("DELETE", url_prefix + '/vehicles/{vehicle_id}', vehicle.delete_vehicle)
    app.router.add_route("PUT", url_prefix + '/vehicles/{vehicle_id}', vehicle.update_vehicle)
    app.router.add_route("PUT", url_prefix + '/vehicles/{vehicle_id}/status', vehicle.change_status)
    # eld
    app.router.add_route("GET", url_prefix + '/eld', eld.get_eld_list)
    app.router.add_route("POST", url_prefix + '/eld', eld.create_eld)
    app.router.add_route("GET", url_prefix + '/eld/search', eld.search)
    app.router.add_route("GET", url_prefix + '/eld/{eld_id}', eld.get_eld_info)
    app.router.add_route("DELETE", url_prefix + '/eld/{eld_id}', eld.delete_eld)
    app.router.add_route("PUT", url_prefix + '/eld/{eld_id}', eld.update_eld)
    # groups
    app.router.add_route("GET", url_prefix + '/groups', groups.get_list)
    app.router.add_route("POST", url_prefix + '/groups', groups.create)
    app.router.add_route("GET", url_prefix + '/groups/search', groups.search)
    app.router.add_route("GET", url_prefix + '/groups/{group_id}', groups.get_info)
    app.router.add_route("DELETE", url_prefix + '/groups/{group_id}', groups.delete)
    app.router.add_route("PUT", url_prefix + '/groups/{group_id}', groups.update)
    # units
    app.router.add_route("GET", url_prefix + '/units', unit.get_list)
    app.router.add_route("POST", url_prefix + '/units', unit.create)
    app.router.add_route("GET", url_prefix + '/units/search', unit.search)
    app.router.add_route("GET", url_prefix + '/units/{unit_id}', unit.get_info)
    app.router.add_route("DELETE", url_prefix + '/units/{unit_id}', unit.delete)
    app.router.add_route("PUT", url_prefix + '/units/{unit_id}', unit.update)
    # driving_event
    app.router.add_route("GET", url_prefix + '/driving_events', driving_event.get_list)
    app.router.add_route("POST", url_prefix + '/driving_events', driving_event.create)
    app.router.add_route("GET", url_prefix + '/driving_events/{driving_event_id}', driving_event.get_info)
    app.router.add_route("DELETE", url_prefix + '/driving_events/{driving_event_id}', driving_event.delete)
    app.router.add_route("PUT", url_prefix + '/driving_events/{driving_event_id}', driving_event.update)
    # issue_state
    app.router.add_route("GET", url_prefix + '/issue_state', issue_state.get_list)
    # fuel_type
    app.router.add_route("GET", url_prefix + '/fuel_type', fuel_type.get_list)
    # ping
    app.router.add_route("GET", url_prefix + '/ping', test2)
    # app.router.add_route("POST", url_prefix + '/update_app', update_app)


def setup_routes_mobile(app):
    app.router.add_route("GET", url_mob + '/ping-mobile', test2)
    # Auth
    app.router.add_route("POST", url_mob + '/user/login', auth.login_driver)
    app.router.add_route("PUT", url_mob + '/user/password', auth.change_password)
    app.router.add_route("POST", url_mob + '/user/send_password', auth.send_password)
    app.router.add_route("GET", url_mob + '/user/is_authorized', auth.is_valid_token)
    # Vehicle
    app.router.add_route("POST", url_mob + '/vehicle', m_vehicle.get_vehicle_list)
    app.router.add_route("PUT", url_mob + '/vehicle/{vehicle_id}/driver/{driver_id}', m_vehicle.set_vehicle_to_driver)
    # Log Edit Request
    app.router.add_route("POST", url_mob + '/log_edit_request', log_edit_request.get_list)
    app.router.add_route("POST", url_mob + '/log_edit_request/{log_id}/accept', log_edit_request.accept)
    app.router.add_route("POST", url_mob + '/log_edit_request/{log_id}/reject', log_edit_request.reject)
    # Log
    app.router.add_route("POST", url_mob + '/log', log_mobile.get_by_date)
    app.router.add_route("GET", url_mob + '/log/{log_id}', log_mobile.get_info)
    # Event
    app.router.add_route("POST", url_mob + '/update/{event_id}', event_mobile.update)
    app.router.add_route("POST", url_mob + '/insert/{event_id}', event_mobile.insert)
    # Inspection
    # app.router.add_route("POST", url_mob + '/inspection', inspection_mobile.hand_review)
    # File Upload/Multipart
    app.router.add_route("POST", url_mob + '/file_upload_test', file_upload_mobile.file_upload_test)
