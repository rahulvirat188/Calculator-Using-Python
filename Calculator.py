#Import the required libraries
import customtkinter as ct #GUI
from tkinter import * #GUI
import tkinter as tk #GUI
from tkinter import messagebox #ERROR BOX
import mysql.connector #BACKEND
import tabulate #BETTER TABLES
from PIL import Image,ImageTk #IMPORTING IMAGES
import math # MATHEMATICAL OPERATIONS
import asteval as ast # EVALUATION
import sympy as sp # CALCULUS
from sympy import * # MATHEMATICAL FUNCTIONS
import matplotlib.pyplot as plt # GRAPHING
import numpy as np # MATHEMATICAL FUNCTIONS
import numexpr as ne # BETTER EVALUATION
from numexpr import * # BETTER EVALUATION

class MC(ct.CTk):#class 
    def __init__(yo):
        super().__init__()
        # creating the gui screen 
        yo.geometry("700x700")
        yo.title("MATH MATE - MATEMATICAL CALCULATOR")
        ct.set_appearance_mode("dark")
        yo.resizable(0,0)
        yo.iconbitmap(r"c:\Users\Rahul M\OneDrive\Desktop\ROHIT M\CS PROJECT\logocalc.ico")
        yo.font1= ct.CTkFont(family="Courier Black", size=14, weight="bold") #a customfont
        
        # connect to MySQL database
        try:
            yo.db = mysql.connector.connect(user='root', password='rohitwalkz4558',
                                        host='localhost',  
                                        database='History')#should be created in mysql first
            print("Connected successfully")
            yo.cursor= yo.db.cursor()

            #creating the table for history

            yo.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT,
                expression TEXT,
                result TEXT,
                PRIMARY KEY (id)    )
                                    """)
            yo.db.commit()
            
        except mysql.connector.Error as err: #exceptional case
            print(f"Something went wrong: {err}")
        
        # framing the gui screen

        yo.menu_frame = ct.CTkFrame(yo, width=200, corner_radius=0, fg_color="#333333")
        yo.menu_frame.pack(side="left", fill="y")

        yo.content_frame = ct.CTkFrame(yo)
        yo.content_frame.pack(side="right", fill="both", expand=True)

        yo.frame1 = ct.CTkFrame(yo.content_frame)
        yo.frame1.pack(fill="both", expand=True)
        
        yo.frame2= ct.CTkFrame(yo.content_frame)
        yo.frame2.pack(fill="both", expand=True)
        yo.frame2.pack_forget()

        yo.frame3 = ct.CTkFrame(yo.content_frame)
        yo.frame3.pack(fill="both", expand=True)
        yo.frame3.pack_forget()

        yo.frame4 = ct.CTkFrame(yo.content_frame)
        yo.frame4.pack(fill="both", expand=True)
        yo.frame4.pack_forget()
        
        #importing images

        yo.i1=Image.open(r"C:\Users\Rahul M\OneDrive\Desktop\ROHIT M\CS PROJECT\home_icon.png")
        yo.i2=Image.open(r"C:\Users\Rahul M\OneDrive\Desktop\ROHIT M\CS PROJECT\calculus_icon.png")
        yo.i3=Image.open(r"C:\Users\Rahul M\OneDrive\Desktop\ROHIT M\CS PROJECT\graph_icon.png")
        yo.i4=Image.open(r"C:\Users\Rahul M\OneDrive\Desktop\ROHIT M\CS PROJECT\quit_icon.png")
        yo.i5=Image.open(r"C:\Users\Rahul M\OneDrive\Desktop\ROHIT M\CS PROJECT\returns_icon.png")
        yo.i6=Image.open(r"C:\Users\Rahul M\OneDrive\Desktop\ROHIT M\CS PROJECT\LOGO.png.png")

        #main method calls 
        yo.swap = False
        yo.create_menu_buttons()
        yo.frame1_calculator()
        yo.frame2_calculator()
        yo.frame3_calculator()
        
        #inserting logo
        yo.logo_image = yo.i6
        yo.logo_image = ImageTk.PhotoImage(yo.logo_image.resize((200, 280)))
        yo.logo_label = tk.Label(yo, image=yo.logo_image)
        yo.logo_label.place(x=25, y=2)

    def create_menu_buttons(yo): #creation of menu
        images=[yo.i1,yo.i2,yo.i3,yo.i4]
        texts = ["Home", "Calculus", "Graphing", "Quit"]
        commands = [yo.switch_to_frame1, yo.switch_to_frame2, yo.switch_to_frame3,yo.switch_to_frame4]
        b = ct.CTkButton(yo, text="MATH-MATE", font=("Arial Black",20), corner_radius=10, fg_color="#333333", bg_color="#333333", hover_color="#333333")
        b.place(x=20, y=230)

        for i in range(4):
            images2=ct.CTkImage(dark_image=images[i],light_image=images[i])
            button = ct.CTkButton(yo.menu_frame,text_color="black", text=texts[i], font=yo.font1,image=images2, width=170, height=70, command=commands[i],fg_color="white",hover_color="#666666",)
            button.place(x=16, y=300 + i * 100)      
        yo.oscillate_colors(b, ["#FFA07A", "#FFC080", "#FFFF00", "#00BFFF", "#0080FF"])

    def oscillate_colors(yo, button, colors, delay=500):
        color_index = 0
        def update_colors():
            nonlocal color_index
            button.configure(text_color=colors[color_index % len(colors)])
            color_index += 1
            button.after(delay, update_colors)
        update_colors()

    def frame1_calculator(yo): #defining and creation of frame1 widgets
        yo.entry1=ct.CTkEntry(yo.frame1,placeholder_text="0",justify="right",width=490,height=160,fg_color="black", border_color="#646665", border_width=4, corner_radius=10, font=("Courier", 24), placeholder_text_color="white", text_color="white")
        yo.entry1.place(x=5,y=5)  
        yo.entry1.bind("<KeyRelease>", yo.adjust_font_size)  
        yo.d1= ct.CTkButton( yo.frame1, text="History", text_color="white",fg_color="#0a0a0a", height=30,  font=yo.font1, image=ct.CTkImage(dark_image=yo.i5), command=yo.history).place(x=356,y=170)
        yo.triglist=["◣ Trig Fn","sin","cos","tan","cosec","sec","cot","sin⁻¹","cos⁻¹","tan⁻¹","cot⁻¹","sec⁻¹","cosec⁻¹"]
        yo.func=["ƒ Functions","|x|","⌈x⌉","⌊x⌋"]
        yo.d2 = ct.CTkComboBox(yo.frame1, values=yo.triglist, text_color="white", fg_color="#333333",dropdown_text_color="white", dropdown_fg_color="#333333",dropdown_hover_color="#666666", height=30, font=yo.font1, command=lambda value1: yo.trig_value(value1))
        yo.d2.place(x=10, y=170)
        yo.d2.set("◣ Trig Fn")
        yo.d3 = ct.CTkComboBox(yo.frame1, values=yo.func, text_color="white", fg_color="#333333",dropdown_text_color="white", dropdown_fg_color="#333333",dropdown_hover_color="#666666", height=30, font=yo.font1, command=lambda value2: yo.func_value(value2))
        yo.d3.place(x=160, y=170)
        yo.d3.set("ƒ Functions")

        numbers = [7, 8, 9, 4, 5, 6, 1, 2, 3, 0]
        xcords = [103, 201, 299, 103, 201, 299, 103, 201, 299, 201]
        ycords = [415, 415, 415, 485, 485, 485, 555, 555, 555, 625]
        yo.c1 = ct.CTkButton(yo.frame1, text=".", width=97.19, height=70, font=("Courier Black", 24),command=lambda: yo.operators("."))
        yo.c1.place(x=103, y=625)
        yo.buttons = []
        for i in numbers:
            button = ct.CTkButton(yo.frame1, text=str(i), width=97, height=70, font=("Courier Black", 24), fg_color="#0a0a0a", command=lambda value=i: yo.num(value))
            button.place(x=xcords[i-1], y=ycords[i-1])
            yo.buttons.append(button)

        operator= ["+", "-", "×", "÷", "^", "⌫", "n!", "floor(÷)", "C", "τ", "mod(÷)", "ℯ", "1/x", "π"]
        xcords =   [397, 397, 397, 397, 397, 397, 299, 299, 299, 103, 201, 201, 103, 103]
        ycords =   [555, 485, 415, 345, 275, 205, 345, 275, 205, 345, 275, 205, 275, 205]
        yo.c1a= ct.CTkButton(yo.frame1, text="(", width=49, height=70,fg_color="#666666", font=("Courier Black", 24),command=lambda: yo.operators("(")).place(x=299, y=625)
        yo.c1b= ct.CTkButton(yo.frame1, text=")", width=49, height=70,fg_color="#666666", font=("Courier Black", 24),command=lambda: yo.operators(")")).place(x=348, y=625)
        yo.c1c= ct.CTkButton(yo.frame1, text="deg/rad", width=97.8, height=70,fg_color="#666666", font=("Courier Black", 20),command=yo.open_degrad).place(x=201, y=345)

        yo.e1= ct.CTkButton(yo.frame1,text="ln", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("ln"))
        yo.e1.place(x=5, y=625)
        yo.e2= ct.CTkButton(yo.frame1,text="log", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("log"))
        yo.e2.place(x=5, y=555)
        yo.e3= ct.CTkButton(yo.frame1,text="10ⁿ", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("10ⁿ"))
        yo.e3.place(x=5, y=485)
        yo.e4= ct.CTkButton(yo.frame1,text="x%", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("x%"))
        yo.e4.place(x=5, y=415)
        yo.e5= ct.CTkButton(yo.frame1,text="√x", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("√x"))
        yo.e5.place(x=5, y=345)
        yo.e6= ct.CTkButton(yo.frame1,text="x²", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("x²"))
        yo.e6.place(x=5, y=275)
        yo.e7= ct.CTkButton(yo.frame1,text="⇆", width=98, height=70,fg_color="#666666", font=("Courier Black", 40), command=yo.show)
        yo.e7.place(x=5, y=205)

        yo.f1= ct.CTkButton(yo.frame1,text="x³", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("x³"))
        yo.f1.place_forget()
        yo.f2= ct.CTkButton(yo.frame1,text="³√x", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("³√x"))
        yo.f2.place_forget()
        yo.f3= ct.CTkButton(yo.frame1,text="ⁿ√x", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("ⁿ√x"))
        yo.f3.place_forget()
        yo.f4= ct.CTkButton(yo.frame1,text="2ⁿ", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("2ⁿ"))
        yo.f4.place_forget()
        yo.f5= ct.CTkButton(yo.frame1,text="logₓ(y)", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("logₓ(y)"))
        yo.f5.place_forget()
        yo.f6= ct.CTkButton(yo.frame1,text="eⁿ", width=98, height=70,fg_color="#666666", font=("Courier Black", 24), command=lambda: yo.operators("eⁿ"))
        yo.f6.place_forget()
        for i in range(len(operator)):
            yo.operator = ct.CTkButton(yo.frame1, text=operator[i], width=98, height=70, font=("Courier Black", 20), fg_color="#666666", command=lambda value=str(operator[i]): yo.operators(value)).place(x=xcords[i], y=ycords[i])
        yo.c2 = ct.CTkButton(yo.frame1, text="=", width=98, height=70, font=("Courier Black", 24), command=yo.equals).place(x=397, y=625)
    
    def frame2_calculator(yo): #calculus solver
        yo.e1 = ct.CTkLabel(yo.frame2, text="Enter expression:", font=("Courier Black", 24))
        yo.e1.place(x=5, y=5)

        yo.e2 = ct.CTkEntry(yo.frame2, width=490, height=160, fg_color="black", border_color="#646665", border_width=4, corner_radius=10, font=("Courier", 24), placeholder_text="0", placeholder_text_color="white", text_color="white")
        yo.e2.place(x=5, y=50)

        yo.l1 = ct.CTkLabel(yo.frame2, text="Enter variable (e.g. x):", font=("Courier Black", 24))
        yo.l1.place(x=5, y=220)

        yo.e3 = ct.CTkEntry(yo.frame2, width=490, height=70, fg_color="black", border_color="#646665", border_width=4, corner_radius=10, font=("Courier", 24), placeholder_text="", placeholder_text_color="white", text_color="white")
        yo.e3.place(x=5, y=250)

        yo.l2 = ct.CTkLabel(yo.frame2, text="Select problem type:", font=("Courier Black", 24))
        yo.l2.place(x=5, y=330)

        yo.v = ct.StringVar()
        yo.v.set("differentiation")

        yo.r1 = ct.CTkRadioButton(yo.frame2, text="Differentiation", variable=yo.v, value="differentiation", font=("Courier Black", 24), fg_color="#0a0a0a")
        yo.r1.place(x=5, y=360)

        yo.r2 = ct.CTkRadioButton(yo.frame2, text="Integration", variable=yo.v, value="integration", font=("Courier Black", 24), fg_color="#0a0a0a")
        yo.r2.place(x=5, y=400)

        yo.b1 = ct.CTkButton(yo.frame2, text="Solve", command=yo.solve_problem, width=98, height=70, font=("Courier Black", 24), fg_color="#0a0a0a")
        yo.b1.place(x=5, y=440)

        yo.l3 = ct.CTkLabel(yo.frame2, text="", font=("Courier Black", 24))
        yo.l3.place(x=5, y=510)
    
    def frame3_calculator(yo): #graphing
        yo.f3 = ct.CTkFrame(yo.frame3, width=500, height=600, corner_radius=10, fg_color="#2a2d2e")
        yo.f3.place(x=510, y=10)

        yo.l4 = ct.CTkLabel(yo.frame3, text="Enter function to plot:", font=("Courier Black", 24))
        yo.l4.place(x=5, y=5)

        yo.e4 = ct.CTkEntry(yo.frame3, width=490, height=70, fg_color="black", border_color="#646665", border_width=4, corner_radius=10, font=("Courier", 24), placeholder_text="", placeholder_text_color="white", text_color="white")
        yo.e4.place(x=5, y=40)

        yo.b2 = ct.CTkButton(yo.frame3, text="Plot Graph", command=lambda: yo.plot_graph(yo.e4.get()), width=98, height=70, font=("Courier Black", 24), fg_color="#0a0a0a")
        yo.b2.place(x=5, y=120)

    def plot_graph(yo, func_str):
        try:
            x = np.linspace(-10, 10, 400)
            func_str = func_str.replace('^', '**')  # Replace ^ with ** for exponentiation

            # Evaluate the function using numexpr
            y = ne.evaluate(func_str)

            plt.plot(x, y)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Graph of ' + func_str)
            plt.grid(True)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def solve_problem(yo):
        expression = yo.e2.get()
        variable = yo.e3.get()
        problem_type = yo.v.get()
        try:
            if problem_type == "differentiation":
                result = yo.differentiate(expression, variable)
            else:
                result = yo.integrate(expression, variable)

            yo.l3.configure(text=f"Result: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def differentiate(yo, expression, variable):
        var = sp.symbols(variable)
        expr = sp.sympify(expression)
        expr = sp.trigsimp(expr)
        expr = sp.powsimp(expr)
        diff_expr = sp.diff(expr, var)
        result = str(diff_expr)
        return result

    def integrate(yo, expression, variable):
        var = sp.symbols(variable)
        expr = sp.sympify(expression)
        expr = sp.trigsimp(expr)
        expr = sp.powsimp(expr)
        int_expr = sp.integrate(expr, var)
        result = str(int_expr)
        return result

    def show(yo): #shows the hidden operators by swapping 
        if yo.swap:
            yo.e1.place(x=5, y=625)
            yo.e2.place(x=5, y=555)
            yo.e3.place(x=5, y=485)
            yo.e4.place(x=5, y=415)
            yo.e5.place(x=5, y=345)
            yo.e6.place(x=5, y=275)
            
            yo.f1.place_forget()
            yo.f2.place_forget()
            yo.f3.place_forget()
            yo.f4.place_forget()
            yo.f5.place_forget()
            yo.f6.place_forget()
        else:
            yo.e1.place_forget()
            yo.e2.place_forget()
            yo.e3.place_forget()
            yo.e4.place_forget()
            yo.e5.place_forget()
            yo.e6.place_forget()
            
            yo.f1.place(x=5, y=625)
            yo.f2.place(x=5, y=555)
            yo.f3.place(x=5, y=485)
            yo.f4.place(x=5, y=415)
            yo.f5.place(x=5, y=345)
            yo.f6.place(x=5, y=275)
            
        yo.swap = not yo.swap
            
    def adjust_font_size(yo, event): #adjust font size in the entry box
        text_length = len(yo.entry1.get())
        font_size = 24
        if text_length > 20:
            font_size -= (text_length - 20) * 0.1
        font_size = max(10, font_size) 
        yo.entry1.configure(font=("Courier", int(font_size)))

    def switch_to_frame1(yo):
        yo.frame2.pack_forget()
        yo.frame3.pack_forget()
        yo.frame4.pack_forget()
        yo.frame1.pack(fill="both", expand=True)

    def switch_to_frame2(yo):
        yo.frame1.pack_forget()
        yo.frame3.pack_forget()
        yo.frame4.pack_forget()
        yo.frame2.pack(fill="both", expand=True)

    def switch_to_frame3(yo):
        yo.frame1.pack_forget()
        yo.frame2.pack_forget()
        yo.frame4.pack_forget()
        yo.frame3.pack(fill="both", expand=True)

    def switch_to_frame4(yo):
        yo.destroy()

    def trig_value(yo,value1): #trigonometric functions
        if value1!="◣ Trig Fn":
            yo.entry1.delete(0, "end")  
            yo.entry1.insert(0, value1)
            yo.adjust_font_size(None)
            yo.d2.set("◣ Trig Fn")
            try:
                if value1 == "sin":
                    try:
                        yo.n1window = ct.CTkToplevel(yo.frame1)
                        yo.n1window.title("Sine")
                        yo.n1window.geometry("200x200")

                        yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                        yo.n1entry.place(x=10,y=50)
                        yo.n1label=ct.CTkLabel(yo.n1window,text="The Value in Radians:").place(x=5,y=2)
                        def ok():
                            try:
                                v = float(yo.n1entry.get())
                                i= math.sin(v)
                                yo.entry1.delete(0, "end") 
                                yo.entry1.insert(0, i) 
                                yo.adjust_font_size(None)
                                yo.n1window.destroy()
                            except Exception as e:
                                messagebox.showerror("Error",str(e))
                        yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                    except Exception as e:
                        messagebox.showerror("Error",str(e))
                
                elif value1 == "cos":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Cosine")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value in Radians:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= math.cos(v)
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value1 == "tan":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Tangent")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value in Radians:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= math.tan(v)
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value1 == "cosec":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Cosecant")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value in Radians:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= 1/(math.sin(v))
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value1 == "sec":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Secant")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value in Radians:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= 1/(math.cos(v))
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value1 == "cot":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Cotangent")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value in Radians:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= 1/(math.tan(v))
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value1 == "sin⁻¹":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Arcsine")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= math.asin(v)
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value1 == "cos⁻¹":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Arccosine")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= math.acos(v)
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value1 == "tan⁻¹":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Arctangent")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= math.atan(v)
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
            
                elif value1 == "cot⁻¹":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Arccotangent")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= 1/(math.atan(v))
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value1 == "sec⁻¹":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Arcsecant")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= 1/(math.acos(v))
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value1 == "cosec⁻¹":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Arccosecant")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i= 1/(math.asin(v))
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            yo.d2.set("◣ Trig Fn")

        else:
            yo.entry1.delete(0, "end")  
            messagebox.showerror("Error", "Invalid Input")

    def func_value(yo,value2): #mathematical functions
        if value2!="ƒ Functions":
            yo.entry1.delete(0, "end")  
            yo.entry1.insert(0, value2)
            yo.adjust_font_size(None)
            yo.d3.set("ƒ Functions")
            try:
                if value2 == "|x|":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Absolute Value")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i=abs(v)
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value2 == "⌈x⌉":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Ceiling")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i=math.ceil(v)
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                
                elif value2 == "⌊x⌋":
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Floor")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="The Value:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            i=math.floor(v)
                            yo.entry1.delete(0, "end") 
                            yo.entry1.insert(0, i) 
                            yo.adjust_font_size(None)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            yo.entry1.delete(0, "end")  
            messagebox.showerror("Error","Invalid Input")

    def num(yo,v):#defining number pad
        curr = yo.entry1.get()
        yo.entry1.delete(0, END)
        yo.entry1.insert(0, str(curr) + str(v))
        yo.adjust_font_size(None)
    
    def operators(yo, op): #defining operators
        l1=["+", "-", "×", "÷","(",")",".","floor(÷)","mod(÷)"]
        if op in l1:
            if op == "floor(÷)":
                curr = yo.entry1.get()
                yo.entry1.delete(0, END)
                yo.entry1.insert(0, curr + "//")
                yo.adjust_font_size(None)
            elif op == "mod(÷)":
                curr = yo.entry1.get()
                yo.entry1.delete(0, END)
                yo.entry1.insert(0, curr + "%")
                yo.adjust_font_size(None)
            elif op == "(":
                pos = len(yo.entry1.get())
                yo.entry1.insert(pos, '(')
                yo.adjust_font_size(None)
            elif op == ")":
                pos = len(yo.entry1.get())
                yo.entry1.insert(pos, ')')
                yo.adjust_font_size(None)

            else:
                curr = yo.entry1.get()
                yo.entry1.delete(0, END)
                yo.entry1.insert(0, str(curr) + str(op))
                yo.adjust_font_size(None)
            
        else:
            if op == "^":
                try:
                    yo.entry1.insert(END, "**")
                    yo.adjust_font_size(None)
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "τ":
                try:
                    yo.entry1.insert(END, "τ")
                    yo.adjust_font_size(None)
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "ℯ":
                try:
                    yo.entry1.insert(END, "ℯ")
                    yo.adjust_font_size(None)
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "π":
                try:
                    yo.entry1.insert(END, "π")
                    yo.adjust_font_size(None)
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "C":
                try:
                    yo.entry1.delete(0, END)
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "⌫":
                try:
                    yo.entry1.delete(yo.entry1.index(END)-1, END)
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "n!":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Factorial")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of n is:").place(x=5,y=2)
                    def ok():
                        try:
                            v = int(yo.n1entry.get())
                            fact= math.factorial(v)
                            yo.entry1.insert(END , fact)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "1/x":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("Reciprocal")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of x is:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            rec=1/(v)
                            yo.entry1.insert(END , rec)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "log":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("logarithm to base 10")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of log of:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            log=math.log(v,10)
                            yo.entry1.insert(END , log)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "ln":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("natural logarithm")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of natural log of:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            log=math.log(v)
                            yo.entry1.insert(END , log)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "10ⁿ":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("exponent")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of the power:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            exp=10**v
                            yo.entry1.insert(END , exp)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "x%":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("percentage")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of x: ").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            per= v/100
                            yo.entry1.insert(END , per)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "√x":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("square root")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of x: ").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            t = math.sqrt(v)
                            yo.entry1.insert(END , t)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "x²":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("square")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of x: ").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            t = math.pow(v,2)
                            yo.entry1.insert(END , t)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "x³":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("cube")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of x:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            t= v**3
                            yo.entry1.insert(END , t)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "³√x":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("cube root")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of x:").place(x=5,y=2)
                    def ok():
                        try:
                            v = float(yo.n1entry.get())
                            log= math.cbrt(v)
                            yo.entry1.insert(END , log)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "ⁿ√x":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("y root x")
                    yo.n1window.geometry("200x200")
                    yo.n1entry2=ct.CTkEntry(yo.n1window, placeholder_text="the value of x:" ,width=170, height=30)
                    yo.n1entry2.place(x=10,y=30)
                    yo.n1entry=ct.CTkEntry(yo.n1window, placeholder_text="the value of n:", width=170, height=30)
                    yo.n1entry.place(x=10,y=60)
                    
                    def ok():
                        try:
                            n= float(yo.n1entry.get())
                            x= float(yo.n1entry2.get())
                            f= math.pow(x,1/n)
                            yo.entry1.insert(END , f)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=100)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "logₓ(y)":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("log of y to the base x")
                    yo.n1window.geometry("200x200")
                    yo.n1entry2=ct.CTkEntry(yo.n1window, placeholder_text="the value of x:" ,width=170, height=30)
                    yo.n1entry2.place(x=10,y=30)
                    yo.n1entry=ct.CTkEntry(yo.n1window, placeholder_text="the value of y:", width=170, height=30)
                    yo.n1entry.place(x=10,y=60)
                    
                    def ok():
                        try:
                            y= float(yo.n1entry.get())
                            x= float(yo.n1entry2.get())
                            f= math.log(y,x)
                            yo.entry1.insert(END , f)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=100)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "2ⁿ":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("2 raised to n")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of n: ").place(x=5,y=2)
                    def ok():
                        try:
                            n = float(yo.n1entry.get())
                            t = 2**n
                            yo.entry1.insert(END , t)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))
            if op == "eⁿ":
                try:
                    yo.n1window = ct.CTkToplevel(yo.frame1)
                    yo.n1window.title("e raised to n")
                    yo.n1window.geometry("200x200")

                    yo.n1entry=ct.CTkEntry(yo.n1window, width=170, height=30)
                    yo.n1entry.place(x=10,y=50)
                    yo.n1label=ct.CTkLabel(yo.n1window,text="the value of n: ").place(x=5,y=2)
                    def ok():
                        try:
                            n = float(yo.n1entry.get())
                            t = 2.71828**n
                            yo.entry1.insert(END , t)
                            yo.n1window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error",str(e))
                    yo.n1butt=ct.CTkButton(yo.n1window,text="OK",command=ok).place(x=30,y=90)
                    
                except Exception as e:
                    messagebox.showerror("Error",str(e))

    def equals(yo): #equal operator which is used for evaluation of the expressions
        try:
            exp = yo.entry1.get()
            exp = exp.replace("×", "*").replace("÷", "/").replace("ℯ", "2.71828").replace("π", "3.14159265359").replace("τ", "6.28320")

            yo.result = ne.evaluate(exp)

            aeval = ast.Interpreter()
            yo.astresult = aeval(exp)
            
            yo.entry1.delete(0, END)
            yo.entry1.insert(0, str(yo.result))
            
            query = "INSERT INTO history (expression, result) VALUES (%s, %s)"
            values = (exp, (yo.astresult))
            yo.cursor.execute(query, values)
            yo.db.commit()
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            yo.entry1.delete(0, END)
           
    def open_degrad(yo): #degree and radian conversion
        yo.degrad = ct.CTkToplevel(yo.frame1)
        yo.degrad.geometry("300x200")
        yo.degrad.title("Angle Converter")

        rad = ct.CTkLabel(yo.degrad, text="Radians:")
        rad.place(x=10, y=10)

        yo.e_rad = ct.CTkEntry(yo.degrad)
        yo.e_rad.place(x=100, y=10)

        deg = ct.CTkLabel(yo.degrad, text="Degrees:")
        deg.place(x=10, y=40)

        yo.e_deg = ct.CTkEntry(yo.degrad)
        yo.e_deg.place(x=100, y=40)

        def degrad():
            try:
                rad_val = yo.e_rad.get()
                deg_val = yo.e_deg.get()

                if rad_val:
                    rad = float(rad_val)
                    deg = rad * 180 / 3.14159
                    yo.e_deg.delete(0, ct.END)
                    yo.e_deg.insert(0, str(deg))
                elif deg_val:
                    deg = float(deg_val)
                    rad = deg * 3.14159 / 180
                    yo.e_rad.delete(0, ct.END)
                    yo.e_rad.insert(0, str(rad))
                else:
                    messagebox.showerror("Error", "Please enter a value to convert")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a number.")

        convert = ct.CTkButton(yo.degrad, text="Convert", command=degrad)
        convert.place(x=100, y=70)

        close = ct.CTkButton(yo.degrad, text="Close", command=lambda: yo.degrad.destroy())
        close.place(x=100, y=100)

    def history(yo):  # shows history in a different window
        try:
            yo.cursor.execute("SELECT id, expression, result FROM history ORDER BY id DESC")
            row = yo.cursor.fetchall()
            rows = (row)
            yo.n3window = ct.CTkToplevel(yo.frame1)
            yo.n3window.title("HISTORY")
            yo.n3window.geometry("600x500")  
            yo.n3window.resizable(0, 0) 
            yo.n3window.configure(bg_color="#2b2b2b", fg_color="white")
            yo.font_size = 11
            yo.t = ct.CTkTextbox(yo.n3window, width=550, height=400, text_color="#ffffff", bg_color="#2b2b2b", fg_color="#2b2b2b", font=("Courier", yo.font_size))
            yo.t.pack(padx=20, pady=20)

            headers = ["ORDER", "EXPRESSIONS", "RESULT"]
            table = tabulate.tabulate(rows, headers, tablefmt="grid")
            yo.t.insert(ct.END, table + "\n")

            clear = ct.CTkButton(yo.n3window, text="Clear History", font=yo.font1, command=lambda: clear_history(yo))
            clear.place(x=24, y=423)

            maximum = ct.CTkButton(yo.n3window, width=10, text="+", font=yo.font1, command=lambda: max_zoom(yo))
            maximum.place(x=550, y=423)

            minimum = ct.CTkButton(yo.n3window, width=20, text="-", font=yo.font1, command=lambda: min_zoom(yo))
            minimum.place(x=530, y=423)

            close = ct.CTkButton(yo.n3window, text="Close", font=yo.font1, command=yo.n3window.destroy)
            close.place(x=230, y=450)

        except Exception as e:
            messagebox.showerror("Error", str(e))

        def clear_history(yo):
            try:
                yo.cursor.execute("DROP TABLE IF EXISTS history")
                yo.db.commit()
                yo.cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INT AUTO_INCREMENT,
                    expression TEXT,
                    result TEXT,
                    PRIMARY KEY (id)
                )
                """)
                yo.db.commit()
                yo.t.delete(1.0, ct.END)
                yo.t.insert(ct.END, "There's nothing to see here....")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def max_zoom(yo):
            yo.font_size += 1
            yo.t.configure(font=("Courier", yo.font_size)) 

        def min_zoom(yo):
            if yo.font_size > 5:  
                yo.font_size -= 1
                yo.t.configure(font=("Courier", yo.font_size)) 

    def close_database(yo): #closing database
        if yo.db:
            yo.cursor.close()
            yo.db.close()

if __name__=="__main__": #closing the instance of the class object
    mpc = MC() 
    mpc.mainloop() 
    mpc.close_database()