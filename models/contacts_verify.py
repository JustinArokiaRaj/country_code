from odoo import models,api,fields
from odoo.exceptions import ValidationError
import requests
import json


class ContactsVerify(models.Model):
	_inherit = 'res.company'

	email_api_key = fields.Char(string='EmailBox API Key')
	num_api_key = fields.Char(string='NumVerify API Key')
class Respartner(models.Model):
	_inherit = 'res.partner'

	phone_verify_state = fields.Selection([('draft','Draft'),('valid','Valid'),('invalid','Invalid')],default='draft',string="Phone State")
	email_verify_state = fields.Selection([('draft','Draft'),('valid','Valid'),('invalid','Invalid')],default='draft',string="Email State")


	@api.multi
	def verify_phone(self):
		if not self.country_id:
			raise ValidationError("Please choose your Country for Country Code..!")
		else:
			country_code = self.country_id.phone_code
			company = self.env.user.company_id
			api_key = company.num_api_key
			if api_key:
				api_endurl = 'http://apilayer.net/api/validate?access_key=%s&number=%s%s&country_code=&format=1' %(api_key,str(country_code),self.phone)
				response = requests.get(api_endurl)
				response_json = json.loads(response.text)
				if response_json:
					final_response = response_json['valid']
					if final_response == True:
						self.phone_verify_state = 'valid'
					elif final_response == False:
						self.phone_verify_state = 'invalid'
			else:
				raise ValidationError("Please Configure your Phone API in Company Settings ..!")

	@api.multi
	def verify_email(self):
		if self.email:
			company = self.env.user.company_id
			api_key = company.email_api_key
			if api_key:
				api_endurl = 'http://apilayer.net/api/check?access_key=%s&email=%s&smtp=1&format=1' %(api_key,self.email)
				response = requests.get(api_endurl)
				response_json = json.loads(response.text)
				if response_json:
					final_response = response_json['smtp_check']
					if final_response == True:
						self.email_verify_state = 'valid'
					elif final_response == False:
						self.email_verify_state = 'invalid'
			else:
				raise ValidationError("Please Configure your MailBox API in Company Settings ..!")



