from django.db import models
from django.contrib.auth.models import User

# Create your models here.
MONTH = (
('January','January'),
('February','February'),
('March','March'),
('April','April'),
('May','May'),
('June','June'),
('July','July'),
('August','August'),
('September','September'),
('October','October'),
('November','November'),
('December','December'),
)

class Contributions(models.Model):
    name = models.CharField(max_length=100,null=True)
    month = models.CharField(max_length=50,choices=MONTH,null=True)
    amount = models.PositiveIntegerField(null=True)

    class Meta:
        verbose_name_plural = "Contribution"

    def __str__(self):
        return f'{self.name}-{self.month}-{self.amount}'

class LoansRequest(models.Model):
    members = models.ForeignKey(User,models.CASCADE, null=True)
    loan_amount = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Loan Application"

    def __str__(self):
        return f'{self.members}- Laon Request'
