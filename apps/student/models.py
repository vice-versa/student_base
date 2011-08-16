# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from lfs.criteria.models.criteria_objects import CriteriaObjects

from margin.settings import MARGIN_TYPE_CHOICES, MARGIN_TYPE_PERCENTAGE,\
    MARGIN_TYPE_ABSOLUTE
from lfs.criteria.models.criteria import Criterion
from lfs.criteria.settings import NUMBER_OPERATORS, LESS_THAN, LESS_THAN_EQUAL,\
    GREATER_THAN, GREATER_THAN_EQUAL, EQUAL, IS
from django.template.loader import render_to_string
from django.template.context import RequestContext
from lfs.distributor.models import Distributor
from pwshop.models.criteria import CHOICE_OPERATORS
from pwshop.utils import FakeRequest

class Margin(models.Model):

    name = models.CharField(_("Name"), max_length=100)
    value = models.FloatField(_(u"Value"))
    type = models.PositiveSmallIntegerField(_(u"Type"), choices=MARGIN_TYPE_CHOICES, default=MARGIN_TYPE_PERCENTAGE)
    active = models.BooleanField(verbose_name=u'Активно', default=False)
    position = models.PositiveIntegerField(verbose_name=u'Порядок', default=999)

    class Meta:
        permissions = (
            ("manage_prices", "Can manage prices"),
             )

    def __unicode__(self):
        return self.name

    def get_margin(self, product):

        price = float(product.localproduct.get_best_distributor_price())
        if price <=0:
            return 0
        if self.prices.count():
            for p in self.prices.all():
                if p.is_valid(product):
                    return p.value(price)

        if self.type == MARGIN_TYPE_PERCENTAGE:
            return self.value
        else:
            return self.value / price * 100



class MarginPrice(models.Model):

    margin = models.ForeignKey(Margin, verbose_name=_(u"margin"), related_name="prices")
    price = models.FloatField(_(u"Price"), default=0.0)
    priority = models.IntegerField(_(u"Priority"), default=0)

    # NOTE: At the moment the active attribute is not used within the GUI.
    # We set it to True by default so every added shipping price is active immediately
    active = models.BooleanField(_(u"Active"), default=True)

    criteria_objects = generic.GenericRelation(CriteriaObjects,
        object_id_field="content_id", content_type_field="content_type")

    class Meta:
        ordering = ("priority", )

    def __unicode__(self):
        return u"%s" % self.price

    def is_valid(self, product):

        """The margin is valid if it has no criteria or if all assigned
        criteria are true.

        """
        request=FakeRequest()
        if self.criteria_objects.count():
            for criterion_object in self.criteria_objects.all():
                if not criterion_object.criterion.is_valid(request, product):
                    return False
        return True

    def value(self, price):
        if self.margin.type == MARGIN_TYPE_PERCENTAGE:
            return self.price
        elif self.margin.type == MARGIN_TYPE_ABSOLUTE:
            return self.price / price * 100

class ProductPriceCriterion(Criterion):
    """A criterion for the product price.
    """
    operator = models.PositiveIntegerField(_(u"Operator"), blank=True, null=True, choices=NUMBER_OPERATORS)
    price = models.FloatField(_(u"Price"), default=0.0)
    value_attr = 'price'

    content_type = u"product_price"
    name = _(u"Стоимость товара")

    def is_valid(self, request, product=None):
        """Returns True if the criterion is valid.

        If product is given the price is taken from the product otherwise from
        the cart.
        """

        price = product.localproduct.get_best_distributor_price()
        if price is None:
            return False
        if self.operator == LESS_THAN and (price < self.price):
            return True
        if self.operator == LESS_THAN_EQUAL and (price <= self.price):
            return True
        if self.operator == GREATER_THAN and (price > self.price):
            return True
        if self.operator == GREATER_THAN_EQUAL and (price >= self.price):
            return True
        if self.operator == EQUAL and (price == self.price):
            return True

        return False

    def as_html(self, request, position):
        """Renders the criterion as html in order to displayed it within several
        forms.
        """
        template = "manage/product_price_criterion.html"

        return render_to_string(template, RequestContext(request, {
            "id" : "ex%s" % self.id,
            "operator" : self.operator,
            "value" : self.value,
            "position" : position,
            "content_type" : self.content_type,
            "types" : [(ProductPriceCriterion.content_type, ProductPriceCriterion),
                       (ProductDistrubutorCriterion.content_type, ProductDistrubutorCriterion)
                       ]
        }))


class ProductDistrubutorCriterion(Criterion):
    """A criterion for the product distributor.
    """

    operator = models.PositiveIntegerField(_(u"Operator"), blank=True, null=True, choices=CHOICE_OPERATORS)
    distributor = models.ManyToManyField(Distributor, verbose_name=u"Поставщик")

    value_attr = 'distributor'
    multiple_value = True

    content_type = u"distributor"
    name = _(u"Поставщик")

    def __unicode__(self):
        values = []
        for value in self.value.all():
            values.append(value.title)

        return u"%s %s %s" % (self.name, self.get_operator_display(), u", ".join(values))

    def is_valid(self, request, product=None):

        rel = product.localproduct.get_best_distributor_relation()
        if rel is None:
            return False

        distributors = [d.id for d in self.distributor.all()]
        result = rel.distributor.id in distributors

        if self.operator == IS:
            return result
        else:
            return not result

    def as_html(self, request, position):
        """Renders the criterion as html in order to be displayed within several
        forms.
        """
        selected_distributors = self.distributor.all()
        distributors = []
        for d in Distributor.objects.all():
            if d in selected_distributors:
                selected = True
            else:
                selected = False

            distributors.append({
                "id" : d.id,
                "title" : d.title,
                "selected" : selected,
            })
        return render_to_string("manage/criteria/distributor_criterion.html", RequestContext(request, {
            "id" : "ex%s" % self.id,
            "operator" : self.operator,
            "value" : self.value,
            "position" : position,
            "distributors" : distributors,
            "content_type" : self.content_type,
            "types" : [(ProductPriceCriterion.content_type, ProductPriceCriterion),
                       (ProductDistrubutorCriterion.content_type, ProductDistrubutorCriterion)
                       ]
        }))

