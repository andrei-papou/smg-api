from datetime import timedelta
import factory
from authentication.models import User
from departments.models import DepartmentSpecialization, Department
from out_of_office.models import TimeShift, BusinessLeave, Unpaid, Vacation, Illness


class DepartmentSpecializationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = DepartmentSpecialization

    name = factory.Faker('job')


class DepartmentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Department

    name = factory.Sequence(lambda n: 'D{}'.format(n))
    room = factory.Sequence(lambda n: 'Room {}'.format(n))
    specialization = factory.SubFactory(DepartmentSpecializationFactory)


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    patronymic = factory.Faker('first_name')
    phone = factory.Faker('phone_number')
    birthday = factory.Faker('date_time')
    employment_date = factory.Faker('date_time')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('ean13')
    skype = factory.Sequence(lambda n: 'skype_{}'.format(n))
    is_manager = False


class TimeShiftFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TimeShift

    start = factory.Faker('date_time')
    end = factory.LazyAttribute(lambda obj: obj.start + timedelta(hours=4))
    working_off_start = factory.LazyAttribute(lambda obj: obj.start + timedelta(days=1))
    comment = factory.Faker('sentence')
    approver = factory.SubFactory(UserFactory)
    employee = factory.SubFactory(UserFactory)


class BusinessLeaveFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = BusinessLeave

    start = factory.Faker('date_time')
    end = factory.LazyAttribute(lambda obj: obj.start + timedelta(hours=4))
    comment = factory.Faker('sentence')
    approver = factory.SubFactory(UserFactory)
    employee = factory.SubFactory(UserFactory)


class UnpaidFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Unpaid

    start = factory.Faker('date_time')
    end = factory.LazyAttribute(lambda obj: obj.start + timedelta(hours=4))
    comment = factory.Faker('sentence')
    approver = factory.SubFactory(UserFactory)
    employee = factory.SubFactory(UserFactory)


class VacationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Vacation

    start = factory.Faker('date_time')
    end = factory.LazyAttribute(lambda obj: obj.start + timedelta(hours=4))
    comment = factory.Faker('sentence')
    approver = factory.SubFactory(UserFactory)
    employee = factory.SubFactory(UserFactory)


class IllnessFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Illness

    start = factory.Faker('date_time')
    end = factory.LazyAttribute(lambda obj: obj.start + timedelta(hours=4))
    comment = factory.Faker('sentence')
    employee = factory.SubFactory(UserFactory)
