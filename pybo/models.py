from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Question(models.Model):
    #author필드는 User모델을 ForeignKey로적용하여 선언했다. User모델은 장고모델에서 뽑아왔다. 작가가 지워지면 작가와 연결된 Question모델도 지워진다.   
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'author_question')  
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    # related_name를 지정해주어서 User모델을 통해 Question데이터에 접근할 경우 author필드로 접근할지 voter필드를 기준으로 할지 정해 주었다. 
    voter = models.ManyToManyField(User, related_name='voter_question')
    
    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    # null=True는 DB에서 modify_date칼럼에 null을 허용한다는 의미이며 
    # blank=True는 form.is_valid()를 통한 입력 폼 데이터 검사 시 값이 없어도 된다는 의미이다. 
    # 즉 어떤 조건으로든 값을 비워둘 수 있다. 수정일시는 수정한 경우에만 생성되는 데이터이므로 지정한거다 . 
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True,blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE) 
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


