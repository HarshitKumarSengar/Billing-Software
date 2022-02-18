import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector
import random
class inventroy:
    def __init__(self,win):
        def sql(q):
            conn = mysql.connector.connect(host='localhost',username = 'root',password = 'mysql',database = 'hyper_mart')
            cu = conn.cursor()
            cu.execute(q)
            a = cu.fetchall()
            conn.commit()
            conn.close()
            return a
        win = win
        hight_value = win.winfo_screenwidth()
        width_value = win.winfo_screenheight()
        win.geometry(f"{hight_value}x{width_value}+0+0")
        win.state('zoomed')
        win.attributes('-fullscreen',True)
        load = Image.open(r"images\inventory_win.jpg")
        self.bg_image = ImageTk.PhotoImage(load)
        self.back_label = ttk.Label(win,image=self.bg_image)
        self.back_label.place(x=-2,y=-2)
       
        conpro = ""
        def a(event=None):
            pass
                    ###########################  tree view ####################### 
        table_frame = ttk.Frame(win)
        table_frame.place(x=435,y=130,height = 600,width = 875)
        trv = ttk.Treeview(table_frame,columns=(1,2,3,4,5,6,7,8,9,10),show="headings",)

        def adder(a):
            l =['grocery','cosmetics',   'house_hold_items', 'electronics', 'men_clothing','women_clothing','kids_clothing',  'toys_and_games']
            trv.tag_configure('near_out', background="orange")
            trv.tag_configure('out', background="red")
            trv.delete(*trv.get_children())
            for i in range(0,8):
                q = a.replace('@',l[i]) 
                query = q
                cu = sql(q)
                for j in cu:
                    if j==():
                        break
                    else:
                        if 0<j[6]<10:
                            trv.insert('','end',values=j,tags='near_out')
                        elif j[6]==0:
                            trv.insert('','end',values=j,tags='out')
                        else:
                            trv.insert('','end',values=j)

        def update(event=None):
            adder("SELECT * FROM @")

        yscrlbar = ttk.Scrollbar(table_frame,orient ="vertical",command = trv.yview)
        yscrlbar.pack(side =RIGHT, fill ='y') 

        yerscrlbar = ttk.Scrollbar(table_frame,orient ="horizontal",command = trv.xview)
        yerscrlbar.pack(side =BOTTOM, fill ='x') 
        trv.configure(xscrollcommand=  yerscrlbar.set,yscrollcommand = yscrlbar.set)
        trv.pack(fill = 'both',expand = True)
        cu = sql("DESCRIBE cosmetics")
        w = [100,100,100,100,100,100,100,100,100,100]
        y = 1
        for i in cu:
            v = i[0]
            trv.column(y, stretch=NO, width=w[y-1])
            trv.heading(y,text=v)
            y +=1
        update()
        # trv.heading(1, text="Customer ID"
        style = ttk.Style()
        style.theme_use(None)
        style.map('Treeview', 
	    background=[('selected', '#0078d7')])
        #### func ######
        def undoear(event = None):
            update()
            self.sear_button.configure(command=sear)
        def sear(event=None):
            z = prosearch.get()
            if z == "":
                pass
            else:
                a = f"SELECT * FROM @ WHERE id = {z}"
                adder(a)
                self.sear_button.configure(command=undoear)
        def proupdate(event=None):
            global conpro
            conpro = 'u'
            item = trv.item(trv.focus())
            conpro+=str(item['values'][0])
            v1.set(item['values'][1])
            v2.set(item['values'][7])
            v3.set(item['values'][2])
            v4.set(item['values'][3])
            v5.set(item['values'][4])
            v6.set(item['values'][5])
            v7.set(item['values'][6])
            v8.set(item['values'][8])
            v9.set(item['values'][9])
            pro_frame.place(x=205,y=160,height = 540,width = 952)
        def prof(event = None):
            global conpro
            pro_frame.place(x=205,y=160,height = 540,width = 952)
            v1.set('')
            v2.set('')
            v3.set('')
            v6.set('')
            v7.set('')
            v8.set('')
            v9.set('')
            conpro = 'a'

        def subbmit(event = None):
            global conpro
            id = idgen()
            n = v1.get()
            q = v2.get()
            b=  v3.get()
            c = v4.get()
            sc = v5.get()
            cp  =v6.get()
            sp = v7.get()
            w = v8.get()
            vp = v9.get()
            if conpro == 'a':
                conpro=''
                query = f"INSERT INTO {c} VALUE ({id},'{n}',{b},'{c}','{sc}',{cp},{sp},{q},{w},{vp})"
                sql(query)
            else:
                id = conpro[1:]
                query = f"UPDATE {c} SET name = '{n}',bar_code = {b},category = '{c}',sub_category = '{sc}',cost_price = {cp},selling_price={sp},stock = {q},weight = {w},vendor_no = {vp} WHERE id ={id}"
                sql(query)
                conpro = ''
            update()
            pro_frame.place_forget()

        catl = ['grocery','cosmetics','house_hold_items','electronics', 'men_clothing','women_clothing','kids_clothing','toys_and_games']
        def idgen():
            id = ''
            c = v4.get()
            ind = str(catl.index(c)+1)
            id+=ind
            with open (r"data\subcar.txt",'r') as f:
                d = f.readlines()
                for i in d:
                    if c in i:
                        a = i.split(' ')
                        a.remove(c)
                        if '@' in a:
                            a.remove('@')
                        else:
                            a.remove("@\n")
                        in1 = a.index(v5.get())+1
                        id+= '0'+str(in1)
            il = []
            cu = sql(f"SELECT id FROM {c}")
            for i in cu:
                il.append(i[0])
            if il==[]:
                a = 100001
            else:
                a = max(il) +1
            si = str(a)
            id+=si[3:6]                  
            return int(id)
        def prodelete(event = None):
            item = trv.item(trv.focus())
            if item['values'] == '':
                pass
            else:
                id = item['values'][0]
                a = int(str(id)[0]) - 1
                sql(f"DELETE FROM {catl[a]} WHERE id = {id}")
                update()

        def combovalue(event = None):
            with open (r"data\subcar.txt",'r') as f:
                d = f.readlines()
                for i in d:
                    if (v4.get()) in i:
                        a = i.split(' ')
                        a.remove(v4.get())
                        if '@' in a:
                            a.remove('@')
                        else:
                            a.remove("@\n")
                        self.subcate['values'] = tuple(a)
                        self.subcate.current(0)

        def comboplus(event = None):
            if ps.get() == '':
                self.plus_entry.place(x=660,y=250,width = 190)      
            else:
                d = []
                with open (r"data\subcar.txt",'r') as f:
                    d = f.readlines()
                a = 0
                pluv = ps.get()
                for i in d:
                    if (v4.get()) in i:
                        j = i.replace('@',f"{pluv} @")
                        d[a] = j
                    a+=1
                with open (r"data\subcar.txt",'w') as f:
                    f.writelines(d)
                ps.set('')
                self.plus_entry.place_forget()
                combovalue()
             ######################### buttons #################
        prosearch = tk.Entry(win, bd=0, bg="white", fg="black", font=("arial",15))
        prosearch.place(x=60,y=240)

        load = Image.open(r"images\insear.jpg")
        self.sear_image = ImageTk.PhotoImage(load)
        self.sear_button = tk.Button(win,image = self.sear_image,command = sear,border = 0)
        self.sear_button.place(x = 220,y=220)

        load = Image.open(r"images\update.jpg")
        self.update_image = ImageTk.PhotoImage(load)
        self.update_button = tk.Button(win,image = self.update_image,command = proupdate,border = 0)
        self.update_button.place(x = 70,y=380)
        trv.bind('<Double 1>',proupdate)

        load = Image.open(r"images\add.jpg")
        self.add_image = ImageTk.PhotoImage(load)
        self.add_button = tk.Button(win,image = self.add_image,command = prof,border = 0)
        self.add_button.place(x = 70,y=500)

        load = Image.open(r"images\delete.jpg")
        self.delete_image = ImageTk.PhotoImage(load)
        self.delete_button = tk.Button(win,image = self.delete_image,command = prodelete,border = 0)
        self.delete_button.place(x = 70,y=625)

        pro_frame = ttk.Frame(win)

        load = Image.open(r"images\add_pro.jpg")
        self.bg_image1 = ImageTk.PhotoImage(load)
        self.back_label1 = ttk.Label(pro_frame,image=self.bg_image1)
        self.back_label1.place(x=-2,y=-2)

        v1 = tk.StringVar()
        v2 = tk.StringVar()
        v3 = tk.StringVar()
        v4 = tk.StringVar()
        v5 = tk.StringVar()
        v6 = tk.StringVar()
        v7 = tk.StringVar()
        v8= tk.StringVar()
        v9 = tk.StringVar()


        self.pro_name= tk.Entry(pro_frame, textvariable = v1,bd=0, bg="white", fg="black", font=("arial",15))
        self.pro_name.place(x=65,y=110,width = 550)

        self.qty= tk.Entry(pro_frame, textvariable = v2, bd=0, bg="white", fg="black", font=("arial",15))
        self.qty.place(x=200,y=185,width = 190)

        self.bcode= tk.Entry(pro_frame, textvariable = v3, bd=0, bg="white", fg="black", font=("arial",15))
        self.bcode.place(x=660,y=185,width = 190)

        self.cate= ttk.Combobox(pro_frame, textvariable = v4, state='readonly')
        self.cate['values'] = tuple(catl)
        self.cate.current(0)
        self.cate.place(x=200,y=250,width = 190)

        # self.subcate= tk.Entry(pro_frame, textvariable = v5, bd=0, bg="white", fg="black", font=("arial",15))
        # self.subcate.place(x=660,y=250,width = 190)
            
        self.subcate= ttk.Combobox(pro_frame, textvariable = v5, state='readonly')
        self.subcate.place(x=660,y=250,width = 190)
        combovalue()
        self.cate.bind("<<ComboboxSelected>>", combovalue)

        load = Image.open(r"images\plus.jpg")
        self.plus_image = ImageTk.PhotoImage(load)
        self.plus_button = tk.Button(pro_frame,image = self.plus_image,command = comboplus,border = 0)
        self.plus_button.place(x =850 ,y=250)
        ps = tk.StringVar()
        self.plus_entry= tk.Entry(pro_frame, textvariable = ps, bd=0, bg="white", fg="black", font=("arial",13))
        # self.plus_entry.place(x=660,y=250,width = 190)

        self.cprice= tk.Entry(pro_frame, textvariable = v6, bd=0, bg="white", fg="black", font=("arial",15))
        self.cprice.place(x=200,y=317,width = 190)

        self.sprice= tk.Entry(pro_frame, textvariable = v7, bd=0, bg="white", fg="black", font=("arial",15))
        self.sprice.place(x=200,y=384,width = 190)

        self.weight= tk.Entry(pro_frame, textvariable = v8, bd=0, bg="white", fg="black", font=("arial",15))
        self.weight.place(x=660,y=317,width = 190)

        self.v_phone= tk.Entry(pro_frame, textvariable = v9, bd=0, bg="white", fg="black", font=("arial",15))
        self.v_phone.place(x=660,y=384,width = 190)

        load = Image.open(r"images\submit.jpg")
        self.submit_image = ImageTk.PhotoImage(load)
        self.submit_button = tk.Button(pro_frame,image = self.submit_image,command = subbmit,border = 0)
        self.submit_button.place(x =420 ,y=450)

        def back(event = None):
            win.destroy()
            adminstraion = tk.Tk()
            adminstraion.iconbitmap(r"images\logo.ico")
            obj = control(adminstraion)
            adminstraion.mainloop()

        load1 = Image.open(r"images\backbutton.jpg")
        self.bacck_image = ImageTk.PhotoImage(load1)
        self.bacck_button = tk.Button(win,image = self.bacck_image,command = back,border = 0)
        self.bacck_button.place(x =30 ,y=30,height = 38,width = 138)
        
class emploeye:
    def __init__(self,win):

        win = win
        hight_value = win.winfo_screenwidth()
        width_value = win.winfo_screenheight()
        win.geometry(f"{hight_value}x{width_value}+0+0")
        win.state('zoomed')
        win.attributes('-fullscreen',True)
        load = Image.open(r"images\employee_win.jpg")
        self.bg_image = ImageTk.PhotoImage(load)
        self.back_label = ttk.Label(win,image=self.bg_image)
        self.back_label.place(x=-2,y=-2)
        conemp = ""
        def sql(q):
            conn = mysql.connector.connect(host='localhost',username = 'root',password = 'mysql',database = 'hyper_mart')
            cu = conn.cursor()
            cu.execute(q)
            a = cu.fetchall()
            conn.commit()
            conn.close()
            return a

        def adder(q):
            trv.delete(*trv.get_children())
            cu = sql(q)
            for j in cu:
                if j==():
                    break
                else:    
                    trv.insert('','end',values=j)
        def update(event = None):
            adder("SELECT * FROM employee")
        table_frame = ttk.Frame(win)
        table_frame.place(x=435,y=130,height = 600,width = 875)
        trv = ttk.Treeview(table_frame,columns=(1,2,3,4,5,6,7,8,9),show="headings",)

        yscrlbar = ttk.Scrollbar(table_frame,orient ="vertical",command = trv.yview)
        yscrlbar.pack(side =RIGHT, fill ='y') 

        yerscrlbar = ttk.Scrollbar(table_frame,orient ="horizontal",command = trv.xview)
        yerscrlbar.pack(side =BOTTOM, fill ='x') 
        trv.configure(xscrollcommand=  yerscrlbar.set,yscrollcommand = yscrlbar.set)

        trv.pack(fill = 'both',expand = True)

        cu = sql("DESCRIBE employee")
        w = [100,200,100,100,100,100,100,100,100,100]
        y = 1
        for i in cu:
            v = i[0]
            trv.column(y, stretch=NO, width=w[y-1])
            trv.heading(y,text=v)
            y +=1
        update()

        ################ func ######################
        def undoear(event = None):
            update()
            self.sear_button.configure(command=sear)
        def sear(event=None):
            z = prosearch.get()
            if z == "":
                pass
            else:
                a = f"SELECT * FROM employee WHERE id = {z}"
                adder(a)
                self.sear_button.configure(command=undoear)

        def idgen(d,w,c):
            id = ''
            with open(r"data\work.txt","r") as f:
                data=  f.readlines()
                a = 1 
                for i in data:
                    if w in i:
                        break
                    a +=1                    
            id += d[0:2]
            id += str(a)
            id += c[-4:]
            return int(id)
        def empdelete(event = None):
            item = trv.item(trv.focus())
            if item['values'] == '':
                pass
            else:
                id = item['values'][0]
                sql(f"DELETE FROM employee WHERE id={id}")
                update()

        def empupdate(event=None):
            global conpro
            conpro = ''
            item = trv.item(trv.focus())
            conpro+=str(item['values'][0])
            v1.set(item['values'][1])
            v2.set(item['values'][2])
            v3.set(item['values'][3])
            v4.set(item['values'][4])
            v5.set(item['values'][7])
            v6.set(item['values'][6])
            emp_frame.place(x=205,y=160,height = 540,width = 952)

        def empadd(event = None):
            global conpro
            emp_frame.place(x=205,y=160,height = 540,width = 952)
            v1.set('')
            v2.set('')
            v3.set('')
            v4.set('')
            v5.set('')
            v6.set('')
            conpro = 'a'

        def subbmit(event = None):
            global conpro
            n = v1.get()
            c = v2.get()
            d=  v3.get()
            a = v4.get()
            w = v5.get()

            with open(r"data\work.txt",'r+') as f:
                ad= f.readlines()
                cbollean = True
                for i in ad:
                    if w in i:
                        cbollean = False
                if cbollean:
                    f.write(f"\n{w.lower()}")
            s  =v6.get()
            id = idgen(d,w,c)
            p = f"{n[0:2]}@{d[0:2]}{c[-4:]}"
            if conpro == 'a':
                conpro=''
                query = f"INSERT INTO employee VALUE ({id},'{n}','{c}','{d}','{a}',0,{s},'{w}','{p}')"
                sql(query)
            else:
                query = f"UPDATE employee SET NAME = '{n}',CONTACT = '{c}',DOB = '{d}',AADAHAR_NO = '{a}' , SALARY = {s},WORK = '{w}' WHERE ID = {conpro}"
                sql(query)
            update()
            emp_frame.place_forget()
                
        
        ######################### button ####################

        prosearch = tk.Entry(win, bd=0, bg="white", fg="black", font=("arial",15))
        prosearch.place(x=60,y=240)
        
        load = Image.open(r"images\insear.jpg")
        self.sear_image = ImageTk.PhotoImage(load)
        self.sear_button = tk.Button(win,image = self.sear_image,command = sear,border = 0)
        self.sear_button.place(x = 220,y=220)

        load = Image.open(r"images\update.jpg")
        self.update_image = ImageTk.PhotoImage(load)
        self.update_button = tk.Button(win,image = self.update_image,command = empupdate,border = 0)
        self.update_button.place(x = 70,y=380)
        trv.bind('<Double 1>',empupdate)

        load = Image.open(r"images\add.jpg")
        self.add_image = ImageTk.PhotoImage(load)
        self.add_button = tk.Button(win,image = self.add_image,command = empadd,border = 0)
        self.add_button.place(x = 70,y=500)

        load = Image.open(r"images\delete.jpg")
        self.delete_image = ImageTk.PhotoImage(load)
        self.delete_button = tk.Button(win,image = self.delete_image,command = empdelete,border = 0)
        self.delete_button.place(x = 70,y=625)

        ############### emp frame #################
        emp_frame = ttk.Frame(win)

        load = Image.open(r"images\emp_up.jpg")
        self.bg_image1 = ImageTk.PhotoImage(load)
        self.back_label1 = ttk.Label(emp_frame,image=self.bg_image1)
        self.back_label1.place(x=-2,y=-2)

        v1 = tk.StringVar()
        v2 = tk.StringVar()
        v3 = tk.StringVar()
        v4 = tk.StringVar()
        v5 = tk.StringVar()
        v6 = tk.StringVar()

        self.emp_name= tk.Entry(emp_frame, textvariable = v1,bd=0, bg="white", fg="black", font=("arial",15))
        self.emp_name.place(x=65,y=135,width = 550)

        self.contact= tk.Entry(emp_frame, textvariable = v2,bd=0, bg="white", fg="black", font=("arial",15))
        self.contact.place(x=205,y=220,width = 200)

        self.dob= tk.Entry(emp_frame, textvariable = v3,bd=0, bg="white", fg="black", font=("arial",15))
        self.dob.place(x=690,y=224,width = 200)

        self.aadhar= tk.Entry(emp_frame, textvariable = v4,bd=0, bg="white", fg="black", font=("arial",15))
        self.aadhar.place(x=205,y=285,width = 200)
        
        self.work= tk.Entry(emp_frame, textvariable = v5,bd=0, bg="white", fg="black", font=("arial",15))
        self.work.place(x=690,y=285,width = 200)


        self.salry= tk.Entry(emp_frame, textvariable = v6,bd=0, bg="white", fg="black", font=("arial",15))
        self.salry.place(x=205,y=355,width = 200)

        load = Image.open(r"images\submit.jpg")
        self.submit_image = ImageTk.PhotoImage(load)
        self.submit_button = tk.Button(emp_frame,image = self.submit_image,command = subbmit,border = 0)
        self.submit_button.place(x =420 ,y=450)
        def back(event = None):
            win.destroy()
            adminstraion = tk.Tk()
            adminstraion.iconbitmap(r"images\logo.ico")
            obj = control(adminstraion)
            adminstraion.mainloop()

        load1 = Image.open(r"images\backbutton.jpg")
        self.bacck_image = ImageTk.PhotoImage(load1)
        self.bacck_button = tk.Button(win,image = self.bacck_image,command = back,border = 0)
        self.bacck_button.place(x =30 ,y=30,height = 38,width = 138)
class deveelopeer:
    def __init__(self,win):

        win = win
        hight_value = win.winfo_screenwidth()
        width_value = win.winfo_screenheight()
        win.geometry(f"{hight_value}x{width_value}+0+0")
        win.state('zoomed')
        win.attributes('-fullscreen',True)
class control:
    def __init__(self,win):

        win = win
        hight_value = win.winfo_screenwidth()
        width_value = win.winfo_screenheight()
        win.geometry(f"{hight_value}x{width_value}+0+0")
        win.state('zoomed')
        win.attributes('-fullscreen',True)
        load = Image.open(r"images\ad_bac.jpg")
        self.bg_image = ImageTk.PhotoImage(load)
        self.back_label = ttk.Label(win,image=self.bg_image)
        self.back_label.place(x=-2,y=-2)
        with open(r"data\status.txt",'w') as f:
            f.write("")
        def invent(event=None):
            win.destroy()
            root = tk.Tk()
            root.iconbitmap(r"images\logo.ico")
            obj = inventroy(root)
            root.mainloop()
        def emp(event=None):
            win.destroy()
            root = tk.Tk()
            root.iconbitmap(r"images\logo.ico")
            obj = emploeye(root)
            root.mainloop()
            
        def devo(event=None):
            win.destroy()
            root = tk.Tk()
            root.iconbitmap(r"images\logo.ico")
            obj = deveelopeer(root)
            root.mainloop()


        load = Image.open(r"images\inventory.jpg")
        self.invent_image1 = ImageTk.PhotoImage(load)
        self.invent_b = tk.Button(win,image = self.invent_image1,command = invent,border = 0)
        self.invent_b.place(x = 240,y=365)

        load = Image.open(r"images\emp.jpg")
        self.emp_image2 = ImageTk.PhotoImage(load)
        self.emp_b = tk.Button(win,image = self.emp_image2,command = emp,border = 0)
        self.emp_b.place(x = 980,y=365)

        load = Image.open(r"images\devo.jpg")
        self.devo_image = ImageTk.PhotoImage(load)
        self.devo_b = tk.Button(win,image = self.devo_image,command = devo,border = 0)
        self.devo_b.place(x = 610,y=170)

class billing:
    def __init__(self,win):
        win = win
        hight_value = win.winfo_screenwidth()
        width_value = win.winfo_screenheight()
        win.geometry(f"{hight_value}x{width_value}+0+0")
        win.state('zoomed')
        win.attributes('-fullscreen',True)

        load = Image.open(r"images\main.jpg")
        self.bg_image = ImageTk.PhotoImage(load)
        self.back_label = ttk.Label(win,image=self.bg_image)
        self.back_label.place(x=-2,y=-2)

        def sql(q):
            conn = mysql.connector.connect(host='localhost',username = 'root',password = 'mysql',database = 'hyper_mart')
            cu = conn.cursor()
            cu.execute(q)
            a = cu.fetchall()
            conn.commit()
            conn.close()
            return a

        cat = tk.StringVar()
        subcat = tk.StringVar()
        product = tk.StringVar()
        qty = tk.StringVar()
        custom_name = tk.StringVar()
        phone_no = tk.StringVar()
        bill_no = tk.StringVar()

        probill = []
        cart = []

        catl = ['grocery','cosmetics',   'house_hold_items', 'electronics', 'men_clothing','women_clothing','kids_clothing',  'toys_and_games']

        self.table_frame = tk.Frame(win,bg = "White")
        self.table_frame.place(x = 78,y = 245,width = 770,height = 360)
        text_editor = tk.Text(self.table_frame,font=('consolas', 11, 'normal'))
        text_editor.config(wrap='word', relief=tk.FLAT)

        scroll_bar = tk.Scrollbar(self.table_frame)
        text_editor.focus_set()
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        text_editor.pack(fill=tk.BOTH, expand=True)
        scroll_bar.config(command=text_editor.yview)
        text_editor.config(yscrollcommand=scroll_bar.set)
        text_editor.config(state = 'disabled')

        s = " "
        b = '_'
        def default_view(event = None):
            text_editor.config(state = 'normal')
            text_editor.delete('1.0',tk.END)
            text_editor.insert(END,f"{s*41}HYPER MART{s*41}\n{s*38}Rohini New Delhi{s*38}\n{s*43}110089{s*43}\n{s*35}Phone N0. : 011-123456{s*35}\nCustomer Name:{custom_name.get()}{s*(50-len(custom_name.get()))}Phone Number:+91{phone_no.get()}\n{b*92}\n\nProduct{s*20}Unit Price{s*10}Qty{s*11}tax(18%){s*8}Total Price\n{b*93}\n")
            text_editor.config(state = 'disabled')
        default_view()

        def billwriter(pn,p,q,t,tp):
            text_editor.config(state = 'normal')
            text_editor.insert(END,f"{pn}{s*(27-len(pn))}{p}{s*(20-len(str(p)))}{q}{s*(14-len(str(q)))}{t}{s*(16-len(str(t)))}{tp}\n")
            text_editor.config(state = 'disabled')
        def cartwriter():
            default_view()
            for i in cart:
                billwriter(i['name'],i['price'],i['qty'],i['tax'],i['total_price'])

        def combovalue(event = None):
            with open (r"data\subcar.txt",'r') as f:
                d = f.readlines()
                for i in d:
                    if (cat.get()) in i:
                        a = i.split(' ')
                        a.remove(cat.get())
                        if '@' in a:
                            a.remove('@')
                        else:
                            a.remove("@\n")
                        self.subcat['values'] = tuple(a)
                        self.subcat.current(0)
        def category(event = None):
            combovalue()
            provalue()
        def provalue(event = None):
            l = []
            c = cat.get()
            s = subcat.get()
            a = sql(f"SELECT * FROM {c} WHERE sub_category = '{s}'")
            probill.clear()
            for i in a:
                probill.append({'id':i[0],'name':i[1],'selling_price':i[6],'stock':i[7]})
                l.append(i[1])
            self.probox['values'] = tuple(l)
            if l!=[]:
                self.probox.current(0)

        def exit(event = None):

            win.destroy()

        def cartadder(event = None):
            p = product.get()
            c = cat.get()
            s=  subcat.get()
            q = qty.get()
            if probill!=[]:
                for i in probill:
                    if i['name'] == p:
                        sql(f"UPDATE {c} SET stock = stock-{q} WHERE id = {i['id']}")
                        t = round(int(i['selling_price'])*0.18)
                        tp = round((i['selling_price']+t)*int(q)) 
                        cart.append({'id':i['id'],'name':p,'price':i['selling_price'],'qty':q,'tax':t,'total_price':tp})
                        cartwriter()
                        break
        def remover(event = None):
            p = product.get()
            if cart!=[]:
                for i in cart:
                    if i['name'] == p:
                        cart.remove(i)
                        cartwriter()
                        break
        def billclear(event = None):
            custom_name.set('')
            phone_no.set('')
            default_view()
            cart.clear()

        def totalbill(event=  None):
            x = random.randint(10000,99999)
            bill_no.set(str(x))
            total = 0
            if cart!=[]:
                for i in cart:
                    total +=  int(i['total_price'])
            text_editor.config(state = 'normal')
            text_editor.insert(END,f"{b*92}\n\nTotal Amount To Be Paid:{total}\n")
            text_editor.config(state = 'disabled')
            data = text_editor.get("1.0",END)
            with open(f"bills/{str(x)}.txt","w") as f:
                f.write(data) 


        self.name= tk.Entry(win,textvariable = custom_name, bd=0, bg="white", fg="black", font=("arial",15))
        self.name.place(x=235,y=152)

        self.phone_no= tk.Entry(win,textvariable = phone_no, bd=0, bg="white", fg="black", font=("arial",15))
        self.phone_no.place(x=605,y=152)

        load = Image.open(r"images\total.jpg")
        self.total_image = ImageTk.PhotoImage(load)
        self.total_button = tk.Button(win,image = self.total_image,command = totalbill,bd = 0)
        self.total_button.place(x = 90,y=652)

        load = Image.open(r"images\gen.jpg")
        self.gen_image = ImageTk.PhotoImage(load)
        self.genrate_button = tk.Button(win,image = self.gen_image,command = default_view,bd = 0)
        self.genrate_button.place(x = 280,y=652)

        load = Image.open(r"images\clear.jpg")
        self.clear_image = ImageTk.PhotoImage(load)
        self.clear_button = tk.Button(win,image = self.clear_image,command = billclear,bd = 0)
        self.clear_button.place(x = 470,y=652)

        load = Image.open(r"images\exit.jpg") 
        self.exit = ImageTk.PhotoImage(load)
        self.exit_button = tk.Button(win,image = self.exit,command = exit,bd = 0)
        self.exit_button.place(x = 660,y=652)

        load = Image.open(r"images\addcart.jpg") 
        self.addpro = ImageTk.PhotoImage(load)
        self.addpro_button = tk.Button(win,image = self.addpro,command = cartadder,bd = 0)
        self.addpro_button.place(x = 915,y=650)

        load = Image.open(r"images\remove.jpg") 
        self.remove = ImageTk.PhotoImage(load)
        self.remove_button = tk.Button(win,image = self.remove,command = remover,bd = 0)
        self.remove_button.place(x = 1100,y=650)

        self.cat= ttk.Combobox(win, textvariable = cat, state='readonly',font =('arial', 15, 'normal') )
        self.cat['values'] = tuple(catl)
        self.cat.current(0)
        self.cat.place(x=900,y=300,width = 370)

        self.subcat= ttk.Combobox(win,textvariable = subcat, state='readonly',font =('arial', 15, 'normal'))
        self.subcat.place(x=900,y=385,width = 370)
        
        self.probox= ttk.Combobox(win,textvariable = product, state='readonly',font =('arial', 15, 'normal'))
        self.probox.place(x=900,y=470,width = 370)
        combovalue()
        provalue()        
        self.cat.bind("<<ComboboxSelected>>", category)
        self.subcat.bind("<<ComboboxSelected>>", provalue)

        self.qty_value= tk.Entry(win,textvariable = qty, bg="white", fg="black", font=("arial",15))
        self.qty_value.place(x=900,y=560,width = 370)

class login_style:
    def __init__(self,login_page):
        with open(r"data\status.txt",'w') as f:
            pass
        self.login_page = login_page
        hight_value = self.login_page.winfo_screenwidth()
        width_value = self.login_page.winfo_screenheight()
        self.login_page.geometry(f"{hight_value}x{width_value}+0+0")
        self.login_page.state('zoomed')
        self.login_page.attributes('-fullscreen',True)
        load = Image.open(r"images\login_back.jpg")

        self.bg_image = ImageTk.PhotoImage(load)
        self.back_label = ttk.Label(login_page,image=self.bg_image)
        self.back_label.place(x=-2,y=-2)

        def employee_login(event = None):
            with open(r"data\status.txt",'w') as f:
                f.write("employee")
            self.login_page.destroy()

        def admin_login(event = None):
            with open(r"data\status.txt",'w') as f:
                f.write("admin")
            self.login_page.destroy()

        load = Image.open(r"images\ee_login.jpg")
        self.e_image = ImageTk.PhotoImage(load)
        self.e_button = tk.Button(login_page,image = self.e_image,command = employee_login,border = 0)
        self.e_button.place(x = 278.75,y=288)

        load = Image.open(r"images\a_login.jpg")
        self.admin_image = ImageTk.PhotoImage(load)
        self.admin_button = tk.Button(login_page,image = self.admin_image,command = admin_login,border = 0)
        self.admin_button.place(x = 868.75,y=288)

class input_style:
    def __init__(self,win):
        win = win
        hight_value = win.winfo_screenwidth()
        width_value = win.winfo_screenheight()
        win.geometry(f"{hight_value}x{width_value}+0+0")
        win.state('zoomed')
        load = Image.open(r"images\back.jpg")

        def sql(q):
            conn = mysql.connector.connect(host='localhost',username = 'root',password = 'mysql',database = 'hyper_mart')
            cu = conn.cursor()
            cu.execute(q)
            a = cu.fetchall()
            conn.commit()
            conn.close()
            return a

        self.bg_image = ImageTk.PhotoImage(load)
        self.back_label = ttk.Label(win,image=self.bg_image)
        self.back_label.place(x=-2,y=-2)
        win.attributes('-fullscreen',True)
        username = tk.Entry(win, bd=0, bg="white", fg="black", font=("arial",20))
        username.place(x=525,y=240)
        username.focus_set()

        password= tk.Entry(win, bd=0,show="*", bg="white", fg="black", font=("arial",20))
        password.place(x=525,y=398)
        password.focus_set()

        login_error = tk.Label(win,text = "",fg = 'red',bg = 'white',font = ('arial',10),bd = 0)
        login_error.place(x=580,y=450)
        def writer():
            with open(r"data\status.txt",'r') as f:
                d = f.readline()
            with open(r"data\status.txt",'w') as f:
                if 'employee' in d:
                    f.write("pass\nemployee")
                else:
                    f.write("pass\nadmin")
        def l_func(event = None):
            u = username.get()
            p = password.get()
            if u == '':
                login_error.configure(text = "** Please Enter Username **")
            if p == '':
                login_error.configure(text = "** Please Enter password **")
            else:
                a = sql(f'SELECT * FROM employee WHERE NAME ="{u}" AND PASSWORD = "{p}"')
                if a == []:     
                    login_error.configure(text = "** Incorrect Password or Username **")
                    messagebox.showinfo("Invalid","Incorrect Username or Password")
                else:
                    writer()
                    win.destroy()
        load = Image.open(r"images\login_butoon.jpg")
        self.admin_image = ImageTk.PhotoImage(load)
        self.admin_button = tk.Button(win,image = self.admin_image,command = l_func,border = 0)
        self.admin_button.place(x = 450,y=500)
login_page = tk.Tk()
login_page.iconbitmap(r"images\logo.ico")
obj1 = login_style(login_page)
login_page.mainloop()
password_page = tk.Tk()
password_page.iconbitmap(r"images\logo.ico")
obj = input_style(password_page)
password_page.mainloop()
with open(r"data\status.txt",'r')as f:
    a = f.readlines()
if a[0] == 'pass\n':
    if a[1] == 'employee':
        bill = tk.Tk()
        bill.iconbitmap(r"images\logo.ico")
        obj = billing(bill)
        bill.mainloop()
    else:
        adminstraion = tk.Tk()
        adminstraion.iconbitmap(r"images\logo.ico")
        obj = control(adminstraion)
        adminstraion.mainloop()
