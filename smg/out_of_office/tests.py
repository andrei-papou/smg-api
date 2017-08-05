import json
from datetime import datetime
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from common.factories import (
    TimeShiftFactory, UserFactory, DepartmentFactory, BusinessLeaveFactory, UnpaidFactory, VacationFactory,
    IllnessFactory
)
from out_of_office.models import OOOTypes


class TimeShiftTestCase(APITestCase):

    def setUp(self):
        self.department = DepartmentFactory()
        self.user = UserFactory(department=self.department)
        self.manager = UserFactory(is_manager=True)
        for i in range(5):
            user = UserFactory(department=self.department)
            TimeShiftFactory(employee=user, approver=self.manager)
        for i in range(5):
            TimeShiftFactory()

    def test_returns_department_only_to_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('ooo:time-shifts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_returns_all_to_manager(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(reverse('ooo:time-shifts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_returns_401_to_anon(self):
        response = self.client.get(reverse('ooo:time-shifts'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creates_time_shift_with_valid_data(self):
        data = {
            'start': datetime(2017, 9, 12, 16).isoformat(),
            'end': datetime(2017, 9, 12, 17).isoformat(),
            'comment': 'Some comment',
            'working_off_start': datetime(2017, 9, 21, 9).isoformat(),
            'approver': self.manager.pk
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ooo:time-shifts'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(response.data[key], value)

    def test_returns_400_when_data_is_invalid(self):
        data = {
            'start': 'some date',
            'end': 'some date'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ooo:time-shifts'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BusinessLeaveTestCase(APITestCase):

    def setUp(self):
        self.department = DepartmentFactory()
        self.user = UserFactory(department=self.department)
        self.manager = UserFactory(is_manager=True)
        for i in range(5):
            user = UserFactory(department=self.department)
            BusinessLeaveFactory(employee=user, approver=self.manager)
        for i in range(5):
            BusinessLeaveFactory()

    def test_returns_department_only_to_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('ooo:business-leaves'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_returns_all_to_manager(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(reverse('ooo:business-leaves'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_returns_401_to_anon(self):
        response = self.client.get(reverse('ooo:business-leaves'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creates_business_leave_with_valid_data(self):
        data = {
            'start': datetime(2017, 9, 12, 16).isoformat(),
            'end': datetime(2017, 9, 12, 17).isoformat(),
            'comment': 'Some comment',
            'approver': self.manager.pk
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ooo:business-leaves'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(response.data[key], value)

    def test_returns_400_when_data_is_invalid(self):
        data = {
            'start': 'some date',
            'end': 'some date'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ooo:business-leaves'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UnpaidTestCase(APITestCase):

    def setUp(self):
        self.department = DepartmentFactory()
        self.user = UserFactory(department=self.department)
        self.manager = UserFactory(is_manager=True)
        for i in range(5):
            user = UserFactory(department=self.department)
            UnpaidFactory(employee=user, approver=self.manager)
        for i in range(5):
            UnpaidFactory()

    def test_returns_department_only_to_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('ooo:unpaids'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_returns_all_to_manager(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(reverse('ooo:unpaids'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_returns_401_to_anon(self):
        response = self.client.get(reverse('ooo:unpaids'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creates_unpaid_with_valid_data(self):
        data = {
            'start': datetime(2017, 9, 12, 16).isoformat(),
            'end': datetime(2017, 9, 12, 17).isoformat(),
            'comment': 'Some comment',
            'approver': self.manager.pk
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ooo:unpaids'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(response.data[key], value)

    def test_returns_400_when_data_is_invalid(self):
        data = {
            'start': 'some date',
            'end': 'some date'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ooo:unpaids'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VacationTestCase(APITestCase):

    def setUp(self):
        self.department = DepartmentFactory()
        self.user = UserFactory(department=self.department)
        self.manager = UserFactory(is_manager=True)
        for i in range(5):
            user = UserFactory(department=self.department)
            VacationFactory(employee=user, approver=self.manager)
        for i in range(5):
            VacationFactory()

    def test_returns_department_only_to_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('ooo:vacations'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_returns_all_to_manager(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(reverse('ooo:vacations'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_returns_401_to_anon(self):
        response = self.client.get(reverse('ooo:vacations'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creates_vacation_with_valid_data(self):
        data = {
            'start': datetime(2017, 9, 12, 16).isoformat(),
            'end': datetime(2017, 9, 12, 17).isoformat(),
            'comment': 'Some comment',
            'approver': self.manager.pk
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ooo:vacations'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(response.data[key], value)

    def test_returns_400_when_data_is_invalid(self):
        data = {
            'start': 'some date',
            'end': 'some date'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ooo:vacations'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class IllnessTestCase(APITestCase):

    def setUp(self):
        self.department = DepartmentFactory()
        self.user = UserFactory(department=self.department)
        self.manager = UserFactory(is_manager=True)
        for i in range(5):
            user = UserFactory(department=self.department)
            IllnessFactory(employee=user)
        for i in range(5):
            IllnessFactory()

    def test_returns_department_only_to_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('ooo:illnesses'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_returns_all_to_manager(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(reverse('ooo:illnesses'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_returns_401_to_anon(self):
        response = self.client.get(reverse('ooo:illnesses'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creates_illness_with_valid_data(self):
        data = {
            'start': datetime(2017, 9, 12, 16).isoformat(),
            'end': datetime(2017, 9, 12, 17).isoformat(),
            'comment': 'Some comment'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ooo:illnesses'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(response.data[key], value)

    def test_returns_400_when_data_is_invalid(self):
        data = {
            'start': 'some date',
            'end': 'some date'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ooo:illnesses'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ApproveViewTestCase(APITestCase):

    def setUp(self):
        self.other_manager = UserFactory(is_manager=True)
        self.manager = UserFactory(is_manager=True)
        self.user = UserFactory()
        self.time_shift = TimeShiftFactory(employee=self.user, approver=self.manager)
        self.vacation = VacationFactory(employee=self.user, approver=self.manager)
        self.business_leave = BusinessLeaveFactory(employee=self.user, approver=self.manager)
        self.unpaid = UnpaidFactory(employee=self.user, approver=self.manager)

    def test_manager_can_approve(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.time_shift.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.TIME_SHIFT}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.time_shift.refresh_from_db()
        self.assertTrue(self.time_shift.approved)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.vacation.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.VACATION}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vacation.refresh_from_db()
        self.assertTrue(self.vacation.approved)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.business_leave.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.BUSINESS_LEAVE}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.business_leave.refresh_from_db()
        self.assertTrue(self.business_leave.approved)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.unpaid.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.UNPAID}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unpaid.refresh_from_db()
        self.assertTrue(self.unpaid.approved)

    def test_other_manager_has_no_access(self):
        self.client.force_authenticate(user=self.other_manager)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.time_shift.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.TIME_SHIFT}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.time_shift.refresh_from_db()
        self.assertFalse(self.time_shift.approved)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.vacation.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.VACATION}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.vacation.refresh_from_db()
        self.assertFalse(self.vacation.approved)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.business_leave.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.BUSINESS_LEAVE}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.business_leave.refresh_from_db()
        self.assertFalse(self.business_leave.approved)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.unpaid.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.UNPAID}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.unpaid.refresh_from_db()
        self.assertFalse(self.unpaid.approved)

    def test_non_manager_has_no_access(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.time_shift.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.TIME_SHIFT}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.time_shift.refresh_from_db()
        self.assertFalse(self.time_shift.approved)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.vacation.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.VACATION}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.vacation.refresh_from_db()
        self.assertFalse(self.vacation.approved)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.business_leave.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.BUSINESS_LEAVE}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.business_leave.refresh_from_db()
        self.assertFalse(self.business_leave.approved)

        response = self.client.patch(reverse('ooo:approve', kwargs={'pk': self.unpaid.pk}),
                                     data=json.dumps({'ooo_type': OOOTypes.UNPAID}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.unpaid.refresh_from_db()
        self.assertFalse(self.unpaid.approved)
