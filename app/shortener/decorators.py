from loguru import logger

from django.views import View


class ExceptionHandlerMixin(View):
	"""Миксин для отлавливания всех необработанных эксепшенов
	в представлениях"""

	def dispatch(self, request, *args, **kwargs):
		try:
			return super().dispatch(request, *args, **kwargs)
		except Exception as e:
			logger.exception(e)
			return super().dispatch(request, *args, **kwargs)