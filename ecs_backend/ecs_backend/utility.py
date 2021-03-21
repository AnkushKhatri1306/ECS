import traceback

def exception_detail(e):
	try:
		print(e)
		print('exception -> ', traceback.format_exc())
	except Exception as e:
		print(e.args)


