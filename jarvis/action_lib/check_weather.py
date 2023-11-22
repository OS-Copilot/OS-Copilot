from jarvis.action.base_action import BaseAction
from jarvis.atom_action.operations.system import terminal_show_file_content
import requests
import tempfile

class check_weather(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = "check the weather of the target place"
        self.action_type = 'BASH'

    def __call__(self, *places) -> None:
        # 例子curl wttr.in/anhui?m
        placeStr = ""
        if(len(places) > 1):
            placeStr = "+".join(places[::-1])
        elif(len(places) == 1):
            placeStr = places[0]
        weather_api = "http://wttr.in/{place}?m?".format(place=placeStr)
        response = requests.get(weather_api)
        res = "暂无天气数据"
        if(response != None):
            res = response.text
        terminal_show_file_content
        with tempfile.NamedTemporaryFile('w', delete=True) as temp:
            temp.write(res)
            temp.flush()
            terminal_show_file_content(temp.name)




