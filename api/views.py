from django.utils.timezone import localdate
from django.db.models import Count
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .models import TinyURLStats, TinyURL
from api import serializers


class TherapieLandViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    """
    A viewset that provides default `create()` and `retrieve()` actions.
    """
    pass


class TinyURLViewSet(TherapieLandViewSet):
    """
    URLs Endpoint

    Allowed methods are: POST, GET (Retrieve single url)

    Statistics can be found in /actions for each url detail endpoint.

    """
    lookup_field = "shortcode"
    serializer_class = serializers.TinyURLSerializer
    queryset = TinyURL.objects.all()

    def update_stats(self, shortcode):
        year, week, _ = localdate().isocalendar()
        ts = TinyURLStats(shortcode=shortcode, week=week, year=year)
        ts.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.update_stats(instance)
        headers = {"Location": instance.url}
        return Response(status=status.HTTP_302_FOUND, headers=headers)

    def create(self, request, *args, **kwargs):
        shortcode = request.data.get("shortcode")
        # check 409 errors -
        # That could be also a validation error. error inherit from Model validator
        # we could save all this method
        if shortcode and TinyURL.objects.filter(shortcode=shortcode).count():
            return Response(
                "Shortcode already in use", status=status.HTTP_409_CONFLICT
            )
        return super().create(request, *args, **kwargs)

    @action(detail=True)
    def stats(self, request, shortcode):
        """Retrieve statistics for a url usage."""
        queryset = TinyURLStats.objects.filter(
            shortcode=shortcode
        ).values('week', 'year').annotate(
            redirects_count=Count('shortcode')
        ).order_by('redirects_count')

        serializer = serializers.URLStatsSerializer(queryset, many=True)
        return Response(serializer.data)
