from rest_framework.serializers import ModelSerializer, SerializerMethodField

from shortener.models import URL
from shortener.services import build_shortened_url


class URLSerializer(ModelSerializer):
	shortened_url = SerializerMethodField()

	class Meta:
		model = URL
		fields = ('original_url', 'code', 'shortened_url', 'created_at')
	
	def get_shortened_url(self, obj: URL) -> str:
		request = self.context.get('request')
		return build_shortened_url(request, obj.code)



	
