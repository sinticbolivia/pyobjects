import jinja2
import pdfkit
from sqlalchemy import func, cast, Date

from entities.record_history import RecordHistory 
import database
import config

class ModelReports:

	def __init__(self):
		self._template_loader = None
		self._template_env = None
		self._pdf_config = None
		self._prepare()
		
	def _prepare(self):
		self._template_loader = jinja2.FileSystemLoader(config.BASE_DIR + '/reports')
		self._template_env = jinja2.Environment(loader=self._template_loader)
		self._pdf_config = pdfkit.configuration(wkhtmltopdf=config.WKHTMLTOPDF_BIN_PATH)

	def buildGeneral(self):
		
		query = database.session.query(
			RecordHistory.creation_date,
			#func.count(RecordHistory.total_persons),
			func.sum(RecordHistory.total_persons).label('total_persons'),
			func.sum(RecordHistory.total_cars),
			func.sum(RecordHistory.total_motorcicles),
			func.sum(RecordHistory.total_animals)
		)
		#query = query.filter(payment.c.payment_date > '2005-05-25')
		items = query.group_by( cast(RecordHistory.creation_date, Date) ).all()
		
		print('items', items)
		context = {
			'nombre_usuario': 'Sof. Patricio Olaguivel',
			'items': items
		}
		template = self._template_env.get_template('reporte-general.html')
		output_html = template.render(context)
		pdfkit.from_string(output_html, 'reporte-general.pdf', configuration=self._pdf_config)
		
	def buildUsuario(self):
		
		context = {
			'nombre_usuario': 'Sof. Patricio Olaguivel',
			'items': []
		}
		template = self._template_env.get_template('reporte-usuario.html')
		output_html = template.render(context)
		pdfkit.from_string(output_html, 'reporte-general.pdf', configuration=self._pdf_config)
