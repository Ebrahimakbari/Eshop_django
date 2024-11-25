from django.db import models
from account_module.models import User
from project_module.models import product
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="کاربر", on_delete=models.CASCADE)
    is_paid = models.BooleanField(verbose_name='نهایی/غیر نهایی')
    date = models.DateTimeField(verbose_name="تاریخ", auto_now=False, auto_now_add=False,blank=True,null=True)
    
    def get_total(self):
        total_price = 0
        if self.is_paid:
            for order in self.orderdetail_set.all():
                total_price += order.count *order.final_price
        else:
            for order in self.orderdetail_set.all():
                total_price += order.count *order.products.price
        return total_price

    def __str__(self) -> str:
        return str(self.user)

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name="سبد خرید", on_delete=models.CASCADE)
    products = models.ForeignKey(product, verbose_name="کالا", on_delete=models.CASCADE)
    final_price = models.IntegerField(verbose_name='قیمت نهایی',blank=True,null=True)
    count = models.IntegerField(verbose_name="تعداد")
    
    def get_full_price(self):
        return self.products.price * self.count

    def __str__(self) -> str:
        return str(self.order)

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبد های خرید'