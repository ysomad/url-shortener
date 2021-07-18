from loguru import logger

from .serializers import URLSerializer


def save_url_serializer(
		session_key: str, serializer: URLSerializer) -> URLSerializer:
	"""Сохраняет URL инстанс в БД из сериалайзера URLSerializer"""
	url_serializer = serializer
	url_serializer.is_valid(raise_exception=True)
	url_serializer.save(session=session_key)

	original_url = url_serializer.data['original_url']
	url_code = url_serializer.data['code']

	logger.info((
		f'Original URL "{original_url}" with code "{url_code}" saved in db '
		f'for session "{session_key}" from serializer {url_serializer}'
	))

	return url_serializer