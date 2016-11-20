from datetime import datetime

from django.db import models
from apollo.utils import utc


class Shot(models.Model):

    term_01 = models.DecimalField(default=0.0, max_digits=8, decimal_places=5)
    term_02 = models.DecimalField(default=0.0, max_digits=8, decimal_places=5)
    term_03 = models.DecimalField(default=0.0, max_digits=8, decimal_places=5)
    term_04 = models.DecimalField(default=0.0, max_digits=8, decimal_places=5)
    term_05 = models.DecimalField(default=0.0, max_digits=8, decimal_places=5)
    water_sensor = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def title(self):
        return '%s %s/%s' % (self.human_date, self.term_01, self.term_02)

    @property
    def human_date(self):
        delta = datetime.now(utc) - self.created
        if delta.total_seconds() < 60 * 60:
            return 'just now'
        elif delta.total_seconds() < 60 * 60 * 5:
            return '%sh ago' % str(int(delta.total_seconds() / (60 * 60)))
        elif delta.total_seconds() < 60 * 60 * 24:
            return 'today'
        elif delta.total_seconds() < 60 * 60 * 24 * 7:
            return '%sd ago' % str(int(delta.total_seconds() / (60 * 60 * 24)))
        else:
            return self.created.strftime('%b %d')

    def as_dict(self):
        return {'id': self.id, 'date': self.human_date, 'text': self.title,
                'term_01': self.term_01, 'term_02': self.term_02, 'term_03': self.term_03,
                'term_04': self.term_04, 'term_05': self.term_05, 'water_sensor': self.water_sensor}
