
class Registration_I:

    def __init__(self, schoolId, 
                 schoolName, grade, parent, student, account):
        self.schoolId = schoolId
        self.schoolName = schoolName
        self.grade = grade
        self.parent = parent
        self.student = student
        self.account = account

class LoginHistory_I:
    """记录用户登录历史，在换设备的情况可以保证能正确收的消息推送"""
    def __init__(self, parentId, deviceId, notificationId) -> None:
        self.parentId = parentId
        self.deviceId = deviceId
        self.notificationId = notificationId