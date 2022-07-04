from rest_framework import serializers
from handbooks.models import Handbook, HandbookElement


class HandbookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Handbook
        fields = [
            'handbook_id', 'title', 'short_title',
            'description', 'version', 'start_at'
        ]


class HandbookElementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HandbookElement
        fields = ['element_code', 'value']
