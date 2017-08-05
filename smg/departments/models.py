from django.db import models


class DepartmentSpecialization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '#{} {}'.format(self.pk, self.name)


class Department(models.Model):
    name = models.CharField(max_length=4)
    specialization = models.ForeignKey('departments.DepartmentSpecialization')
    room = models.CharField(max_length=8)

    def __str__(self):
        return '{} {}'.format(self.name, self.specialization)

    @property
    def manager(self):
        return self.members.filter(is_manager=True).one()
