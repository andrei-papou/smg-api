from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    TimeShiftListSerializer, TimeShiftCreateSerializer, BusinessLeaveListSerializer, BusinessLeaveCreateSerializer,
    UnpaidListSerializer, UnpaidCreateSerializer, VacationListSerializer, VacationCreateSerializer,
    IllnessCreateSerializer, IllnessListSerializer, ApproveSerializer
)
from .models import TimeShift, BusinessLeave, Unpaid, Vacation, Illness


class OOOViewMixin:
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        user = self.request.user
        if not user.is_manager:
            return queryset.filter(employee__department=user.department)
        return queryset

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)


class TimeShiftView(OOOViewMixin, ListCreateAPIView):
    queryset = TimeShift.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TimeShiftListSerializer
        return TimeShiftCreateSerializer


class BusinessLeaveView(OOOViewMixin, ListCreateAPIView):
    queryset = BusinessLeave.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BusinessLeaveListSerializer
        return BusinessLeaveCreateSerializer


class UnpaidView(OOOViewMixin, ListCreateAPIView):
    queryset = Unpaid.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UnpaidListSerializer
        return UnpaidCreateSerializer


class VacationView(OOOViewMixin, ListCreateAPIView):
    queryset = Vacation.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return VacationListSerializer
        return VacationCreateSerializer


class IllnessView(OOOViewMixin, ListCreateAPIView):
    queryset = Illness.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IllnessListSerializer
        return IllnessCreateSerializer


class ApproveView(APIView):

    def patch(self, request, pk):
        if not request.user.is_manager:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ApproveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model = serializer.validated_data['model']
        instance = get_object_or_404(model, pk=pk)
        if instance.approver.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance.approved = True
        instance.save()
        return Response(status=status.HTTP_200_OK)
