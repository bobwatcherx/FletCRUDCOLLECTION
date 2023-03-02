from flet import *
from pocketbase import PocketBase


client = PocketBase("http://127.0.0.1:8090")

def main(page:Page):
	name_txt = TextField(label="name")
	age_txt = TextField(label="age")
	id_txt = Text()
	listcollection = Column()


	def addnewdata(e):
		# NOW I SET MY COLLECTION
		# IF YOU NOT LOGIN USER YOU NOT GET DATA ALL FROM
		# COLLECTION
		# SO YOU MUST LOGIN FOR GET ALL DATA AND EDIT DELETE
		# OPERATION COLLECTION

		auth_user = client.collection("users").auth_with_password("jaka@gmail.com","admin12345")
		col = client.collection("youtubeFlet").create({
			"name":name_txt.value,
			"age":age_txt.value
			})		
		listcollection.controls.clear()
		get_all_from_collection()
		page.snack_bar = SnackBar(
			Text("success add new data",size=30),
			bgcolor="blue"

			)
		page.snack_bar.open = True
		page.update()


	def savedatayou(e):
		auth_user = client.collection("users").auth_with_password("jaka@gmail.com","admin12345")
		col = client.collection("youtubeFlet").update(id_txt.value,{
			"name":name_txt.value,
			"age":age_txt.value
			})
		listcollection.controls.clear()
		get_all_from_collection()
		dialog_details.open = False
		page.snack_bar = SnackBar(
			Text("success edit",size=30),
			bgcolor="blue"

			)
		page.snack_bar.open = True
		page.update()

	def deletedata(e):
		auth_user = client.collection("users").auth_with_password("jaka@gmail.com","admin12345")
		col = client.collection("youtubeFlet").delete(id_txt.value)
		listcollection.controls.clear()
		get_all_from_collection()
		dialog_details.open = False
		page.snack_bar = SnackBar(
			Text("success delete",size=30),
			bgcolor="red"

			)
		page.snack_bar.open = True
		page.update()
		

	# CREATE DIALOG DETAILS FOR EDIT AND DELETE
	dialog_details = AlertDialog(
		title=Text("edit data"),
		content=Column([
			Row([
				Text("id = "),
				id_txt
				]),
			name_txt,
			age_txt,
			]),
		actions=[
			IconButton("delete",
				icon_size=40,icon_color="red",
				on_click=deletedata
				),
			TextButton("save",
				on_click=savedatayou
				),
			]

		)



	def showdetails(e):
		name_txt.value = e.control.title.value
		# THIS GET AGE 
		age_txt.value = e.control.subtitle.controls[0].value
		id_txt.value = e.control.data
		# AND OPEN DIALOG
		page.dialog = dialog_details
		dialog_details.open = True
		page.update()



	# GET ALL DATA FROM COLLECTION
	def get_all_from_collection():
		auth_user = client.collection("users").auth_with_password("jaka@gmail.com","admin12345")
		col = client.collection("youtubeFlet").get_full_list()
		# NOW PUSH TO WIDGET LIST TILE
		for x in col:
			listcollection.controls.append(
				ListTile(
				title=Text(x.name),
				subtitle=Row([Text(x.age),Text(x.created)]),
				data=x.id,
				on_click=showdetails

					)

				)
		page.update()



	# CALL FUNCTION WHEN FLET ALL FIRST OPEN THEN PUSH DATA
	# TO YOU SCREEN
	get_all_from_collection()


	page.add(
		Column([
		Text("Pocketbase crud collection",size=30),
			name_txt,
		age_txt,
		ElevatedButton("add new data",
			bgcolor="blue",color="white",
			on_click=addnewdata

			),
		Divider(),
		listcollection

			])

		)

flet.app(target=main)
