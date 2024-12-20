import json


class _Touch:
    touch_down_timestamp = 0
    touch_x_timestamp = 0
    touch_y_timestamp = 0
    touch_x_value = 0
    touch_y_value = 0


class Data:
    version = ""
    update_count = 0
    touch_data = _Touch()
    frame_count = 0
    charge = 0
    charging = False
    ipv4 = ""
    ipv6 = ""
    cable: dict[int, list[int]] = {}

    def toJSON(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          indent=0)[:-1] + ", \"cable\": " + \
               json.dumps(self.cable,
                          indent=0) + "}"
