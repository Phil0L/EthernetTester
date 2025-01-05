import json


class Data:

    def __init__(self):
        self.version = ""
        self.frame_count = 0
        self.update_count = 0
        self.touch_data = _Touch()
        self.cable_data = _Cable()
        self.charge_data = _Charge()
        self.ip_data = _Ip()

    def __str__(self):
        out = "{"
        if self.version != "":
            out += f"\"version\": {self.version}, "
        if self.update_count != 0:
            out += f"\"update_count\": {self.update_count}, "
        out += f"\"frame_count\": {self.frame_count}, "
        # To add: touch
        # To add: charge
        if self.ip_data.ipv4 != "":
            out += f"\"ipv4\": {self.ip_data.ipv4}, "
        if self.ip_data.ipv6 != "":
            out += f"\"ipv6\": {self.ip_data.ipv6}, "
        if self.ip_data.wlan != "":
            out += f"\"wlan\": {self.ip_data.wlan}, "
        if self.ip_data.speed != "":
            out += f"\"speed\": {self.ip_data.speed}, "
        if not self.cable_data.is_empty():
            out += f"\"pin\": {self.cable_data.pin}, \"cable\": {json.dumps(self.cable_data, indent=0)}"
        return out.replace("\n", "") + "}"

    def __eq__(self, other):
        return str(self) == str(other)

    # def __copy__(self):
    #     cls = self.__class__
    #     result = cls.__new__(cls)
    #     result.__dict__.update(self.__dict__)
    #     return result
    #
    # def __deepcopy__(self, memo):
    #     cls = self.__class__
    #     result = cls.__new__(cls)
    #     result.__dict__.update(self.__dict__)
    #     result.ip_data.__dict__.update(self.ip_data.__dict__)
    #     result.touch_data.__dict__.update(self.touch_data.__dict__)
    #     result.charge_data.__dict__.update(self.charge_data.__dict__)
    #     result.cable_data.__dict__.update(self.cable_data.__dict__)
    #     return result


class _Touch:

    def __init__(self):
        self.touch_down_timestamp = 0
        self.touch_x_timestamp = 0
        self.touch_y_timestamp = 0
        self.touch_x_value = 0
        self.touch_y_value = 0


class _Cable(dict[int, list[int]]):

    def __init__(self):
        super(_Cable, self).__init__()
        self.pin = -1

    def is_empty(self):
        for key in self:
            if self[key]:
                return False
        return True


class _Charge:

    def __init__(self):
        self.charge = 0
        self.charging = False


class _Ip:

    def __init__(self):
        self.ipv4 = ""
        self.ipv6 = ""
        self.wlan = ""
        self.speed = ""


