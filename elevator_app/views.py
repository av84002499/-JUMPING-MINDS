from django.http import Http404
from django.db.models import Func, F, ExpressionWrapper, IntegerField

from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from elevator_app.models import Elevator, ElevatorRequest
from elevator_app.serializers import (
    ElevatorSerializer,
    ElevatorRequestSerializer,
    ElevatorRequestDetailListSerializer,
)

# Create your views here.


class ListCreateGetElevator(generics.ListCreateAPIView):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer


class GetUpdateElevator(generics.RetrieveUpdateAPIView):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer


# Added a view to save the elevetor request and before saving also get the most optimal or nearest lift and assigned it to the request.
class GetDetailElevetorRequest(generics.RetrieveAPIView):
    """
    First this class have a opnly put method to update the existing request for further processing. This class can upate only whoose , where object has empty requested_floor and
    The same class is also use for Opening Gate.
    """

    queryset = ElevatorRequest.objects.all()
    serializer_class = ElevatorRequestSerializer


class GetCreateElevatorDoor(generics.ListCreateAPIView):
    queryset = ElevatorRequest.objects.all()
    serializer_class = ElevatorRequestSerializer

    def get_optimal_elevator(self, requested_from_floor):
        """
        This method return the optimal Elevator according to the request's floor.
        """
        try:
            # return Elevator.objects.all().order_by("current_floor").first()
            nearest_elevator = (
                Elevator.objects.annotate(
                    abs_diff=Func(
                        F(
                            "current_floor",
                        )
                        - requested_from_floor,
                        function="ABS",
                        # output_field=IntegerField(),
                    )
                )
                .order_by("abs_diff")
                .first()
            )
            return nearest_elevator

        except Elevator.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        request_floor = serializer.validated_data.get("requested_from_floor")
        nearest_elevator = self.get_optimal_elevator(requested_from_floor=request_floor)
        serializer.save(full_filled_by=nearest_elevator)


# TODO Get all request for a given Elevator


class GetAllElevatorRequest(generics.RetrieveAPIView):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorRequestDetailListSerializer
