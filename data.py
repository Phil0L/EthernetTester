import json


class Touch:
    touch_down_timestamp = 0
    touch_x_timestamp = 0
    touch_y_timestamp = 0
    touch_x_value = 0
    touch_y_value = 0


class Data:
    version = ""
    update_count = 0
    touch_data = Touch()
    frame_count = 0
    charge = 0
    charging = False
    ipv4 = ""
    ipv6 = ""

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=0)

