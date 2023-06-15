from kivy.app import App
from kivy.base import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

import psycopg2
import datetime
import locale 

DATABASE_URL = 'postgres://klpt_user:Q94JbsQkoSwhGT7CUDprCW0F9B80nv9a@dpg-ci59t25ph6eh6mojq44g-a.oregon-postgres.render.com/klpt'

connection = psycopg2.connect(DATABASE_URL)

connection.autocommit = True

class Studless_adminApp(App):
	aa = StringProperty('')
	def build(self):

		return BL()

class CircularButton(Button):
	button = ObjectProperty()

	def __init__(self, **kwargs):
		super(CircularButton, self).__init__()


		if 'size_hint' in kwargs:
			self.size_hint = kwargs.pop('size_hint', (1,1))
		if 'size' in kwargs:
			self.size = kwargs.pop('size', (100, 100))
		if 'width' in kwargs:
			self.width = kwargs.pop('width', 100)
		if 'height' in kwargs:
			self.height = kwargs.pop('height', 100)
		if 'pos_hint' in kwargs:
			self.pos_hint = kwargs.pop('pos_hint', (None, None))
		if 'pos' in kwargs:
			self.pos = kwargs.pop('pos', (0,0))
		if 'x' in kwargs:
			self.x = kwargs.pop('x', 0)
		if 'y' in kwargs:
			self.y = kwargs.pop('y', 0)

        # remaining args get applied to the Button
		self.butt_args = kwargs
		Clock.schedule_once(self.set_button_attrs)

	def set_button_attrs(self, dt):
		for k,v in self.butt_args.items():
			setattr(self.button, k, v)

class CustomButton(Button):
	text = StringProperty('')
	button_color = ListProperty([0, 0, 0, .2])
	text_color = ListProperty([0, 0, 0, .1])
	events_callback = ObjectProperty(None)

class CustomLabel(Label):
	text = StringProperty('')
	color = ListProperty([0, 0, 0, .1])

class CLabel(Label):
	text = StringProperty('')
	color = ListProperty([0, 0, 0, .1])

class CBoxLayout(BoxLayout):
	text = StringProperty('')
	color = ListProperty([0, 0, 0, .1])

class Menu_admin(Screen):
	pass 

class Course(Screen):
	num_course = NumericProperty(0) 

class Add_less(Screen):
	date_input = StringProperty()
	course_input = StringProperty()
	group_input = StringProperty()
	title_num_input = StringProperty()
	title_input = StringProperty()
	fio_input = StringProperty()
	build_input = StringProperty()
	def add_less(self):
		print(self.date_input)
		print(self.group_input)
		print(self.title_input)
		print(self.fio_input)
		print(self.build_input)
		fio_input = self.fio_input.split()[:3]
		firstname = fio_input[0]
		lastname = fio_input[1]
		middlename = fio_input[2]

		with connection.cursor() as cursor:

			

			cursor.execute(
							"""INSERT INTO lessons_group (name, num_less, day, firstname, lastname, middlename, building, course, name_group) 
							VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
							(self.title_input,  self.title_num_input, self.date_input, firstname, lastname, middlename, self.build_input, self.course_input, self.group_input)
				)



	def clear_inputs(self, text_inputs):
		for text_input in text_inputs:
			text_input.text = ""

class	Add_group(Screen):
	course_input_g = StringProperty()
	group_input_g	= StringProperty()

	def add_group(self):
		with connection.cursor() as cursor:

			cursor.execute(
							"""INSERT INTO list_group (name, course) VALUES (%s, %s)""",
							(self.group_input_g, self.course_input_g)
				)


	def clear_inputs(self, text_inputs):
		for text_input in text_inputs:
			text_input.text = ""

StudlessApp = Studless_adminApp()

class Group(Screen):
	num_group = NumericProperty(0) 
	box_list_g = ObjectProperty()
	title_course = ObjectProperty()
	label = StringProperty()
	
	def list_group(self, num_course):
		aa = StringProperty()
		print(self.box_list_g)
		print(type(num_course))
		print("курс={}".format(num_course))
		with connection.cursor() as cursor:

			cursor.execute(
							"""SELECT name FROM list_group WHERE course = (%s)""",
							(num_course,)
				)
			l_group = cursor.fetchall()
		print(l_group)

		self.box_list_g.clear_widgets()

		self.box_list_g.bind(minimum_height=self.box_list_g.setter('height'))

		for j in range(0, len(l_group)):
			for i in l_group[j]:
				but = CustomButton(text=f"Группа - {i}")
				but.bind(on_release=self.create_callback(i))
				self.box_list_g.add_widget(but)
		
	def create_callback(self, i):
		def callback(instance):
			StudlessApp.aa = i
			print(i)
			
			self.manager.current = 'lessons'
		return callback			
				
class Lessons(Screen):
	box_grid = ObjectProperty()
	title_course = ObjectProperty()

	
	
	def on_pre_enter(self):
		pass

	def lesson(self):
		group_name = StudlessApp.aa
		locale.setlocale(locale.LC_ALL, "")

		self.box_grid.clear_widgets()

		self.box_grid.bind(minimum_height=self.box_grid.setter('height'))

		months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
		time_start = ['9:30', '10:10', '12:05', '14:00', '15:40']
		time_end = ['10:00', '11:40', '13:35', '15:30', '17:10']
		time_now = datetime.date.today()
		delta = datetime.timedelta(days = 1)
		time_week = time_now

		self.title_course.clear_widgets()

		self.title_course.add_widget(CLabel(
				text = f"Группа {group_name}",
				color = (0, .36, .63, 1),
				font_size = 28,
				halign = "center",
				valign = "bottom"))

		for b in range(0, 7):

			with connection.cursor() as cursor:
				cursor.execute(
					"""SELECT * FROM lessons_group 
					WHERE name_group = %s AND day = %s""", 
					(group_name, time_week,)
					)
				db_lessons = cursor.fetchall()
			print(db_lessons)

			oo = time_week.weekday()
			months_num = time_week.strftime('%m')

			day = time_week.strftime("%d")
			self.label2 = CustomLabel(text=f"{day} {months[int(months_num) - 1]}, {time_week.strftime('%A')}")
			self.box0 = BoxLayout(orientation='vertical', size_hint_y=None)
			self.box0.bind(minimum_height=self.box0.setter('height'))
			self.box0.add_widget(self.label2)

			for item_day in db_lessons:
				
				self.boxx = CBoxLayout(orientation='vertical', size_hint_y=None, padding = (0, 5, 0, 5))
				self.boxx.bind(minimum_height=self.boxx.setter('height'))
					
					# for r in range(0, 4):
				self.box1 = BoxLayout(orientation='horizontal', size_hint_y=None, padding = (0, 0, 0, 5))
				self.box1.bind(minimum_height=self.box1.setter('height'))
				self.box2 = BoxLayout(orientation='vertical', size_hint_y=None, size_hint_x=0.5, padding = (0, 0, 0, 0))
				self.box2.bind(minimum_height=self.box2.setter('height'))
				self.box3 = BoxLayout(orientation='vertical', size_hint_y=None, padding = (0, 5, 0, 5))
				self.box3.bind(minimum_height=self.box3.setter('height'))
				self.box4 = BoxLayout(orientation='horizontal', size_hint_y=None, padding = (0, 5, 0, 0))
				self.box4.bind(minimum_height=self.box4.setter('height'))
				name_less = item_day[1]
					
				ln = item_day[3]
				fn = str(item_day[4])
				mn = str(item_day[5])
				build = item_day[6]
				num_les = item_day[9]
				self.label1 = CLabel(text=name_less, font_size = 20)					
				self.label3 = CLabel(text=f"{ln} {fn[0]}. {mn[0]}.", halign = "right")
				self.label4 = CLabel(text=f"ауд. {build}", halign = "left", padding = (10, 0))
				self.label7 = CLabel(text=str(num_les), font_size = 20, padding = (0, 10))
					
				a_del = num_les - 1
				time_less = f"{time_start[a_del]} - {time_end[a_del]}"
						
				self.box2.add_widget(self.label7)
				self.box2.add_widget(CLabel(text=time_less)) 
				self.box4.add_widget(self.label3)
				self.box4.add_widget(self.label4)
				self.box3.add_widget(self.label1)
				self.box3.add_widget(self.box4)

				self.box1.add_widget(self.box2)
				self.box1.add_widget(self.box3)
				self.boxx.add_widget(self.box1)
					
					

				self.box0.add_widget(self.boxx)

			self.box_grid.add_widget(self.box0)
			if len(db_lessons) == 0:
				self.boxxx = CBoxLayout(orientation='vertical', size_hint_y=None, padding = (0, 5, 0, 5))
				self.boxxx.bind(minimum_height=self.boxxx.setter('height'))
				self.lal = CLabel(text = "Выходной!!!", font_size = 20)
				self.boxxx.add_widget(self.lal)
				self.box_grid.add_widget(self.boxxx)
			time_week = time_week + delta
		
		




class Box(BoxLayout):
	pass

class BL(BoxLayout):
	total_button = NumericProperty()
	Window.size = (420, 650)
	bl = BoxLayout()
	b = Button(text='Hello world')
	bl.add_widget(b)

less = Lessons()




if __name__ == '__main__':
	StudlessApp.run()