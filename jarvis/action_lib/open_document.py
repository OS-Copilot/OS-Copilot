from jarvis.action.base_action import BaseAction
from jarvis.atom_action.operations.media import view_office_document, play_video, play_audio, view_txt

class open_document(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = "open the target document in your offered file path."
        self.action_type = 'BASH'

    def __call__(self, path: str, type: str, *args, **kwargs):
        # 如果是offcie文件
        if type == 'doc' or type == 'docx' or type == 'ppt' or type == 'pptx' or type == 'xls' or type == 'xlsx' or type == 'pdf':
            view_office_document(path)
        # 如果是视频文件
        elif type == 'avi' or type == 'mp4' or type == 'mkv':
            play_video(path)
        # 如果是音频文件
        elif type == 'mp3' or type == 'wav':
            play_audio(path)
        # 如果是文本文件或者其它文件
        else:
            view_txt(path)

