from rest_framework import serializers
from .models import TimeShift, BusinessLeave, Unpaid, Vacation, Illness, ooo_mapping


class OutOfOfficeSerializerMixin:
    person = serializers.SerializerMethodField()

    common_fields = ('start', 'end', 'comment', 'person', 'approver')


create_ooo_common_fields = ('start', 'end', 'comment', 'approver')


class TimeShiftListSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()

    class Meta:
        model = TimeShift
        fields = ('id', 'start', 'end', 'comment', 'person', 'approver', 'working_off_start', 'working_off_end')

    def get_person(self, obj):
        return obj.employee.get_full_name()


class TimeShiftCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeShift
        fields = create_ooo_common_fields + ('working_off_start',)


class BusinessLeaveListSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()

    class Meta:
        model = BusinessLeave
        fields = ('id', 'start', 'end', 'comment', 'person', 'approver')

    def get_person(self, obj):
        return obj.employee.get_full_name()


class BusinessLeaveCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessLeave
        fields = create_ooo_common_fields


class UnpaidListSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()

    class Meta:
        model = Unpaid
        fields = ('id', 'start', 'end', 'comment', 'person', 'approver')

    def get_person(self, obj):
        return obj.employee.get_full_name()


class UnpaidCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unpaid
        fields = create_ooo_common_fields


class VacationListSerializer(OutOfOfficeSerializerMixin, serializers.ModelSerializer):
    person = serializers.SerializerMethodField()

    class Meta:
        model = Vacation
        fields = ('id', 'start', 'end', 'comment', 'person', 'approver')

    def get_person(self, obj):
        return obj.employee.get_full_name()


class VacationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vacation
        fields = create_ooo_common_fields


class IllnessListSerializer(serializers.ModelSerializer):
    employee = serializers.ReadOnlyField(source='full_name')

    class Meta:
        model = Illness
        fields = ('start', 'end', 'comment', 'employee')


class IllnessCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Illness
        fields = ('start', 'end', 'comment')


class ApproveSerializer(serializers.Serializer):
    ooo_type = serializers.CharField(max_length=127)

    def validate(self, data):
        if data['ooo_type'] not in ooo_mapping:
            raise serializers.ValidationError({'ooo_type': ['Invalid ooo_type.']})
        data['model'] = ooo_mapping[data['ooo_type']]
        return data
