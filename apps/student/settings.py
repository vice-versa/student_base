# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

MARGIN_TYPE_ABSOLUTE = 0
MARGIN_TYPE_PERCENTAGE = 1

MARGIN_TYPE_CHOICES = (
    (MARGIN_TYPE_ABSOLUTE, _(u"Absolute")),
    (MARGIN_TYPE_PERCENTAGE, _(u"Percentage")),
)