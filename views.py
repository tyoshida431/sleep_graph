from django.http import HttpResponse
from .models import Sleeps
from .models import SleepProspects
from .models import DeepSleepProspects
from .models import Percent
import datetime
import matplotlib.pyplot as plt
from django.shortcuts import render
import io

def index(request):
    return render(request,'graph/index.html')

def deep_sleep(request):
    return render(request,'graph/deep_sleep.html')

def setSleepPlt():
    sleep_prospects=SleepProspects.objects.first()
    prospect_year=sleep_prospects.year
    prospect_season=sleep_prospects.season
    prospect_month=sleep_prospects.month
    prospect_week=sleep_prospects.week
    # TODO : per_...をクラスにして返却する関数を作ること。
    setPlt(prospect_year,prospect_season,prospect_month,prospect_week)

def makePlt(percent):
    per_year=percent.per_year
    per_season=percent.per_season
    per_month=percent.per_month
    per_week=percent.per_week
    fig=plt.figure()
    ax1=fig.add_subplot(4,1,1)
    ax1.set_title('year')
    plt.ylim(0.1,100)
    plt.subplots_adjust(wspace=0.5, hspace=0.8)
    ax2=fig.add_subplot(4,1,2)
    ax2.set_title('season')
    plt.ylim(0.1,100)
    plt.subplots_adjust(wspace=0.5, hspace=0.8)
    ax3=fig.add_subplot(4,1,3)
    ax3.set_title('month')
    plt.ylim(0.1,100)
    plt.subplots_adjust(wspace=0.5, hspace=0.8)
    ax4=fig.add_subplot(4,1,4)
    ax4.set_title('week')
    plt.ylim(0.1,100)
    year_y=range(len(per_year))
    ax1.plot(year_y,per_year)
    season_y=range(len(per_season))
    ax2.plot(season_y,per_season)
    month_y=range(len(per_month))
    ax3.plot(month_y,per_month)
    month_y=range(len(per_week))
    ax4.plot(month_y,per_week)

def setPlt(prospect_year,prospect_season,prospect_month,prospect_week):
    current_year=datetime.datetime.now().year
    start_date=datetime.date(current_year,1,1)
    end_date=datetime.date(current_year,12,31)
    sleeps=Sleeps.objects.filter(date__range=(start_date,end_date))
    # 目標。
    #sleep_prospects=SleepProspects.objects.first()
    #prospect_year=sleep_prospects.year
    #prospect_season=sleep_prospects.season
    #prospect_month=sleep_prospects.month
    #prospect_week=sleep_prospects.week
    year_sum=0
    season_sum=0
    month_sum=0
    week_sum=0
    per_year=[]
    per_season=[]
    per_month=[]
    per_week=[] 
    year_count=0
    season_count=0
    month_count=0
    week_count=0
    for sleep in sleeps:
      if sleep.sleep=="":
          break
      year_sum+=convert_to_min(sleep.sleep)
      year_count+=1
      per_year.append(calc_percent(prospect_year,year_sum))
      if is_now_season(sleep):
          season_sum+=convert_to_min(sleep.sleep)
          per_season.append(calc_percent(prospect_season,season_sum))
          season_count+=1
      if is_now_month(sleep):
          month_sum+=convert_to_min(sleep.sleep)
          per_month.append(calc_percent(prospect_month,month_sum))
          month_count+=1
      if is_now_week(sleep):
          #print(sleep.date)
          week_sum+=convert_to_min(sleep.sleep)
          per_week.append(calc_percent(prospect_week,week_sum))
          week_count+=1
    for i in range(365-year_count):
        per_year.append(0)
    for i in range(91-season_count):
        per_season.append(0)
    for i in range(31-month_count):
        per_month.append(0)
    for i in range(7-week_count):
        per_week.append(0) 
    fig=plt.figure()
    ax1=fig.add_subplot(4,1,1)
    ax1.set_title('year')
    plt.ylim(0.1,100)
    plt.subplots_adjust(wspace=0.5, hspace=0.8)
    ax2=fig.add_subplot(4,1,2)
    ax2.set_title('season')
    plt.ylim(0.1,100)
    plt.subplots_adjust(wspace=0.5, hspace=0.8)
    ax3=fig.add_subplot(4,1,3)
    ax3.set_title('month')
    plt.ylim(0.1,100)
    plt.subplots_adjust(wspace=0.5, hspace=0.8)
    ax4=fig.add_subplot(4,1,4)
    ax4.set_title('week')
    plt.ylim(0.1,100)
    year_y=range(len(per_year))
    ax1.plot(year_y,per_year)
    season_y=range(len(per_season))
    ax2.plot(season_y,per_season)
    month_y=range(len(per_month))
    ax3.plot(month_y,per_month)
    month_y=range(len(per_week))
    ax4.plot(month_y,per_week)
    #plt.savefig("sleep.png")
    #return HttpResponse("Hello, This is Django Polls")

def pltToSvg():
    buf=io.BytesIO()
    plt.savefig(buf,format='png', bbox_inches='tight')
    s=buf.getvalue()
    buf.close()
    return s

def get_png(request):
    #setPlt()
    setSleepPlt()
    png=pltToSvg()
    plt.cla()
    response=HttpResponse(png,content_type='image/png+xml')
    return response

def calc_percent(prospect,progress):
    ret=0.0
    # 100:x=prospect:progress
    # x=100*progress/prospect
    ret=100.0*progress/prospect
    return ret

def convert_to_min(time):
    ret=0
    if time!="":
      times=time.split(":")
      #print(times)
      ret+=int(times[1])
      ret+=int(times[0])*60
      #print(time)
    return ret

def is_now_season(sleep):
    ret=False
    now_month=datetime.datetime.now().month
    season_start=0
    season_end=0
    if now_month<=3:
      season_start=1
      season_end=3
    elif 4<=now_month and now_month<=6:
      season_start=4
      season_end=6
    elif 7<=now_month and now_month<=9:
      season_start=7
      season_end=9
    elif 10<=now_month and now_month<=12:
      season_start=10
      season_end=12

    month=sleep.date.month
    if season_start<=month and month<=season_end:
        ret=True

    return ret

def is_now_month(sleep):
    ret=False
    now_month=str(datetime.datetime.now().month)
    now_month=now_month.zfill(2)
    date=sleep.date.strftime('%Y-%m-%d')
    #print(now_month)
    #print(date)
    dates=date.split("-")
    #print(dates[1])
    if dates[1]==now_month:
      ret=True
    return ret

def is_now_week(sleep):
    if not is_now_month(sleep):
        return False

    ret=False
    #print(datetime.date.today())
    #print(datetime.date.today().strftime('%a'))
    # Monday : 0
    #print(datetime.date.today().weekday())
    weekday=datetime.date.today().weekday()
    date_tmp=sleep.date.strftime('%Y-%m-%d')
    date_list=date_tmp.split("-")
    date_str=date_list[2]
    date=int(date_str)
    now_day=datetime.datetime.now().day
    #print(date)
    #print(now_day)
    #print(weekday)
    # 日曜日始まりにします。
    sunday=now_day-(weekday+1)
    #print(sunday)
    saturday=now_day+(5-weekday)
    #print(saturday)
    if sunday<=date and date<=saturday:
        ret=True

    return ret
