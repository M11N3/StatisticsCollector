from django.core.validators import MinValueValidator

from rest_framework import serializers

from .models import Statistic


class StatisticSerializer(serializers.ModelSerializer):
    clicks = serializers.IntegerField(required=False, default=0, min_value=0)
    cost = serializers.DecimalField(required=False, default=0, decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])
    views = serializers.IntegerField(required=False, default=0, min_value=0)
    cpc = serializers.ReadOnlyField()
    cpm = serializers.ReadOnlyField()

    class Meta:
        model = Statistic
        fields = ('date', 'cost', 'clicks', 'views', 'cpc', 'cpm')

    def update(self, instance, validated_data):
        instance.cost = instance.cost + validated_data.get('cost', 0)
        instance.clicks = instance.clicks + validated_data.get('clicks', 0)
        instance.views = instance.views + validated_data.get('views', 0)
        instance.save()
        return instance
