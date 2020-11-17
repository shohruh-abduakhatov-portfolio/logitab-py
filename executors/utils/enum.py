from enum import Enum


class MyEnum(Enum):
    def __str__(self):
        return str(self.value)


    def __int__(self):
        return int(self.value)


    def __float__(self):
        return float(self.value)


    def __get__(self, instance, owner):
        return self.value


class EditRequestHistoryDescEnum(MyEnum):
    ADMIN_CANCELED = "Cancelled by Admin"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    WAITING = "Waiting"


class EditRequestHistoryCodeEnum(MyEnum):
    ADMIN_CANCELED = 0
    APPROVED = 1
    REJECTED = 2
    WAITING = 3


class EventEditedDescEnum(MyEnum):
    WAITING = 'Waiting'


class EventEditedCodeEnum(MyEnum):
    WAITING = 0


class DvirStatusCodeEnum(MyEnum):
    ISSUE = 0
    FIXED = 1


class DvirStatusDescEnum(MyEnum):
    ISSUE = "Issue found"
    FIXED = "Fixed"


class ViolationLevelCodeEnum(MyEnum):
    COMPILIANT_LOGS = 1
    NON_COMPLIANT_LOGS = 2
    HOS_VIOLATIONS = 3
    FORM_MANAGER_ERRORS = 4
    SPLIT_BREAK = 5
    APPROACHING_VIOLATIONS = 6
    NO_PTI = 7
    DEVICE_SHUTDOWN = 8


class ViolationLevelCodeClass(MyEnum):
    COMPILIANT_LOGS = "Compliant Logs"  # no errors (completed)
    NON_COMPLIANT_LOGS = "Non-compliant logs"  # logs with
    HOS_VIOLATIONS = "HOS Violations"
    FORM_MANAGER_ERRORS = "Form & Manager Errors"
    SPLIT_BREAK = "Split Break"
    APPROACHING_VIOLATIONS = "Approeaching Violations"
    NO_PTI = "No PTI"
    DEVICE_SHUTDOWN = "Device Shut Down"


class ViolationName(MyEnum):
    MISSING_SIGNATURE = "missing_signature"


class ViolationDesc(MyEnum):
    MISSING_SIGNATURE = "Missing signature"


class EventStatus(MyEnum):
    OFF = 'off'
    D = "d"
    SB = 'sb'
    ON = 'on'
