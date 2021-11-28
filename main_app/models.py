from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models


class Rates(models.Model):  # Таблица Тарифы с полями
    rate_name = models.CharField('Название тарифа', max_length=50)
    fee = models.IntegerField('Стоимость тарифа (руб. в месяц)')
    provided_speed = models.IntegerField('Предоставляемая скорость (Мбит)')

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return str(self.pk) + ' - ' + self.rate_name


class ListOfServices(models.Model):  # Справочная таблица Список тарифов
    service_name = models.CharField('Название предоставляемой услуги', max_length=50)
    comments = models.TextField('Комментарии', max_length=250, blank=True)  # Необязательное поле

    class Meta:
        verbose_name = 'Предоставляемая услуга'
        verbose_name_plural = 'Список предоставляемых услуг'

    def __str__(self):
        return str(self.pk) + ' - ' + self.service_name


class ListOfEquip(models.Model):  # Справочная таблица Типы оборудования
    equip_type = models.CharField('Тип оборудования', max_length=50)
    comments = models.TextField('Комментарии', max_length=250, blank=True)  # Необязательное поле

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'

    def __str__(self):
        return str(self.pk) + ' - ' + self.equip_type


class Employees(models.Model):
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    mid_name = models.CharField('Отчетство', max_length=50, blank=True) # Необязательное поле
    post = models.CharField('Занимаемая должность', max_length=50)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return str(self.pk) + ' - ' + self.first_name + ' ' + self.last_name


class Clients(models.Model):
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    mid_name = models.CharField('Отчетство', max_length=50, blank=True, default=None)
    contract_number = models.CharField('Номер заключенного контракта', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        if self.mid_name is not '':
            return str(self.pk) + ' - ' + self.last_name + ' ' + self.first_name[0] + '.' + self.mid_name[0] + '.'
        else:
            return str(self.pk) + ' - ' + self.last_name + ' ' + self.first_name[0] + '.'


class CustomersEquipment(models.Model):
    equip_name = models.CharField('Название оборудования', max_length=50)
    serial_number = models.CharField('Серийный номер', max_length=50)

    class Meta:
        verbose_name = 'Клиентское оборудование'
        verbose_name_plural = 'Клиентское оборудование'

    def __str__(self):
        return str(self.pk) + ' - ' + self.equip_name + ': ' + self.serial_number


class Equipment(models.Model):
    equip_name = models.CharField('Название оборудования', max_length=50)
    serial_number = models.CharField('Серийный номер', max_length=50)
    cequip_id = models.OneToOneField('CustomersEquipment', on_delete=models.SET_NULL,
                                     verbose_name='Клиентское оборудование', related_name='CuEquipment', null=True,
                                     blank=True)
    equip_type = models.ForeignKey('ListOfEquip', on_delete=models.SET_NULL, verbose_name='Тип оборудования',
                                   related_name='Equipment', null=True)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'

    def __str__(self):
        return str(self.pk) + ' - ' + self.equip_name


class Order(models.Model):
    STATUSES = (
        ('Создан', 'Создан'),
        ('Ожидает оплаты', 'Ожидает оплаты'),
        ('Ожидает заключения контракта', 'Ожидает заключения контракта'),
        ('Ожидание подготовки оборудования', 'Ожидание подготовки оборудования'),
        ('Ожидает выполнения услуг', 'Ожидает выполнения услуг'),
        ('Отложен', 'Отложен'),
        ('Завершен', 'Завершен'),
        ('Отменен', 'Отменен')
    )
    connection_date = models.DateField('Дата подключения', default=timezone.now, blank=True)
    status = models.CharField('Статус заказа', choices=STATUSES, max_length=40, default='Создан')
    client = models.ForeignKey('Clients', on_delete=models.CASCADE, verbose_name='Клиент',
                               related_name='Client', null=False)
    rate = models.ForeignKey('Rates', on_delete=models.SET_NULL, verbose_name='Тариф', related_name='Rate',
                             null=True)
    services = models.ManyToManyField('ListOfServices', verbose_name='Предоставляемые услуги',
                                      related_name='Orders')
    employees = models.ManyToManyField('Employees', verbose_name='Исполнители',
                                       related_name='Orders')
    customers_equipment = models.ForeignKey('CustomersEquipment', on_delete=models.SET_NULL,
                                            verbose_name='Оборудование', related_name='order', null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ №' + str(self.id)
