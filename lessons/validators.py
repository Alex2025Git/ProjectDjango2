from rest_framework.exceptions import ValidationError


class YoutubeValidators:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link_video = value.get(self.field)
        if link_video and not link_video.startswith("https://www.youtube.com/"):
            raise ValidationError("Указана запрещенная ссылка")
