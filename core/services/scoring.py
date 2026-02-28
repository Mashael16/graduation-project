from datetime import timedelta , time , datetime
import math

class ruleBase:

    def __init__(self,data):

        self.submissionTime =data["submissionTime"]
        self.deadline = data["deadline"]
        self.taskNum = data ["taskNum"]
        self.submissionScore = 0
        self.totalTaskScore = 0
        self.taskComplateAVR = data["taskComplateAVR"]
        self.ComplateScore = 0
        self.startWork =data["startWork"]
        self.endWork = data["endWork"]
        self.arrivalTime = data["arrivalTime"]
        self.startMeeting = data["startMeeting"]
        self.endMeeting = data["endMeeting"]
        self.arrivalMeeting = data["arrivalMeeting"]
        self.attendanceScore = 0
        self.dayNum = 0
        self.breachLevel = data ["breachLevel"]
        self.breachNum = 0
        self.totalBreachScore = 0
        self.importanceDegree = data["importanceDegree"]

    # فنكشن لمعيار الالتزام بوقت التسليم
    def submissionTimeRule(self):

        # حساب فرق الوقت والأيام
        timeDifferent = self.submissionTime - self.deadline
        # يحسب أجزاء اليوم ويقربها ليوم ( لو عندي تأخير يوم وساعتين يعتبر تأخير يومين)
        daysLate = math.ceil(timeDifferent.total_seconds() /(24*3600))

        # في حال التسليم في الوقت يحصل على 100 نقطة
        if self.submissionTime <= self.deadline:
            return 100

        # في حال التأخر خلال أول 24 ساعة يتم خصم 3 نقاط
        elif  timeDifferent <= timedelta(hours = 24):
            return 100 - 3

        #التأخير من يومين الى 4 أيام
        elif 2<= daysLate <= 4:
            return 100 - 3 -((daysLate-1)*4)

       # التأخير 5-7 أيام
        elif 5<= daysLate <= 7:
            return 100 - 15 -((daysLate-4)*5)

       # تأخير أكثر من 7 أيام
        else :
            return 100 - 30 -((daysLate-7)*10)


    # حساب معدل نقاط وقت التسليم خلال الشهر
    def submissionAverage(self):
        if self.taskNum == 1:
            self.submissionScore = 0
        self.submissionScore += self.submissionTimeRule() # تحسب مجموع النقاط
        submissionAVR = self.submissionScore / self.taskNum # تحسب المعدل للنقاط بناء على عدد المهام
        return submissionAVR


   # فنكشن تتحقق من اكتمال متطلبات المهمة
    def taskComplate (self):
        # اذا كمل 95 %
       if self.taskComplateAVR >=0.95:
           return 100

       elif 0.85 <= self.taskComplateAVR < 0.95 :
           return 100 - 10

       elif  0.75 <= self.taskComplateAVR < 0.85 :
            return 100 - 20

       elif  0.5 <= self.taskComplateAVR < 0.75 :
           return 100 - 35

       else :
           return 100 - 50


    # حساب معيار مدى أهمية المهمة لتحديد نسبة الخصم على الأداء والاكتمال
    def taskComplateScore (self):
        if self.taskNum == 1:
            self.ComplateScore = 0

        self.ComplateScore += self.taskComplate() # تحسب مجموع النقاط
        taskComplateScoreAVR = self.ComplateScore / self.taskNum # تحسب المعدل للنقاط بناء على عدد المهام
        return taskComplateScoreAVR


    # حساب معيار مدى أهمية المهمة
    def importance(self):
        #حساب عدد النقاط المخصومة من كل معيار
        submissionDeducation = 100 - self.submissionTimeRule()
        taskComplateDeducation = 100 - self.taskComplate()
        # مجموع نقاط الخصم
        totalDeducation = submissionDeducation + taskComplateDeducation
        # تصفير العداد اذا كانت أول مهمة في الشهر
        if self.taskNum == 1:
              self.totalTaskScore = 0
       # حساب نقاط الخصم لمعيار الأهمية بحسب درجة الأهمية
        if self.importanceDegree == 1:
           taskImportanceDeducation = totalDeducation * 0.20
        elif self.importanceDegree == 2:
           taskImportanceDeducation = totalDeducation * 0.10
        else:
           taskImportanceDeducation = 0
        # حساب النقاط بعد الخصم
        importanceScore = 100 - taskImportanceDeducation # قيمة النقاط بعد الخصم

        #حساب معدل النقاط خلال الشهر
        self.totalTaskScore += importanceScore
        importanceAVR = self.totalTaskScore / self.taskNum
        return importanceAVR

   # معيار حساب التأخير عن العمل والاجتماعات والغياب
    def workTime(self):
        today = datetime.today().date()
        # تحويل الوقت الى وقت و تاريخ لحساب التأخير
        start_datetime = datetime.combine(today, self.startWork)
        arrival_datetime = datetime.combine(today, self.arrivalTime)
        start_meetingtime = datetime.combine(today, self.startMeeting)
        arrival_meetingtime = datetime.combine(today, self.arrivalMeeting)

        workDelay = arrival_datetime - start_datetime
        meetingDelay = arrival_meetingtime -start_meetingtime
        # اذا التأخير أقل من ربع ساعة ما يحسب تأخير
        if workDelay <= timedelta(minutes = 14) :
            return 100
        # اذا التأخير ربع ساعة وفوق
        elif  workDelay >= timedelta(minutes =15):
            # حساب مجموع دقائق التأخير
            delayMinutes = workDelay.total_seconds() / 60
            # تحديد كم ربع ساعة تأخير
            timeDelay = math.ceil(delayMinutes / 15)
            # حساب الخصم( يخصم 3 نقاط عن كل ربع  ساعة)
            return 100 - (timeDelay * 3)

        # حساب الغياب ( خصم 30 نقطة على الغياب)
        elif arrival_datetime is None and  datetime.now() == self.endWork:
            return 100 - 30

        elif meetingDelay < timedelta(minutes = 5):
            return 100

        elif  timedelta(minutes = 5)<= meetingDelay <= timedelta(minutes = 10):
            return 90

        elif meetingDelay > timedelta(minutes = 10):
         return 85

        elif arrival_meetingtime is None and datetime.now() == self.endMeeting:
            return 80

    #حساب معدل الالتزام بالحضور خلال الشهر
    def workTimeAverage(self):
        #كل بداية شهر يتم حساب معدل حضور جديد
        if datetime.now()== 1:
            self.attendanceScore = 0
            self.dayNum = 0

        self.attendanceScore += self.workTime()
        self.dayNum += 1
        attendanceAVR = self.attendanceScore / self.dayNum
        return attendanceAVR


   # حساب خصومات الالتزام بسياسة الشركة
    def Breaches (self):
        # اذا ما فيه مخالفات
        if self.breachLevel is None :
            breachScore  = 100
            # مخالفة درجة أولى high
        elif self.breachLevel == 1:
            breachScore = 20
            #  moderate مخالفة درجة ثانية
        elif self.breachLevel == 2:
            breachScore = 70
            # مخالفة درجة ثالثة low
        elif self.breachLevel == 3:
            breachScore = 85
        if datetime == 1 :
            self.totalBreachScore = 0
            self.breachNum = 0

        self.totalBreachScore += breachScore
        self.breachNum +=1
        breachScoreAVR = self.totalBreachScore / self.breachNum
        return breachScoreAVR

    #نتيجة الscore النهائي
    def resultScore(self):
        # حساب محموع نقاط المهام المسلمة
        score_100 = (self.submissionAverage() * 0.20) + (self.taskComplateScore() * 0.20)+ (self.workTimeAverage() * 0.20) + (self.Breaches()* 0.20) + (self.importance() * 0.20)
        score_5 = score_100 / 20
        return score_5