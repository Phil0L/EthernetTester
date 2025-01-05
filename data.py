import copy
import json


class _Touch:
    touch_down_timestamp = 0
    touch_x_timestamp = 0
    touch_y_timestamp = 0
    touch_x_value = 0
    touch_y_value = 0


class _Cable(dict[int, list[int]]):
    pin = -1

    def __int__(self):
        super(_Cable, self).__init__()

    def is_empty(self):
        for key in self:
            if self[key]:
                return False
        return True


class _Charge:
    charge = 0
    charging = False


class _Ip:
    ipv4 = ""
    ipv6 = ""
    wlan = ""
    speed = ""


class Data:
    version = ""
    frame_count = 0
    update_count = 0
    touch_data = _Touch()
    cable_data = _Cable()
    charge_data = _Charge()
    ip_data = _Ip()

    def __str__(self):
        out = "{"
        if self.version != "":
            out += f"\"version\": {self.version}, "
        if self.update_count != 0:
            out += f"\"update_count\": {self.update_count}, "
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

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result
