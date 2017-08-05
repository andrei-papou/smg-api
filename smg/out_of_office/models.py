from django.db import models


class OutOfOfficeRequest(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    comment = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def duration(self):
        return self.end - self.start


class TimeShift(OutOfOfficeRequest):
    employee = models.ForeignKey('authentication.User', related_name='time_shifts')
    approver = models.ForeignKey('authentication.User', related_name='approved_time_shifts')
    working_off_start = models.DateTimeField()

    @property
    def working_off_end(self):
        return self.working_off_start + self.duration


class BusinessLeave(OutOfOfficeRequest):
    employee = models.ForeignKey('authentication.User', related_name='business_leaves')
    approver = models.ForeignKey('authentication.User', related_name='approved_business_leaves')


class Unpaid(OutOfOfficeRequest):
    employee = models.ForeignKey('authentication.User', related_name='unpaids')
    approver = models.ForeignKey('authentication.User', related_name='approved_unpaids')


class Vacation(OutOfOfficeRequest):
    employee = models.ForeignKey('authentication.User', related_name='vacations')
    approver = models.ForeignKey('authentication.User', related_name='approved_vacations')


class Illness(models.Model):
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    comment = models.TextField(null=True, blank=True)
    employee = models.ForeignKey('authentication.User', related_name='illnesses')


class OOOTypes:
    TIME_SHIFT = 'time-shift'
    BUSINESS_LEAVE = 'business-leave'
    UNPAID = 'unpaid'
    VACATION = 'vacation'
    ILLNESS = 'illness'


ooo_mapping = {
    OOOTypes.TIME_SHIFT: TimeShift,
    OOOTypes.BUSINESS_LEAVE: BusinessLeave,
    OOOTypes.UNPAID: Unpaid,
    OOOTypes.VACATION: Vacation,
    OOOTypes.ILLNESS: Illness,
}
