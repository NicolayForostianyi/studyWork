from django.db import models


class Data(models.Model):
    number_of_error = models.IntegerField(verbose_name="номер ошибки")
    interval = models.IntegerField(verbose_name="интервал между ошибкаби")
    index = models.IntegerField(verbose_name="Индекс ошибки")

    class Meta:
        verbose_name = "Данные формы ошибки"
        verbose_name_plural = "Набор данных формы ошибки"


class ModelInfo(models.Model):
    size = models.IntegerField(verbose_name="Размер")
    dataForms = models.ForeignKey(Data, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = "Модель данных"
        verbose_name_plural = "Наборы данных для модели"
