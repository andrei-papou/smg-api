from django.db import models


class DepartmentSpecialization(models.Model):
    name = models.CharField(max_length=255)


class Department(models.Model):
    name = models.CharField(max_length=4)
    specialization = models.ForeignKey('departments.DepartmentSpecialization')
    room = models.CharField(max_length=8)

    @property
    def manager(self):
        return self.members.filter(is_manager=True).one()
