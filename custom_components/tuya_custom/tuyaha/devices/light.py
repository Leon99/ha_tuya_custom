from .base import TuyaDevice


class TuyaLight(TuyaDevice):

    def brightness(self):
        work_mode = self.data.get("color_mode")
        if work_mode == "colour" and "color" in self.data:
            brightness = int(self.data.get("color").get("brightness") * 255 / 100)
        else:
            brightness = self.data.get("brightness")
        return brightness

    def _set_brightness(self, brightness):
        work_mode = self.data.get("color_mode")
        if work_mode == "colour":
            self.data["color"]["brightness"] = brightness
        else:
            self.data["brightness"] = brightness

    def support_color(self):
        if self.data.get("color") is None:
            return False
        else:
            return True

    def support_color_temp(self):
        if self.data.get("color_temp") is None:
            return False
        else:
            return True

    def hs_color(self):
        if self.data.get("color") is None:
            return None
        else:
            work_mode = self.data.get("color_mode")
            if work_mode == "colour":
                color = self.data.get("color")
                return color.get("hue"), color.get("saturation")
            else:
                return 0.0, 0.0

    def color_temp(self):
        if self.data.get("color_temp") is None:
            return None
        else:
            return self.data.get("color_temp")

    def min_color_temp(self):
        return 10000

    def max_color_temp(self):
        return 1000

    def turn_on(self):
        if self._control_device("turnOnOff", {"value": "1"}):
            self._update_data("state", "true")

    def turn_off(self):
        if self._control_device("turnOnOff", {"value": "0"}):
            self._update_data("state", "false")

    def set_brightness(self, brightness):
        """Set the brightness(0-255) of light."""
        value = int(brightness * 100 / 255)
        if self._control_device("brightnessSet", {"value": value}):
            self._update_data("brightness", brightness)

    def set_color(self, color):
        """Set the color of light."""
        hsv_color = {}
        hsv_color["hue"] = color[0]
        hsv_color["saturation"] = color[1] / 100
        if len(color) < 3:
            hsv_color["brightness"] = int(self.brightness()) / 255.0
        else:
            hsv_color["brightness"] = color[2]
        # color white
        if hsv_color["saturation"] == 0:
            hsv_color["hue"] = 0
        if self._control_device("colorSet", {"color": hsv_color}):
            self._update_data("color", hsv_color)
            self._update_data("color_mode", "white" if hsv_color["saturation"] == 0 else "colour")

    def set_color_temp(self, color_temp):
        if self._control_device("colorTemperatureSet", {"value": color_temp}):
            self._update_data("color_temp", color_temp)

    def update(self):
        return self._update(use_discovery=True)
