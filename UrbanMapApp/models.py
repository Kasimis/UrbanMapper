from django.db import models
from django.contrib.auth.models import User


# category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Όνομα Κατηγορίας")
    description = models.TextField(blank=True, null=True, verbose_name="Περιγραφή")

    class Meta:
        verbose_name = "Κατηγορία"
        verbose_name_plural = "Κατηγορίες"

    def __str__(self):
        return self.name


# reports model
class Report(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Σε εκκρεμότητα'),
        ('IN_PROGRESS', 'Σε εξέλιξη'),
        ('RESOLVED', 'Επιλύθηκε'),
    ]

    # relations with other models
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Χρήστης που έκανε την αναφορά")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Κατηγορία")

    # basic info
    title = models.CharField(max_length=200, verbose_name="Τίτλος")
    description = models.TextField(verbose_name="Περιγραφή")
    photo = models.ImageField(upload_to='report_photos/', verbose_name="Φωτογραφία")

    # geolocation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Γεωγραφικό Πλάτος")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Γεωγραφικό Μήκος")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Διεύθυνση (προαιρετικά)")

    # meta-data
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Κατάσταση")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ημ/νία Δημιουργίας")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ημ/νία Ενημέρωσης")

    class Meta:
        verbose_name = "Αναφορά"
        verbose_name_plural = "Αναφορές"

    def __str__(self):
        return f"'{self.title}' από {self.user.username}"


# votes model
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Χρήστης")
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='votes', verbose_name="Αναφορά")

    class Meta:
        unique_together = ('user', 'report')
        verbose_name = "Ψήφος"
        verbose_name_plural = "Ψήφοι"

    def __str__(self):
        return f"Ψήφος από {self.user.username} για την αναφορά '{self.report.title}'"