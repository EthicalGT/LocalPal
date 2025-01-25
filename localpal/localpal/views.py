from django.shortcuts import render
from django.http import HttpResponse
import pymysql
import pymysql.cursors
import shutil
import os

def homepage(req):
    return render(req,'home.html')

def explore(req):
    conn=pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='localpal',
        cursorclass=pymysql.cursors.DictCursor
    )
    data=[]
    try:
        with conn.cursor() as cr:
            cr.execute("select * from local_gems")
            res=cr.fetchall()
            if res:
                for i in res:
                    data.append({
                        'img': i['img'],
                        'lg_name': i['lg_name'],
                        'desc': i['desc'],
                        'address': i['address'],
                        'category': i['category']
                    })
                #print(data)
    except Exception as e:
        print(f"Error -> {e}")
    finally: 
        conn.close()
    return render(req,"explore.html",{'mydata':data})

def feedback(req):
    conn=pymysql.connect(
        host="localhost",
        user="root",
        password=None,
        database="localpal",
        cursorclass=pymysql.cursors.DictCursor
    )
    if req.method=='POST':
        name=req.POST.get('tb1')
        contact=req.POST.get('tb2')
        feedback=req.POST.get('tb3')
        try:
            with conn.cursor() as cr:
                cr.execute("insert into feedback values(%s,%s,%s,%s)",(name,contact,feedback,None))
                conn.commit()
                return HttpResponse("<html><body><script>alert('Feedback Successful.'); window.location='feedback';</script></body></html>")
        except Exception as e:
            print(f"Error -> {e}")
        finally:
            conn.close()
    return render(req,"feedback.html")

def adminlogin(req):
    conn=pymysql.connect(
        host="localhost",
        user="root",
        password=None,
        database="localpal",
        cursorclass=pymysql.cursors.DictCursor
    )
    if req.method=='POST':
        adminname=req.POST.get('tb1')
        pwd=req.POST.get('tb2')
        try:
            with conn.cursor() as cr:
                cr.execute("select * from admin where adminname=%s and password=%s",(adminname,pwd))
                res=cr.fetchone()
                if res:
                    return HttpResponse("<html><body><script>window.location='admindashboard';</script></body></html>")
                else:
                    return HttpResponse("<html><body><script>alert('Inavlid Credentials!'); window.location='adminlogin';</script></body></html>")
        except Exception as e:
            print(f"Error -> {e}")
        finally:
            conn.close()
    return render(req,"adminlogin.html")

def admindashboard(req):
    return render(req,"admindashboard.html")

def addlocalgems(req):
    conn=pymysql.connect(
        host="localhost",
        user="root",
        password=None,
        database="localpal",
        cursorclass=pymysql.cursors.DictCursor
    )
    if req.method=='POST':
        lgname=req.POST.get('tb1')
        file=req.FILES['myfile']
        desc=req.POST.get('tb3')
        addr=req.POST.get('tb4')
        category=req.POST.get('tb5')
        dest="E:/localpal/static/img/"
        destpath=os.path.join(dest,file.name)
        dbimgpath=destpath[19:]
        try:
            with conn.cursor() as cr:
                cr.execute("insert into local_gems values(%s,%s,%s,%s,%s)",(dbimgpath,lgname,desc,addr,category))
                with open(destpath,'wb') as f:
                    shutil.copyfileobj(file,f)
                conn.commit()
                return HttpResponse("<html><body><script>alert('Local Gem Added Successfully.'); window.location='addlocalgems';</script></body></html>")
        except Exception as e:
            print(f"Error->{e}")
        finally:
            conn.close()
    return render(req,"addlocalgems.html")

def deletelocalgems(req):
    conn=pymysql.connect(
        host="localhost",
        user="root",
        password=None,
        database="localpal",
        cursorclass=pymysql.cursors.DictCursor
    )
    if req.method=='POST':
        lgname=req.POST.get('tb1')
        try:
            with conn.cursor() as cr:
                cr.execute("delete from local_gems where lg_name=%s",(lgname,))
                conn.commit()
                return HttpResponse("<html><body><script>alert('Local Gem Deleted Successfully.'); window.location='deletelocalgems';</script></body></html>")
        except Exception as e:
            print(f"Error->{e}")
        finally:
            conn.close()    
    return render(req,"deletelocalgems.html")

def feedbackinfo(req):
    conn=pymysql.connect(
        host="localhost",
        user="root",
        password=None,
        database="localpal",
        cursorclass=pymysql.cursors.DictCursor
    )
    feedbackdata=[]
    try:
        with conn.cursor() as cr:
            cr.execute("select * from feedback")
            rs=cr.fetchall()
            if rs:
                for data in rs:
                    feedbackdata.append({
                        'name': data['name'],
                        'contact': data['contact'],
                        'suggestion': data['suggestion'],
                        'datetime': data['datetime']
                    })
    except Exception as e:
        print(f"Error -> {e}")
    finally:
        conn.close()        
    return render(req,"feedbackinfo.html",{'fdata': feedbackdata})