from werkzeug.routing import BaseConverter


class ReConverter(BaseConverter):
    """自定义转换器; 正则转换器

    use:
        app.url_map.converters["re"] = ReConverter

        @bp.route("/re(r'.*'):name")
        def getname(name):
            return name

    """

    def __init__(self, mapper, regex):
        super(ReConverter, self).__init__(mapper)
        self.regex = regex

