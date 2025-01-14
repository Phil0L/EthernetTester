import json


class Data:

    def __init__(self):
        self.version = ""
        self.frame_count = 0
        self.frame_start = 0
        self.frames_per_second = 0
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
        out += f"\"frames_per_second\": {self.frames_per_second}, "
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

    def __hash__(self):
        return hash((self.version, self.update_count, self.touch_data, self.charge_data, self.cable_data, self.ip_data))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)


class _Touch:

    def __init__(self):
        self.touch_down_timestamp = 0
        self.touch_x_timestamp = 0
        self.touch_y_timestamp = 0
        self.touch_x_value = 0
        self.touch_y_value = 0

    def __hash__(self):
        return hash((self.touch_down_timestamp, self.touch_x_timestamp, self.touch_y_timestamp, self.touch_x_value, self.touch_y_value))


class _Cable(dict[int, list[int]]):

    def __init__(self):
        super(_Cable, self).__init__()
        self.pin = -1

    def __hash__(self):
        if self.is_empty():
            return 0
        return hash(self.pin)

    def is_empty(self):
        for key in self:
            if self[key]:
                return False
        return True


class _Charge:

    def __init__(self):
        self.charge = 0
        self.charging = False

    def __hash__(self):
        return hash((self.charge, self.charging))


class _Ip:

    def __init__(self):
        self.ipv4 = ""
        self.ipv6 = ""
        self.wlan = ""
        self.speed = ""

    def __hash__(self):
        return hash((self.ipv4, self.ipv6, self.wlan, self.speed))
