from django.conf import settings

from .utils import coerce_put_post, translate_mime, MimerDataException, UnsupportedMediaTypeException, rc


class DefaultSerializer(object):

    def __init__(self, handler):
        self.default_emitter = getattr(settings, 'PISTON_DEFAULT_EMITTER', 'json')
        self.stream = getattr(settings, 'PISTON_STREAM_OUTPUT', False)
        self.handler = handler

    def deserialize(self, request):
        rm = request.method.upper()

        # Django's internal mechanism doesn't pick up
        # PUT request, so we trick it a little here.
        if rm == "PUT":
            coerce_put_post(request)

        if rm in ('POST', 'PUT'):
            try:
                translate_mime(request)
            except MimerDataException:
                return rc.BAD_REQUEST
            except UnsupportedMediaTypeException:
                return rc.UNSUPPORTED_MEDIA_TYPE
        return request

    def serialize(self, request, result, fields):
        from .emitters import Emitter
        from .resource import typemapper

        em_format = self.determine_emitter(request)
        if not em_format:
            em_format = self.default_emitter
        emitter, ct = Emitter.get(em_format)
        srl = emitter(result, typemapper, self.handler, request, self.get_serialization_format(request), fields,
                      fun_kwargs={'request': request})
        if self.stream: stream = srl.stream_render(request)
        else: stream = srl.render(request)
        return stream, ct

    def determine_emitter(self, request):
        """
        Function for determening which emitter to use
        for output. It lives here so you can easily subclass
        `Resource` in order to change how emission is detected.
        """
        from .emitters import Emitter
        try:
            import mimeparse
        except ImportError:
            mimeparse = None

        if mimeparse and 'HTTP_ACCEPT' in request.META:
            supported_mime_types = set()
            emitter_map = {}
            for name, (_, content_type) in Emitter.EMITTERS.items():
                content_type_without_encoding = content_type.split(';')[0]
                print content_type_without_encoding
                supported_mime_types.add(content_type_without_encoding)
                emitter_map[content_type_without_encoding] = name
            supported_mime_types = list(supported_mime_types)
            preferred_content_type = mimeparse.best_match(
                supported_mime_types,
                request.META['HTTP_ACCEPT'])
            return emitter_map.get(preferred_content_type, None)

    def get_serialization_format(self, request):
        from .emitters import Emitter

        serialization_format = request.META.get('HTTP_X_SERIALIZATION_FORMAT', Emitter.SerializationTypes.RAW)
        if serialization_format not in Emitter.SerializationTypes:
            return Emitter.SerializationTypes.RAW
        return serialization_format
