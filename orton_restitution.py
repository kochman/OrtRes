#!/usr/bin/env python3

import gspread


class Restitution:

	def __init__(self, name, reason):
		self.name = name
		self.reason = reason

	def __str__(self):
		return '    {}: {}'.format(self.name, self.reason)


class Student:

	def __init__(self, name, email, restitutions):
		self.name = name
		self.email = email
		self.restitutions = restitutions

	def __repr__(self):
		return 'Student({}, {}, {})'.format(self.name, self.email, self.restitutions)

	def __str__(self):
		restitutions = ['    ' + str(rest) for rest in self.restitutions]
		return '{} <{}>\n{}'.format(self.name, self.email, '\n'.join(restitutions))


class OrtonRestitution:

	def __init__(self, gusername, gpassword, key):
		gc = gspread.login(gusername, gpassword)
		self.wks = gc.open_by_key(key).sheet1

	def get_all_students(self):
		students = []
		all_values = self.wks.get_all_values()
		progression = all_values[0][2:]  # Get restitution names from header row
		records = all_values[1:]  # Get assigned restitutions by excluding header
		for record in records:
			recorded_restitutions = record[2:]
			restitutions = []

			for i in range(len(progression)):
				if recorded_restitutions[i]:  # Don't add empty records
					restitution = Restitution(progression[i], recorded_restitutions[i])
					restitutions.append(restitution)

			student = Student(record[0], record[1], restitutions)
			students.append(student)
		return students

	def get_student(self, email):
		"""Return a Student identified by his email address."""
		for student in self.get_all_students():
			if student.email == email:
				return student
