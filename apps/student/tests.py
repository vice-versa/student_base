# -*- coding: utf-8 -*-
from django_webtest import WebTest, DjangoTestApp 
from django.core.urlresolvers import reverse
from margin.settings import MARGIN_TYPE_ABSOLUTE, MARGIN_TYPE_PERCENTAGE
from margin.models import Margin, MarginPrice, ProductPriceCriterion,\
    ProductDistrubutorCriterion
from lfs.criteria.settings import LESS_THAN, GREATER_THAN, IS, IS_NOT
from lfs.criteria.models.criteria_objects import CriteriaObjects
from lfs.catalog.models import Product, Category
from lfs.distributor.models import Distributor, ProductDistributorRelation
from django.contrib.auth.models import User
 

     

class MarginManagerTestCase(WebTest):
    
    fixtures = ['shop']
    
    def setUp(self):
        User.objects.create(username='admin', is_superuser=True)
    def testMainPages(self):
        
        response = self.app.get(reverse('lfs_manage_margins'), extra_environ=dict(REMOTE_USER='admin'))
        
    def testProductPriceMargin(self):
        app = DjangoTestApp(extra_environ=dict(REMOTE_USER='admin'))
        response = app.get(reverse("lfs_manage_add_margin"))                    
        
        form = response.form
        form.set('name', u'Наценка 20,3')
        form.set('value', 20.3)
        form.set('type', MARGIN_TYPE_ABSOLUTE)
        form.set('active', True)
        form.set('position', 1)
        form.submit()
        
        m = Margin.objects.latest('id')
        
        self.assertEqual(m.name, u'Наценка 20,3')
        self.assertEqual(m.value, 20.3)
        self.assertEqual(m.type, MARGIN_TYPE_ABSOLUTE)
        self.assertEqual(m.active, True)
        self.assertEqual(m.position, 1)
        
        product = Product.objects.create(name=u'test', price=200)
        category = Category.objects.create(name='test', slug="tests")
        category.products.add(product)
        lc = category.localcategory
        lc.new_margin = m 
        distributor = Distributor.objects.create(title='test',
                                                 short_title='test',
                                                 slug='test'
                                                 )
        pr_distr = ProductDistributorRelation.objects.create(price=200,
                                                             product=product,
                                                             distributor=distributor)
        
        m.save()
        
        ## Default margin  
        m.value = 40
        m.save()
        
        # get margin returns %
        # absolute 40 = 20 % 200.
        self.assertEqual(lc.get_margin(product), 20)

        # persentage 40 = 40% of 100
        m.type = MARGIN_TYPE_PERCENTAGE
        m.save()
        self.assertEqual(lc.get_margin(product), 40)
        
        ## Add margin price 
        m_price = MarginPrice.objects.create(margin=m,
                                             price=10,
                                             priority=1)
        m_price.save()
        # persentage 10 % from 200
        self.assertEqual(lc.get_margin(product), 10)

        # absolute 10 = 5 % 200
        m.type = MARGIN_TYPE_ABSOLUTE
        m.save()
        self.assertEqual(lc.get_margin(product), 5)
        
        # add criteria price LESS_THAN 200
        p_cr = ProductPriceCriterion(price=200, operator=LESS_THAN)
        p_cr.save()
        CriteriaObjects.objects.create(content=m_price, criterion=p_cr, position=1)
        
        # price less than 200 so use it
        pr_distr.price = 100
        pr_distr.save()
        self.assertEqual(lc.get_margin(product), 10)
        
        pr_distr.price = 400
        pr_distr.save()
        # price more than 200 so margin is default 40
        self.assertEqual(lc.get_margin(product), 10)
        
        # add criteria price GREATER_THAN 50
        p_cr = ProductPriceCriterion(price=50, operator=GREATER_THAN)
        p_cr.save()
        CriteriaObjects.objects.create(content=m_price, criterion=p_cr, position=2)
        
        m.type = MARGIN_TYPE_PERCENTAGE
        m.save()
        
        # price less than 200 so use 10
        pr_distr.price = 100
        pr_distr.save()
        self.assertEqual(lc.get_margin(product), 10)
        
        # price more than 200 so use default 40
        pr_distr.price = 400
        pr_distr.save()
        self.assertEqual(lc.get_margin(product), 40)

        # price less 200 and greater 50 so use 10
        pr_distr.price = 51
        pr_distr.save()
        self.assertEqual(lc.get_margin(product), 10)

        # price less 200 and less 50 so default 40
        pr_distr.price = 10
        pr_distr.save()
        self.assertEqual(lc.get_margin(product), 40)
        

    def test_distributor_criterion(self):

        m = Margin.objects.create(name=u'test',value=40, type=MARGIN_TYPE_ABSOLUTE, active=True)

        product = Product.objects.create(name=u'test', price=200)
        category = Category.objects.create(name='test', slug="tests")
        category.products.add(product)
        lc = category.localcategory
        lc.new_margin = m 
        distributor = Distributor.objects.create(title='test',
                                                 short_title='test',
                                                 slug='test'
                                                 )
        pr_distr = ProductDistributorRelation.objects.create(price=200,
                                                             product=product,
                                                             distributor=distributor)
        
        m.save()

        distributor2 = Distributor.objects.create(title='test',
                                                  short_title='test',
                                                  slug='test2'
                                                  )
        
        
        m_price = MarginPrice.objects.create(margin=m,
                                             price=10,
                                             priority=1)
        m_price.save()

        # margin absolute no criterion, price  10 = 5 % 200 
        self.assertEqual(lc.get_margin(product), 5)

        p_cr = ProductDistrubutorCriterion.objects.create(operator=IS)
        p_cr.distributor.add(distributor)
        CriteriaObjects.objects.create(content=m_price, criterion=p_cr, position=1)
        
        # product.best_distrib == criterion_distrib
        # margin absolute criterion IS, use criterion price 5% = 10 % 200 
        self.assertEqual(lc.get_margin(product), 5)
        
        p_cr.operator = IS_NOT
        p_cr.save()
        # product.best_distrib == criterion_distrib
        # margin absolute criterion IS_NOT, use price default 20% = 40 / 200 
        self.assertEqual(lc.get_margin(product), 20)
        
        # add criterion 
        p_cr2 = ProductPriceCriterion(price=50, operator=LESS_THAN)
        p_cr2.save()
        CriteriaObjects.objects.create(content=m_price, criterion=p_cr2, position=2)
        
        # set operation IS
        p_cr.operator = IS
        p_cr.save()
        
        # product.best_distrib == criterion_distrib
        # margin absolute criterion IS,
        # but price 200 more than second criteria so use default  20% = 40 / 200 
        self.assertEqual(lc.get_margin(product), 20)
        
        # set operator 
        p_cr2.operator = GREATER_THAN
        p_cr2.save()
        
        # product.best_distrib == criterion_distrib
        # margin absolute criterion IS,
        # price 200 less than second criteria so use margin price 5% = 10 / 200 
        self.assertEqual(lc.get_margin(product), 5)
        