from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone 

from ..forms import AnswerForm 
from ..models import Question, Answer 

@login_required(login_url='common:login') #함수가 실행되기전에 로그인 됐는지 확인하고 안되면 로그인 페이지로 보내버린다. 
def answer_create(request,question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user #request.user가 바로 현재 로그인한 계정의 User모델 객체이다. 
            # AnserForm에 author필드가 없으므로 임시로 지정한는 것 
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # 
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id),answer.id))

    else:
        form = AnswerForm()
    context = {'question':question,'form':form}
    return render(request, 'pybo/question_detail.html',context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        # question_id는 주소의 숫자값 여기서는 pybo:detail이 pybo/까지고 question_id에 answer객체에 question필드에 아이디값을 부여한다. 
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id),answer.id))
        
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
