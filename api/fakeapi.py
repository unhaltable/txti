import dbhelper

def fake_an_api(l, number):
	#this is slower than it has to be
	session = dbhelper.db_session()
	uid = session.uid_by_number(number)
	out = session.api_data_from_uid(uid)

	s = str(out)
	session.close()

	return s