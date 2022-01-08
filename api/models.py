from django.db import models
from django.db.models import Case, When, F, Value, ExpressionWrapper, FloatField


class StatisticQuerySet(models.QuerySet):
    def annotate_with_cost_per_clicks(self, *args, **kwargs):
        return self.annotate(cpc=Case(When(clicks=0, then=Value(0)),
                                      default=ExpressionWrapper(F("cost") * 1.0 / F("clicks"),
                                      output_field=FloatField())))

    def annotate_with_cost_per_mille(self, *args, **kwargs):
        return self.annotate(cpm=Case(When(views=0, then=Value(0)),
                                      default=ExpressionWrapper((F("cost") * 1.0 / F("views")) * 1000,
                                      output_field=FloatField())))


class Statistic(models.Model):
    objects = StatisticQuerySet.as_manager()

    date = models.DateField(blank=False, null=False)
    views = models.PositiveIntegerField(null=False, default=0)
    clicks = models.PositiveIntegerField(null=False, default=0)
    cost = models.DecimalField(null=False, decimal_places=2, max_digits=10, default=0)