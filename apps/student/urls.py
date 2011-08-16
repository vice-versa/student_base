# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('margin.views.manage.margins',
    url(r'^margins/$', "manage_margins", name="lfs_manage_margins"),
    url(r'^margin/(?P<id>\d+)$', "manage_margin", name="lfs_manage_margin"),
    url(r'^add-margin/', "add_margin", name="lfs_manage_add_margin"),
    url(r'^save-margin-data/(?P<id>\d+)$', "save_margin_data", name="lfs_manage_save_margin_data"),
    url(r'^delete-margin/(?P<id>\d+)$', "delete_margin", name="lfs_manage_delete_margin"),
    url(r'^add-margin-price/(?P<id>\d+)$', "add_margin_price", name="lfs_manage_add_margin_price"),
    url(r'^update-margin-prices/(?P<id>\d+)$', "update_margin_prices", name="lfs_manage_update_margin_prices"),
    url(r'^margin-price-criteria/(?P<id>\d+)$', "margin_price_criteria", name="lfs_manage_margin_price_criteria"),
    url(r'^save-margin-price-criteria/(?P<id>\d+)$', "save_margin_price_criteria", name="lfs_manage_save_margin_price_criteria"),
    url(r'^recalculate-margin/(?P<id>\d+)', "recalculate_margin", name="lfs_manage_recalculate_margin"),
)