from rest_framework import serializers
from elevator_app.models import Elevator, ElevatorRequest
from rest_framework.validators import UniqueValidator

# Your Serializer
status_choices = (
    (1, "Working"),
    (0, "Not Working"),
)

door_status_choices = (
    (1, "Opened"),
    (0, "Closed"),
)

running_choices = (
    (1, "UP"),
    (0, "Down"),
)
running_status_choices = (
    (1, "Running"),
    (0, "Stopped"),
)


class ChoiceField(serializers.ChoiceField):
    """
    Edited the default representation accrding to Choices.
    """

    def to_representation(self, obj):
        if obj == "" and self.allow_blank:
            return obj
        return self._choices[obj]

    # def to_internal_value(self, data):
    #     # To support inserts with the value
    #     if data == '' and self.allow_blank:
    #         return ''

    #     for key, val in self._choices.items():
    #         if val == data:
    #             return key
    #     self.fail('invalid_choice', input=data)


class ElevatorSerializer(serializers.ModelSerializer):
    """
    This serializer is used to create Elevator Object, Create New Elevator , Update Existing Elevator and so on.
    """

    name = serializers.CharField(
        max_length=200, validators=[UniqueValidator(queryset=Elevator.objects.all())]
    )
    status = ChoiceField(choices=status_choices)
    door_status = ChoiceField(choices=door_status_choices)
    running_direction = ChoiceField(choices=running_choices)
    running_status = ChoiceField(choices=running_status_choices)

    class Meta:
        model = Elevator
        fields = [
            "name",
            "max_floor",
            "min_floor",
            "current_floor",
            "status",
            "door_status",
            "running_direction",
            "running_status",
            "add_time",
            "last_edited",
        ]


class ElevatorRequestSerializer(serializers.ModelSerializer):
    # define validator for requested_from_floor
    requested_from_floor = serializers.IntegerField()
    full_filled_by = serializers.CharField(source="full_filled_by.name", read_only=True)

    class Meta:
        model = ElevatorRequest
        fields = [
            "full_filled_by",
            "requested_from_floor",
            "requested_floor",
            "status",
            "is_fullfilled",
            "requested_date_time",
            "full_filled_date_time",
        ]

    def validate_requested_from_floor(self, data):
        if ElevatorRequest.objects.filter(
            requested_from_floor=data, status=False, is_fullfilled=False
        ).first():
            raise serializers.ValidationError(
                "A request is Already present from this floor."
            )
        return data


class ElevatorRequestDetailListSerializer(ElevatorSerializer):
    elevatorrequests = serializers.StringRelatedField(many=True)

    class Meta:
        model = Elevator
        fields = [
            "name",
            "max_floor",
            "min_floor",
            "current_floor",
            "status",
            "door_status",
            "running_direction",
            "running_status",
            "add_time",
            "last_edited",
            "elevatorrequests",
        ]
