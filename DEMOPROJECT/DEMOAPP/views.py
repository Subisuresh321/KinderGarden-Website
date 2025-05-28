from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
import mysql.connector
from .forms import Video_form
from .models import Video

def hi(request):
    return render(request, 'DEMOAPP/index.html')


def home(request):
    return render(request, 'DEMOAPP/index.html')


def about(request):
    return render(request, 'DEMOAPP/about.html')


def contact(request):
    return render(request, 'DEMOAPP/contact.html')


def teacher(request):
    return render(request, 'DEMOAPP/teacher_signup.html')


def parent(request):
    return render(request, 'DEMOAPP/parent_signup.html')


def thome(request):
    if 'name' in request.session:
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT COUNT(*) FROM parent")
        parent_count = mycursor.fetchone()[0]
        mycursor.execute("SELECT COUNT(*) FROM demoapp_video")
        video_count = mycursor.fetchone()[0]
        fn = request.session['name']
        return render(request, 'DEMOAPP/teacherhome.html', {'name': fn,'parent_count': parent_count,'video_count': video_count})
    else:
        return render(request, 'DEMOAPP/teacherlogin.html', {'msg': 'Login to Continue'})


def ahome(request):
    if 'name' in request.session:
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT COUNT(*) FROM teacher where statusofapproval='Admitted'")
        teacher_count = mycursor.fetchone()[0]

        mycursor.execute("SELECT COUNT(*) FROM parent")
        parent_count = mycursor.fetchone()[0]
        mycursor.execute("SELECT COUNT(*) FROM demoapp_video")
        video_count = mycursor.fetchone()[0]
        fn = request.session['name']
        return render(request, 'DEMOAPP/adminhome.html',
                      {'name': fn, 'teacher_count': teacher_count, 'parent_count': parent_count,'video_count': video_count})
    else:
        return render(request, 'DEMOAPP/adminlogin.html', {'msg': 'Login to Continue'})


def phome(request):
    if 'name' in request.session:
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT COUNT(*) FROM teacher where statusofapproval='Admitted'")
        teacher_count = mycursor.fetchone()[0]
        cls = request.session['childclass']
        if isinstance(cls, list):
            cls = [c.lower() for c in cls]
            cls = cls[0]
            print(cls)
        else:
            cls = cls.lower()
        mycursor.execute('SELECT COUNT(*) FROM demoapp_video where classname="' +cls+ '"')
        video_count = mycursor.fetchone()[0]
        fn = request.session['name']
        return render(request, 'DEMOAPP/parenthome.html', {'name': fn,'teacher_count': teacher_count,'video_count': video_count})
    else:
        return render(request, 'DEMOAPP/parentlogin.html', {'msg': 'Login to Continue'})


def teachersignup(request):
    if request.method == "POST":
        name = request.POST["Name"]
        age = request.POST["Age"]
        gender = request.POST["Gender"]
        subject = request.POST["Subject"]
        contactno = request.POST["Contactno"]
        email = request.POST["Email"]
        password = request.POST["Password"]
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
        mycursor = mydb.cursor()
        q = "insert into teacher(name,age,gender,subject,contactno,email,password)values('" + name + "','" + age + "','" + gender + "','" + subject + "','" + contactno + "','" + email + "','" + password + "')"
        mycursor.execute(q)
        mydb.commit()
        return render(request, 'DEMOAPP/teacher_signup.html', {'msg': "TEACHER REGISTERED SUCCESSFULLY, WAIT FOR APPROVAL"})


def parentsignup(request):
    if request.method == "POST":
        name = request.POST["Name"]
        childname = request.POST["Childname"]
        childage = request.POST["Childage"]
        childdob = request.POST["Childdob"]
        childclass = request.POST["Childclass"]
        contactno = request.POST["Contactno"]
        email = request.POST["Email"]
        password = request.POST["Password"]
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
        mycursor = mydb.cursor()
        q = "insert into parent(name,childname,childage,childdob,childclass,contactno,email,password)values('" + name + "','" + childname + "','" + childage + "','" + childdob + "','" + childclass + "','" + contactno + "','" + email + "','" + password + "')"
        mycursor.execute(q)
        mydb.commit()
        return render(request, 'DEMOAPP/parent_signup.html', {'msg': "PARENT REGISTERED SUCCESSFULLY"})


def aloginf(request):
    return render(request, 'DEMOAPP/adminlogin.html')


def ploginf(request):
    return render(request, 'DEMOAPP/parentlogin.html')


def tloginf(request):
    return render(request, 'DEMOAPP/teacherlogin.html')


def alogin(request):
    if request.method == "POST":
        email = request.POST["Email"]
        password = request.POST["Password"]
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
        mycursor = mydb.cursor()
        mycursor1 = mydb.cursor()
        mycursor.execute("SELECT COUNT(*) FROM teacher where statusofapproval='Admitted'")
        teacher_count = mycursor.fetchone()[0]

        mycursor.execute("SELECT COUNT(*) FROM parent")
        parent_count = mycursor.fetchone()[0]
        mycursor.execute("SELECT COUNT(*) FROM demoapp_video")
        video_count = mycursor.fetchone()[0]

        request.session['username'] = email
        request.session['name'] = "Admin"
        q = "select * from admin where email='" + email + "'and password='" + password + "'"
        mycursor.execute(q)
        mycursor.fetchall()
        if mycursor.rowcount == 0:
            return render(request, 'DEMOAPP/adminlogin.html', {'msg': 'Invalid Email-Id and Password', 'name': 'Admin'})
        else:
            return render(request, 'DEMOAPP/adminhome.html',
                          {'teacher_count': teacher_count, 'name': 'Admin', 'parent_count': parent_count,'video_count':video_count  })


def adminhome(request):
    request.session['name'] = "Admin"
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM teacher where statusofapproval='Admitted'")
    teacher_count = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(*) FROM parent")
    parent_count = mycursor.fetchone()[0]
    return render(request, 'DEMOAPP/adminhome.html', {'teacher_count': teacher_count, 'parent_count': parent_count})


def tlogin(request):
    if request.method == "POST":
        email = request.POST["Email"]
        password = request.POST["Password"]
        a="admitted"
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
        mycursor = mydb.cursor()
        #print(row[0])
        q1 = "select name from teacher where email='" + email + "'and password='" + password + "'"
        mycursor.execute(q1)
        row = mycursor.fetchone()
        if row is not None:
            print(row[0])
            fn = row[0]
            request.session['name'] = fn
        else:
            print("No result found")
        mycursor.execute("SELECT COUNT(*) FROM parent")
        parent_count = mycursor.fetchone()[0]
        mycursor.execute("SELECT COUNT(*) FROM demoapp_video")
        video_count = mycursor.fetchone()[0]

        q = "select * from teacher where email='" + email + "'and password='" + password + "' and statusofapproval='" + a + "'"
        mycursor.execute(q)
        mycursor.fetchall()
        print(mycursor.rowcount)
        if mycursor.rowcount == 0:
            return render(request, 'DEMOAPP/teacherlogin.html', {'msg': 'Invalid Email-Id and Password'})
        else:
            return render(request, 'DEMOAPP/teacherhome.html', {'name': fn,'parent_count': parent_count,'video_count': video_count})


def plogin(request):
    if request.method == "POST":
        email = request.POST["Email"]
        password = request.POST["Password"]
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
        mycursor = mydb.cursor()
        mycursor1 = mydb.cursor()
        q = "select * from parent where email='" + email + "'and password='" + password + "'"
        mycursor.execute(q)
        mycursor.fetchall()

        if mycursor.rowcount == 0:
            return render(request, 'DEMOAPP/parentlogin.html', {'msg': 'Invalid Email-Id and Password'})
        else:
            query = "select childclass from parent where email = '" + email + "' and password = '" + password + "' "
            mycursor1.execute(query)
            childclass = mycursor1.fetchone()
            query = "select name from parent where email = '" + email + "' and password = '" + password + "' "
            mycursor1.execute(query)
            result = mycursor1.fetchone()
            if result is not None:
                fn = result[0]
                request.session['username'] = email
                request.session['name'] = fn
                request.session['childclass'] = childclass
            else:
                print("No result found")
            mycursor1.execute("SELECT COUNT(*) FROM teacher where statusofapproval='Admitted'")
            teacher_count = mycursor1.fetchone()[0]
            mycursor.execute('SELECT COUNT(*) FROM demoapp_video where classname="' + childclass[0] + '"')
            video_count = mycursor1.fetchone()[0]
            return render(request, 'DEMOAPP/parenthome.html', {'name': fn,'teacher_count':teacher_count,'video_count': video_count})


def alogout(request):
    request.session.flush()
    request.session.flush()

    cache.clear()
    return render(request, 'DEMOAPP/adminlogin.html')


def tlogout(request):
    request.session.flush()
    request.session.flush()

    cache.clear()
    return render(request, 'DEMOAPP/teacherlogin.html')


def plogout(request):
    request.session.flush()
    request.session.flush()
    request.session.flush()
    cache.clear()
    return render(request, 'DEMOAPP/parentlogin.html')


def teacher_list(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select id,name,age,gender,subject,contactno,email,statusofapproval from teacher where statusofapproval='Pending'"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            print('no teachers found')
            return render(request, 'DEMOAPP/teacher_list.html', {'msg': 'No Teachers Found', 'name': fn})
        else:
            return render(request, 'DEMOAPP/teacher_list.html', {'records': records})
    else:
        return render(request, 'DEMOAPP/adminlogin.html')


def teacher_approve(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    mycursor1 = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        id = request.POST["t_id"]
        s = "Admitted"
        s1 = "Denied"

        if request.method == 'POST':
            if request.POST.get("status"):
                query = "update teacher set statusofapproval ='" + s + "' where id =" + id + " "
                query1 = "select name from teacher where id = " + id + " "
                mycursor.execute(query)
                mycursor1.execute(query1)
                tname = mycursor1.fetchone()[0]
                print(tname)
                conn.commit()
                query1 = "select id,name,age,gender,subject,contactno,email,statusofapproval from teacher where statusofapproval='Pending'"
                mycursor.execute(query1)
                records = mycursor.fetchall()
                messages.success(request, "Approved.")
                return render(request, 'DEMOAPP/teacher_list.html',
                              {'records': records, 'msg': tname.upper() + ' Approved ','name': fn})

            elif request.POST.get("status1"):
                query = "update teacher set statusofapproval ='" + s1 + "' where id =" + id + " "
                query1 = "select name from teacher where id = " + id + " "
                mycursor.execute(query)
                mycursor1.execute(query1)
                tname = mycursor1.fetchone()[0]
                conn.commit()
                query1 = "select id,name,age,gender,subject,contactno,email,statusofapproval from teacher where statusofapproval='Pending' "
                mycursor.execute(query1)
                records = mycursor.fetchall()
                messages.error(request, "Denied.")
                return render(request, 'DEMOAPP/teacher_list.html', {'records': records, 'msg': tname.upper() + ' Denied','name': fn})

        return render(request, 'DEMOAPP/teacher_list.html')
    else:
        return render(request, 'DEMOAPP/adminlogin.html')


def teacher_list1(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select id,name,age,gender,subject,contactno,email from teacher where statusofapproval='Admitted'"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            print('no teachers found')
            return render(request, 'DEMOAPP/teacher_list1.html', {'msg': 'No Teachers Found','name': fn})
        else:
            return render(request, 'DEMOAPP/teacher_list1.html', {'records': records,'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html')


def teachers(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        st = "Admitted"
        query = "select id,name,age,gender,subject,contactno,email,statusofapproval from teacher where statusofapproval<>'" + st + "'"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            print('no teachers found')
            return render(request, 'DEMOAPP/teachers.html', {'msg': 'No Teachers Found','name': fn})
        else:
            return render(request, 'DEMOAPP/teachers.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html')


def aparent_list(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select id,name,childname,childage,childdob,childclass,contactno,email from parent"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            print('no parents found')
            return render(request, 'DEMOAPP/aview_parent_list.html', {'msg': 'No Parents Found','name': fn})
        else:
            return render(request, 'DEMOAPP/aview_parent_list.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html')


def aview_vacc_list(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select id,vaccinename,agegroup,doseinterval from vaccination"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            return render(request, 'DEMOAPP/aview_vaccination.html', {'msg': 'No Details Found'})
        else:
            return render(request, 'DEMOAPP/aview_vaccination.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html')


def adel_parent(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        if request.POST.get('delete'):
            id = request.POST["t_id"]
            print(id)
            query = "delete from parent where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            query = "select id,name,childname,childage,childdob,childclass,contactno,email from parent"
            mycursor.execute(query)
            records = mycursor.fetchall()
        return render(request, 'DEMOAPP/aview_parent_list.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html', {'msg': 'Login to Enter'})


def adel_vacc(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        if request.POST.get('delete'):
            id = request.POST["t_id"]
            print(id)
            query = "delete from vaccination where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            query = "select id,vaccinename,agegroup,doseinterval from vaccination"
            mycursor.execute(query)
            records = mycursor.fetchall()
        return render(request, 'DEMOAPP/aview_vaccination.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html', {'msg': 'Login to Enter'})


def adel_teacher(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        if request.POST.get('delete'):
            id = request.POST["t_id"]
            print(id)
            query = "delete from teacher where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            query = "select id,name,age,gender,subject,contactno,email from teacher where statusofapproval='Admitted' "
            mycursor.execute(query)
            records = mycursor.fetchall()
        return render(request, 'DEMOAPP/teacher_list1.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html', {'msg': 'Login to Enter'})


def parent_list(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select id,name,childname,childage,childdob,childclass,contactno,email from parent"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            print('no parents found')
            return render(request, 'DEMOAPP/tview_parent_list.html', {'msg': 'No Parents Found','name': fn})
        else:
            return render(request, 'DEMOAPP/tview_parent_list.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/teacherlogin.html')


def vacc_list(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select vaccinename,agegroup,doseinterval from vaccination"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            return render(request, 'DEMOAPP/tview_vaccination.html', {'msg': 'No Details Found','name': fn})
        else:
            return render(request, 'DEMOAPP/tview_vaccination.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/teacherlogin.html')


def add_vacc(request):
    if 'name' in request.session:
        fn = request.session['name']
        return render(request, 'DEMOAPP/add_vacc.html',{'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html')


def addvacc(request):
    if 'name' in request.session:
        fn = request.session['name']
        if request.method == "POST":
            vacc_name = request.POST["Vacc_name"]
            agegrp = request.POST["Agegrp"]
            doseinv = request.POST["Doseinv"]
            mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
            mycursor = mydb.cursor()
            q = "insert into vaccination(vaccinename,agegroup,doseinterval)values('" + vacc_name + "','" + agegrp + "','" + doseinv + "')"
            mycursor.execute(q)
            mydb.commit()
            return render(request, 'DEMOAPP/add_vacc.html', {'msg': "VACCINE DETAILS ADDED",'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html')

def aview_feedback(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select id,name,email,subject,message,date from afeedback"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            return render(request, 'DEMOAPP/aview_feedback.html', {'msg': 'No Details Found', 'name': fn})
        else:
            return render(request, 'DEMOAPP/aview_feedback.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html')
def pview_teachers(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select id,name,age,gender,subject,contactno,email from teacher where statusofapproval='Admitted'"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            print('no teachers found')
            return render(request, 'DEMOAPP/pview_teachers.html', {'msg': 'No Teachers Found','name': fn})
        else:
            return render(request, 'DEMOAPP/pview_teachers.html', {'records': records,'name': fn})
    else:
        return render(request, 'DEMOAPP/parentlogin.html')


def pview_vacc_list(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select id,vaccinename,agegroup,doseinterval from vaccination"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            return render(request, 'DEMOAPP/pview_vaccination.html', {'msg': 'No Details Found','name': fn})
        else:
            return render(request, 'DEMOAPP/pview_vaccination.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/parentlogin.html')


def psent_feedback(request):
    if 'name' in request.session:
        fn = request.session['name']
        return render(request, 'DEMOAPP/psent_feedback.html', {'name': fn})
    else:
        return render(request, 'DEMOAPP/parentlogin.html', {'msg': 'Login to Continue'})


def psent_feedback1(request):
    if 'name' in request.session:
        fn = request.session['name']
        if request.method == "POST":
            pname = request.POST["pname"]
            feedback = request.POST["feedback"]
            date = request.POST["mydate"]
            mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
            mycursor = mydb.cursor()
            q = "insert into feedback(pname,feedback,date)values('" + pname + "','" + feedback + "','" + date + "')"
            mycursor.execute(q)
            mydb.commit()
            return render(request, 'DEMOAPP/psent_feedback.html', {'msg': 'Feedback sent Successfully', 'name': fn})
    else:
        return render(request, 'DEMOAPP/parentlogin.html', {'msg': 'Login to Continue'})


def pview_feedback(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select * from feedback where pname='" + fn + "'"
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            return render(request, 'DEMOAPP/pview_feedback.html', {'msg': 'No Details Found','name': fn})
        else:
            return render(request, 'DEMOAPP/pview_feedback.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/parentlogin.html')


def pdel_feedback(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        if request.POST.get('delete'):
            id = request.POST["f_id"]
            print(id)
            query = "delete from feedback where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            query = "select id,pname,feedback,date from feedback"
            mycursor.execute(query)
            records = mycursor.fetchall()
        return render(request, 'DEMOAPP/pview_feedback.html', {'records': records, 'name': fn,'msg': 'Feedback Deleted'})
    else:
        return render(request, 'DEMOAPP/parentlogin.html', {'msg': 'Login to Enter'})


def tview_feedback(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select * from feedback "
        mycursor.execute(query)
        records = mycursor.fetchall()
        print(len(records))
        if len(records) == 0:
            return render(request, 'DEMOAPP/tview_feedback.html', {'msg': 'No Details Found','name': fn})
        else:
            return render(request, 'DEMOAPP/tview_feedback.html', {'records': records, 'name': fn})
    else:
        return render(request, 'DEMOAPP/teacherlogin.html')


def tadd_video(request):
    #all_video = Video.objects.filter()
    #"all": all_video
    if 'name' in request.session:
        fn = request.session['name']
        if request.method == "POST":
            form = Video_form(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                form = Video_form()
                return render(request, 'DEMOAPP/teacheradd_video.html',{'msg':'Video Uploaded',"form": form,'name': fn})
            else:
                form = Video_form()
                return render(request, 'DEMOAPP/teacheradd_video.html', {'msg': 'Error occured, Try another File',"form": form,'name': fn})
        else:
            form = Video_form()
            return render(request, 'DEMOAPP/teacheradd_video.html', {"form": form,'name': fn})
    else:
        return render(request, 'DEMOAPP/teacherlogin.html')

def tdel_video(request):
    #all_video = Video.objects.filter()
    #"all": all_video
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        if request.POST.get('delete'):
            id = request.POST["t_id"]
            print(id)
            query = "delete from demoapp_video where id =" + id + " "
            mycursor.execute(query)
            conn.commit()
            cls = request.POST["c_id"]
            sub = request.POST["s_id"]
            all_video = Video.objects.filter(classname=cls, subjname=sub)
            return render(request, 'DEMOAPP/tview_video.html', {"all": all_video, 'name': fn,'msg':"Video Deleted"})
    else:
        return render(request, 'DEMOAPP/teacherlogin.html', {'msg': 'Login to Enter'})


def tview_video(request):
    if 'name' in request.session:
        fn = request.session['name']
        if request.method == "POST":
            cls =request.POST["Classname"]
            sub = request.POST["Subjname"]
            all_video = Video.objects.filter(classname=cls, subjname=sub)
            return render(request, 'DEMOAPP/tview_video.html',{"all": all_video,'name': fn,'cls':cls,'sub':sub})
        else:
            return render(request, 'DEMOAPP/tview_video.html',{'name': fn})
    else:
        return render(request, 'DEMOAPP/teacherlogin.html')

def aview_video(request):
    if 'name' in request.session:
        fn = request.session['name']
        if request.method == "POST":
            cls =request.POST["Classname"]
            sub = request.POST["Subjname"]
            all_video = Video.objects.filter(classname=cls, subjname=sub)
            return render(request, 'DEMOAPP/aview_video.html',{"all": all_video,'name': fn})
        else:
            return render(request, 'DEMOAPP/aview_video.html',{'name': fn})
    else:
        return render(request, 'DEMOAPP/adminlogin.html')
def pview_video(request):
    if 'name' in request.session:
        fn = request.session['name']
        if request.method == "POST":
            cls =request.session['childclass']
            if isinstance(cls, list):
                cls = [c.lower() for c in cls]
                cls = cls[0]
                print(cls)
            else:
                cls = cls.lower()
            sub = request.POST["Subjname"]
            all_video = Video.objects.filter(classname=cls, subjname=sub)
            return render(request, 'DEMOAPP/pview_video.html',{"all": all_video,'name': fn})
        else:
            return render(request, 'DEMOAPP/pview_video.html',{'name': fn})
    else:
        return render(request, 'DEMOAPP/parentlogin.html')

def usent_feedback(request):
    if request.method == "POST":
        name = request.POST["Name"]
        email = request.POST["Email"]
        subject = request.POST["Subject"]
        message= request.POST["Message"]
        date = request.POST["Mydate"]
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
        mycursor = mydb.cursor()
        q = "insert into afeedback(name,email,subject,message,date)values('" + name + "','" + email + "','" + subject + "','" + message + "','" + date + "')"
        mycursor.execute(q)
        mydb.commit()
        return render(request, 'DEMOAPP/contact.html', {'msg': 'Feedback sent Successfully'})

def pedit_profile(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select id,name,childname,childage,childdob,childclass,contactno,email,password from parent where name='" + fn + "'"
        mycursor.execute(query)
        records = mycursor.fetchall()
        return render(request, 'DEMOAPP/pedit_profile.html', {'name': fn, 'records': records})
    else:
        return render(request, 'DEMOAPP/parentlogin.html')
def pedit_profile1(request):
    if 'name' in request.session:
        if request.method == "POST":
            name = request.POST["Name"]
            childname = request.POST["Childname"]
            childage = request.POST["Childage"]
            childdob = request.POST["Childdob"]
            childclass = request.POST["Childclass"]
            contactno = request.POST["Contactno"]
            email = request.POST["Email"]
            password = request.POST["Password"]
            mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
            mycursor = mydb.cursor()
            old_name=request.session['name']
            q = "UPDATE parent SET name = '" + name + "', childname = '" + childname + "', childage = '" + childage + "', childdob = '" + childdob + "', childclass = '" + childclass + "', contactno = '" + contactno + "', email = '" + email + "', password = '" + password + "' WHERE name = '" + old_name + "'"
            mycursor.execute(q)
            mycursor.execute("SELECT COUNT(*) FROM teacher where statusofapproval='Admitted'")
            teacher_count = mycursor.fetchone()[0]
            cls = request.session['childclass']
            if isinstance(cls, list):
                cls = [c.lower() for c in cls]
                cls = cls[0]
                print(cls)
            else:
                cls = cls.lower()
            mycursor.execute('SELECT COUNT(*) FROM demoapp_video where classname="' + cls + '"')
            video_count = mycursor.fetchone()[0]
            request.session['name'] = name
            mydb.commit()
            return render(request, 'DEMOAPP/parenthome.html', {'msg': "PROFILE UPDATED SUCCESSFULLY",'name':name,'teacher_count': teacher_count,'video_count': video_count})
    else:
        return render(request, 'DEMOAPP/parentlogin.html')

def tedit_profile(request):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='kindergarden')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        query = "select id,name,age,gender,subject,contactno,email,password from teacher where statusofapproval='Admitted' and name='" + fn + "'"
        mycursor.execute(query)
        records = mycursor.fetchall()
        return render(request, 'DEMOAPP/tedit_profile.html', {'name': fn, 'records': records})
    else:
        return render(request, 'DEMOAPP/teacherlogin.html')

def tedit_profile1(request):
    if 'name' in request.session:
        if request.method == "POST":
            name = request.POST["Name"]
            age = request.POST["Age"]
            gender = request.POST["Gender"]
            subject = request.POST["Subject"]
            contactno = request.POST["Contactno"]
            email = request.POST["Email"]
            password = request.POST["Password"]
            mydb = mysql.connector.connect(host="localhost", user="root", password="", database="kindergarden")
            mycursor = mydb.cursor()
            old_name=request.session['name']
            q = "UPDATE teacher SET name = '" + name + "', age = '" + age + "', gender = '" + gender + "', subject = '" + subject + "', contactno = '" + contactno + "', email = '" + email + "', password = '" + password + "' WHERE name = '" + old_name + "'"
            mycursor.execute(q)
            mycursor.execute("SELECT COUNT(*) FROM parent")
            parent_count = mycursor.fetchone()[0]
            mycursor.execute("SELECT COUNT(*) FROM demoapp_video")
            video_count = mycursor.fetchone()[0]
            request.session['name'] = name
            mydb.commit()
            return render(request, 'DEMOAPP/teacherhome.html', {'msg': "PROFILE UPDATED SUCCESSFULLY",'name':name,'parent_count': parent_count,'video_count': video_count})
    else:
        return render(request, 'DEMOAPP/teacherlogin.html')

def game1(request):
    return render(request, 'DEMOAPP/game1.html')


def game2(request):
    return render(request, 'DEMOAPP/game2.html')


def game3(request):
    return render(request, 'DEMOAPP/game3.html')
