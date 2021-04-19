from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from app.trycheck import *
from django.http import HttpResponse
#from google.appengine.api import memcache
from app.word_cloud import *
from app.para_phrase import *
import csv
import time
import datetime
from app.grading import *
from app.maketable import *
import random
import re
x=nltk.download('averaged_perceptron_tagger')

userid=0
@csrf_exempt
def delques(request):
	if request.method=="POST":
		q=request.POST.get('SI')
		obj=QuestionData.objects.filter(SI=q)
		obj.delete()
		obj=QuestionData.objects.all()
		quesid=[]
		dic={}
		lt=[]
		for elt in obj:
			dic={'QuesNo':elt.SI,
				'Ques':elt.Question,
				'Cate':elt.Question_type,
				'Ans':elt.Answer,}
			lt.append(dic)
			quesid.append(elt.SI)
		return render(request,'admindash.html',{'table':lt,'quesid':quesid})
@csrf_exempt
def addques(request):
	if request.method=="POST":
		q=request.POST.get('ques')
		c=request.POST.get('cate')
		a=request.POST.get('ans')
		x=1
		quesid=[]
		qid='Q'+str(x)
		while QuestionData.objects.filter(SI=qid).exists():
			x=x+1
			qid='Q'+str(x)
		x=int(x)
		obj=QuestionData(SI=qid,Question=q,Question_type=c,Answer=a)
		obj.save()
		obj=QuestionData.objects.all()
		dic={}
		lt=[]
		for elt in obj:
			dic={'QuesNo':elt.SI,
				'Ques':elt.Question,
				'Cate':elt.Question_type,
				'Ans':elt.Answer,}
			lt.append(dic)
			quesid.append(elt.SI)
		return render(request,'admindash.html',{'table':lt,'quesid':quesid})
@csrf_exempt
def admincheck(request):
	if request.method=="POST":
		d=0
		uid=request.POST.get('userid')
		upass=request.POST.get('pswrd')
		if uid=="admin@aiguru.ninja" and upass=="12345":
			d=1
		obj=QuestionData.objects.all()
		dic={}
		lt=[]
		quesid=[]
		for elt in obj:
			dic={'QuesNo':elt.SI,
				'Ques':elt.Question,
				'Cate':elt.Question_type,
				'Ans':elt.Answer,}
			lt.append(dic)
			quesid.append(elt.SI)
		if d==1:
			return render(request,'admindash.html',{'table':lt,'quesid':quesid})
		else:
			return render(request,'admin.html',{})

def adminpage(request):
	return render(request,'admin.html',{})
def start(request):
	#client=memcache.Client(['127.0.0.1:8000'],debug=0) 
	name=request.session['name']
	t=time.time()
	obj=QuestionData.objects.all()
	dict={}
	list=[]
	for elt in obj:
		dict[elt.Question]=elt.Question_type
		list.append(elt.Question)

	length=len(list)

	index=random.randint(1,length-1)
	topic=list[index]
	desc=dict[topic]
	#topic=
	#des=desc[index]
	request.session['starttime']=t
	#print(session['starttime'])
	return render(request, 'index.html',{'name':name,'topic':topic,'desc':desc})

def register(request):
        #client.flush_all()

        #obj=GiveTake.objects.all().delete()
        return render(request, 'Login.html',{})
def login(request):
	return render(request, 'Reg.html',{})
def checkscorepage(request):
	obj=EssayData.objects.all()
	#client=memcache.Client(['127.0.0.1:8000'],debug=0)
	#dictionary_of_paras=perplexity.RunThis(t) 
	email=request.session['email']
	d=0
	context={}
	data={}
	table=[]
	for elt in obj:
		if elt.userid==email:
			d=1
			dictionary_of_paras=perplexity.RunThis(elt.essay) 
			#print(dictionary_of_paras)
			for key,value in dictionary_of_paras.items():
				rate=value[0]
				status=value[1]
				data={'paras':key,
					'dv_rate':rate,
					'final_status':status,
					}
				table.append(data)
	if d==1:
		return render(request, "Cohession.html" , {'tags':table})
	else:
		return render(request, "Cohession.html" , {})
def opencohession(request):
	#client=memcache.Client(['127.0.0.1:8000']) 
	name=request.session['name']
	return render(request,'Cohession.html',{'name':name})
@csrf_exempt
def checkcohession(topic,text,mail_id):
	obj=CohessionData.objects.all().delete()
	result=check_cohession(text[3:len(text)-4],topic)
	p_rep=str(result['Phrase repitions'])
	s_rep=str(result['Sentence repitions'])
	preplex_score=str(result['Preplexity score'])
	relevance=str(result['RElevance Score'])
	para=str(result['Paragraphs'])
	dictionary_of_paras=result['dictionary']
	obj=CohessionData(email=mail_id,p_rep=p_rep,s_rep=s_rep,preplex_score=preplex_score,relevance=relevance,para=para)
	obj.save()
	table={
			'p_rep':p_rep,
			's_rep':s_rep,
			'preplex_score':preplex_score,
			'relevance':relevance,
			'para':para
	}
	
	context = {
			'data':table,
			'topic':topic
	}
	return context

@csrf_exempt
def checkscore(topic,data,timetaken,mail_id):
	obj=EssayData.objects.all().delete()
		#print(data[3:len(data)-4])
	obj=EssayData.objects.all()
	tk=TweetTokenizer()
	t=tk.tokenize(str(data))
	text=[]
	count=0
	for u in t:
		if len(u)>1:
			text.append(u)
			count+=1

	length = count
	spell = Check_spelling(str(data))
	grammer = Capitalize(str(data[3:len(data)-4]))
	art=check_articles(str(data))
	Graded_result=Main_fun(str(data))
	res=para_phrasing(str(data),topic)
	totalerror=int(spell)+int(grammer)+int(art)
	
	obj=ScoreData(userid=mail_id,topic=topic,essay=data,wordcount=length,para_phrasing=res,spellcheck=spell,grammercheck=grammer,articlecheck=art,error=totalerror,grade=Graded_result,totaltime=40,timetaken=timetaken)
	obj.save()
	obj=EssayData(userid=mail_id,topic=topic,essay=data,wordcount=length,para_phrasing=res,spellcheck=spell,grammercheck=grammer,articlecheck=art,error=totalerror,grade=Graded_result,totaltime=40,timetaken=timetaken)
		#mail_id=session['email']
	obj.save()
	obj=EssayData.objects.all()
	data_scores=[mail_id,topic,data,length,spell,grammer,art,Graded_result]
	#print(obj)
	data={}
	table=[]
	for elt in obj:
		if elt.userid==mail_id:
			d=1
			data={'topic':elt.topic,
				'grade':elt.grade,
				'wordcount':elt.wordcount,
				'para_phrasing':elt.para_phrasing,
				'spellcheck':elt.spellcheck,
				'grammercheck':elt.grammercheck,
				'articlecheck':elt.articlecheck,
				'error':elt.error,
				'timetaken':elt.timetaken,
				'totaltime':elt.totaltime}
			table.append(data)
	return table
def analyticspage(request):
	obj=ScoreData.objects.all()
	lt=[]
	a=1
	data=''
	email=request.session['email']
	for elt in obj:
		if elt.userid==email:
			l=[]
			l.append(elt.grade)
			l.append(elt.spellcheck)
			l.append(elt.grammercheck)
			l.append(elt.articlecheck)
			l.append(elt.timetaken)
			con={'ch':l,'idd':'Chart'+str(a),'topic':elt.topic}
			lt.append(con)
			code='''<div class="col-lg-4 col-md-6 mb-5">
            		<div class="product-item">
              		<canvas id="'''+'Chart'+str(a)+'''" width="400" height="400"></canvas>
              		<div class="px-4">
                	<h3><a href="#">'''+elt.topic+'''</a></h3>
              		</div>
            		</div>
          			</div>'''
			a=a+1
			data=data+code
	return render(request, 'Analytics.html',{'tags':lt,'data':data})

def wordcloudpage(request):
	obj=ScoreData.objects.all()
	lt=[]
	number=[]
	a=1
	email=request.session['email']
	#print(email)
	for elt in obj:
		#print(elt.userid,' essay=',elt.essay,' topic=',elt.topic)
		if len(elt.essay)==0:
			
			continue
		if elt.userid==email and len(elt.essay)!=0:
				data=elt.essay
				
				#print('essay=',data)
				cloud=generate_wordcloud(str(data))
				con={'cloud':cloud,'num':'Attempt '+str(a),'topic':elt.topic}
				lt.append(con)
				a=a+1
	return render(request, 'word.html',{'tags':lt})
@csrf_exempt
def choice(request):
	currenttime=time.time()
	starttime=request.session['starttime']
	if starttime <2400:
		timetaken=request.session['starttime']

	else:
		timetaken = (currenttime-starttime)
		request.session['starttime']= int(timetaken/60)
	name=request.session['name']
	if request.method=="POST":
		topic = request.POST.get('Topic')
		text = request.POST.get('text')
		Tag_Re=re.compile(r'<[^>]+>')
		text=Tag_Re.sub('',text)
		Tag_Re=re.compile(r'<[^>]+>')
		topic=Tag_Re.sub('',topic)
	return render(request, 'choice.html',{'name':name,'topic':topic,'text':text})

def version2(text):
	s=contractions(str(text))
	data={}
	table=[]
	data={'contractions':s}
	table.append(data)
	return table

	
@csrf_exempt
def choicemade(request):
	name=request.session['name']
	timetaken=request.session['starttime']
	if request.method=="POST":
		topic = request.POST.get('Topic')
		#print(topic)
		text = request.POST.get('text')
		import re
		Tag_Re=re.compile(r'<[^>]+>')
		text=Tag_Re.sub('',text)
		#print(text)
		Tag_Re=re.compile(r'<[^>]+>')
		topic=Tag_Re.sub('',topic)
		checkscore_status=request.POST.get('checkscore')
		cohession_status=request.POST.get('cohession')
		ver2=request.POST.get('version2')
		re=request.POST.get('redirect')
		table={}
		table2={}
		mail_id=request.session['email']
		table=checkscore(topic,text,timetaken,mail_id)
		table2=checkcohession(topic,text,mail_id)
		table3=version2(text)
		if checkscore_status=="GRAMMATICAL RANGE AND ACCURACY":
			return render(request, 'CheckScore.html',{'tags':table,'tag2':table2})
		elif cohession_status=="COHESION AND COHERENCE":
			return render(request, 'CheckCohession.html',{'tags':table2})
		elif ver2=="version2":
			return render(request,'ver2.html',{'tags':table3})
@csrf_exempt
def redirect(request):
	obj=CohessionData.objects.all()

	for elt in obj:
		table={
			'p_rep':elt.p_rep,
			's_rep':elt.s_rep,
			'preplex_score':elt.preplex_score,
			'relevance':elt.relevance,
			'para':elt.para
			}
	context = {
		'data':table,
		'topic':"topic"
			}


	return render(request, 'CheckCohession.html',{'tags':context})

def terms(request):
	return render(request, 'terms.html',{})


def rulespage(request):
	return render(request, 'RULES.html',{})
@csrf_exempt
def contactpage(request):
	if request.method=="POST":
		fn=request.POST.get('fname')
		ln=request.POST.get('lname')
		email=request.POST.get('email')
		subject=request.POST.get('subject')
		message=request.POST.get('message')
		obj=ContactData(fname=fn,lname=ln,email=email,subject=subject,message=message)
		con={'text':"We Will Get in touch with you soon !"}
		return render(request, 'regresult.html',con)
	else:
		return render(request, 'Contact.html',{})
@csrf_exempt
def saveuser(request):
	if request.method=="POST":
		text=' '
		n=request.POST.get('name')
		g=request.POST.get('gender')
		ph=request.POST.get('phone')
		p=request.POST.get('password')
		e=request.POST.get('email')
		ob=UserData.objects.all()
		d=0
		for elt in ob:
			if e==elt.email:
				d=1
				break
		if d==0:
			obj=UserData(name=n,password=p,email=e,gender=g,phone=ph,status='N')
			obj.save()
			#request.session['userid'] = e
			#client=memcache.Client(['127.0.0.1:8000']) 
			
			request.session['name']=str(n)
			request.session['userid']=str(e)
			request.session['email']=str(e)
			obj.save()		
			text='Account Created Successfully'
			context={'text':text,
					'name':n}
			return render(request,'policy.html',context)
		else:
			text='User Already Exists'
			context={'text':text}
			return render(request,'regresult.html',context)
@csrf_exempt
def checklogin(request):
	text=" "
	d=0
	e=request.POST.get('email')
	p=request.POST.get('password')
	obj=UserData.objects.all()
	name=''
	for elt in obj:
		if e==elt.email and p==elt.password and elt.status=='Y':
			d=1
			name=elt.name
			#client=memcache.Client(['127.0.0.1:8000']) 
			request.session['email']=e
			request.session['name']=elt.name
			break
		elif e==elt.email and p==elt.password and elt.status=='N':
			#client=memcache.Client(['127.0.0.1:8000']) 
			request.session['userid']=e
			request.session['email']=e
			#GiveTake.objects.filter().update(email=e)
			text=' '
			context={'text':text,
					'name':elt.name}
			return render(request,'policy.html',context)
			break
	if d==0:
		con={'text':"No User Found"}
		return render(request,"regresult.html",con)
	else:
		return render(request,'start.html',{'name':name})

def acceptpolicy(request):
	#client=memcache.Client(['127.0.0.1:8000']) 
	ei=request.session['email']
	name=request.session['name']
	obj=UserData.objects.filter(email=ei).update(status="Y")
	return render(request,'start.html',{'name':name})
