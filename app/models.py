from django.db import models

class UserData(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	gender=models.CharField(max_length=50)
	password=models.CharField(max_length=50)
	phone=models.CharField(max_length=50)
	status=models.CharField(max_length=50)
	class Meta:
		db_table="UserData"
class ContactData(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	subject=models.CharField(max_length=50)
	message=models.CharField(max_length=50)
	class Meta:
		db_table="ContactData"

class QuestionData(models.Model):
	SI=models.CharField(max_length=100)
	Question_type=models.CharField(max_length=100)
	Question=models.CharField(max_length=50)
	Answer=models.CharField(max_length=50)
	grade=models.CharField(max_length=50)
	class Meta:
		db_table="QuestionData"

class CohessionData(models.Model):
	email=models.CharField(max_length=100)
	p_rep=models.CharField(max_length=100)
	s_rep=models.CharField(max_length=100)
	preplex_score=models.CharField(max_length=50)	
	relevance=models.CharField(max_length=50)
	para=models.CharField(max_length=50)
	class Meta:
		db_table="CohessionData"

class GiveTake(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	userid=models.CharField(max_length=100)
	starttime=models.CharField(max_length=100)
	class Meta:
		db_table="GiveTake"
		
class EssayData(models.Model):
	userid=models.CharField(max_length=100)
	topic=models.CharField(max_length=1000)
	essay=models.CharField(max_length=20000)
	wordcount=models.CharField(max_length=50)
	para_phrasing=models.CharField(max_length=50)
	spellcheck=models.CharField(max_length=50)
	grammercheck=models.CharField(max_length=50)
	articlecheck=models.CharField(max_length=50)
	error=models.CharField(max_length=50)
	grade=models.CharField(max_length=50)
	totaltime=models.CharField(max_length=50)
	timetaken=models.CharField(max_length=50)
	class Meta:
		db_table="EssayData"

class ScoreData(models.Model):
	userid=models.CharField(max_length=100)
	topic=models.CharField(max_length=1000)
	essay=models.CharField(max_length=20000)
	wordcount=models.CharField(max_length=50)
	para_phrasing=models.CharField(max_length=50)
	spellcheck=models.CharField(max_length=50)
	grammercheck=models.CharField(max_length=50)
	articlecheck=models.CharField(max_length=50)
	error=models.CharField(max_length=50)
	grade=models.CharField(max_length=50)
	totaltime=models.CharField(max_length=50)
	timetaken=models.CharField(max_length=50)
	class Meta:
		db_table="ScoreData"

class HtmlData(models.Model):
	filename=models.CharField(max_length=100)
	code=models.CharField(max_length=10000)
	class Meta:
		db_table="HTMLData"
