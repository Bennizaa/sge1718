# -*- coding: utf-8 -*-i

from odoo import models, fields, api
from datetime import datetime, timedelta
     
class comunity(models.Model):
     _name = 'excontrolador.comunity'

     name = fields.Char()
     country = fields.Many2one('res.country')

class province(models.Model):
     _name = 'excontrolador.province'

     name = fields.Char()
     comunity = fields.Many2one('excontrolador.comunity')

class town(models.Model):
     _name = 'excontrolador.town'

     name = fields.Char()
     province = fields.Many2one('excontrolador.province')

class street(models.Model):
     _name = 'excontrolador.street'

     name = fields.Char()
     town = fields.Many2one('excontrolador.town')


class shipping(models.Model):
     _name = 'excontrolador.shipping'

     name = fields.Char()
     street = fields.Many2one('excontrolador.street')
     town = fields.Many2one(related='street.town')
     province = fields.Many2one(related='street.town.province')
     comunity = fields.Many2one(related='street.town.province.comunity')

     townaux = fields.Many2one('excontrolador.town', store=False)
     provinceaux = fields.Many2one('excontrolador.province', store=False)
     comunityaux = fields.Many2one('excontrolador.comunity', store=False)

     address = fields.Char()

     @api.onchange('comunityaux')
     def _filter_province(self):
        print "comunity"
        return { 'domain': {'provinceaux': [('comunity','=',self.comunityaux.id)]} }   

     @api.onchange('provinceaux')
     def _filter_town(self):
        print "province"+str(self.provinceaux.id)
        return { 'domain': {'townaux': [('province','=',self.provinceaux.id)]} }   

     @api.onchange('townaux')
     def _filter_street(self):
        print "town"
        return { 'domain': {'street': [('town','=',self.townaux.id)]} }   


     ######################################################################
     #################Coses en les dates###################################

     ship_date = fields.Datetime(default=lambda self: fields.Datetime.now())
     estimated_time = fields.Integer(string="Estimated time in hours",default=1)
     delivery_date = fields.Datetime(compute='_get_delivery')
     return_date = fields.Datetime()
     days_before_return = fields.Float(compute='_get_days')
          

     @api.depends('ship_date','estimated_time')
     def _get_delivery(self):
       for i in self:
        if i.ship_date != False:
         data=fields.Datetime.from_string(i.ship_date)
         data=data+timedelta(hours=i.estimated_time)
         i.delivery_date=fields.Datetime.to_string(data)

     @api.depends('return_date','estimated_time','delivery_date')
     def _get_days(self):
       for i in self:
        if i.return_date != False:
         delivery_date=fields.Datetime.from_string(i.delivery_date)
         return_date=fields.Datetime.from_string(i.return_date)
         diff=return_date-delivery_date
         i.days_before_return = diff.total_seconds()/60/60/24


