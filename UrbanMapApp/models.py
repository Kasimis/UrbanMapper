from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ημ/νία Ενημέρωσης")

    def calculate_priority_score(self):
        """
        Calculates a priority score for the report.
        Only calculates for pending or in-progress reports.
        """
        if self.status == 'RESOLVED':
            return 0  # Resolved reports have no priority

        # --- Algorithm Parameters ---
        VOTE_WEIGHT = 10  # Each vote is worth 10 points
        DAY_WEIGHT = 1  # Each day the report is pending is worth 1 point

        # --- Calculations ---
        # 1. Calculate vote score
        vote_count = self.votes.count()
        vote_score = vote_count * VOTE_WEIGHT

        # 2. Calculate age score
        now = timezone.now()
        age = now - self.created_at
        days_pending = age.days
        age_score = days_pending * DAY_WEIGHT

        # 3. Final Score
        total_score = vote_score + age_score
        return total_score

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        return f"'{self.title}' από {self.user.username}"


# votes model
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='votes', verbose_name="Report")

    class Meta:
        unique_together = ('user', 'report')
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __str__(self):
        return f"Vote from {self.user.username} for the report '{self.report.title}'"