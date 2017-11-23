class TicketDetail(object):
	"""docstring for TicketDetail

			Attributes:
				date: string date of program
				month: string month of program
				year: string year of program
				available_ticket: string available ticket count
				program_language: string language of program
				start_time: strng program starting time

	"""


	def __init__(self, date, month,
		year, available_ticket,program_language, start_time):
		"""TicketDetail Class with all ticket information"""
		self.date = date
		self.month = month
		self.year = year
		self.available_ticket = available_ticket
		self.program_language = program_language
		self.start_time = start_time
