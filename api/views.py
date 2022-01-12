from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.filters import OrderingFilter
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from .models import Statistic
from .filters import DateFilter
from .serializers import StatisticSerializer


class StatisticAPIView(CreateModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DateFilter
    ordering_fields = ['date', 'cost', 'clicks', 'views', 'cpc', 'cpm']

    def get(self, request):
        """
        GET method
        Return statistic for all the time WHEN ?from and ?to  were not specified
        Return statistic for the time interval with &from (start date) AND ?to (end date)

        query_params:
            from     (Optional[Date]) - "YYYY-MM-DD"
            to       (Optional[Date]) - "YYYY-MM-DD"
            ordering (Optional[name ordering field])

        response:
            [{
                "date": ...,
                "cost": ...,
                "clicks": ...,
                "views": ...,
                "cpc": ...,
                "cpm": ...
            },]

        """

        queryset = self.filter_queryset(self.get_queryset())
        # Add cost per clicks in QuerySet AS "cpc"
        queryset = queryset.annotate_with_cost_per_clicks()
        # Add cost per mille in QuerySet AS "cpm"
        queryset = queryset.annotate_with_cost_per_mille()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        """
        POST method create or update Statistic on date

        request.data:
            -date   (Required)
            -cost   (Optional) default=0
            -clicks (Optional) default=0
            -views  (Optional) default=0

        response
            Success:
                data: return statistic for the date
                status: 201
            ValidationError:
                error: {'field' : 'message'}
        """

        serializer = self.get_serializer(data=request.POST)
        if serializer.is_valid():
            instance = self.queryset.filter(date=serializer.validated_data["date"]).first()
            if instance:
                instance = serializer.update(instance, serializer.validated_data)
                serializer = self.get_serializer(instance)
            else:
                serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """ DELETE method reset all statistic """
        self.queryset.delete()
        return Response(status=HTTP_204_NO_CONTENT)

