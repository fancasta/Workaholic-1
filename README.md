# Workaholic - Your Project Manager

<p align="center">A Python Django web application that helps you manage your projects!</p>
<p align="center">
	<a href="http://www.youtube.com/watch?feature=player_embedded&v=UVxHLNX_0dE" target="_blank" title="App Video Demo">		
		<img src="https://github.com/chinhockyang/workaholic/blob/master/workaholic/backend/backend/static/photo/logo18.png?raw=true" alt="IMAGE ALT TEXT HERE" width="480" border="10" />
	</a>
</p>

<h5>Summer Vacation Web Development Project by:</h5><p>Chin Hock Yang and Nguyen An Khanh</p>

<h5>Motivation:</h5>
<p>
When assigned a project, it is important for a student to be clear of the project deliveries and deadlines. Having a detailed plan will allow the student to pace himself towards the completion of the project. However as the number of deadlines increases due to the accumulation of workload across modules, many students feel overwhelmed and often struggle to make an organised plan for their projects. Without a clear direction to work towards, students end up wasting time and efforts on insignificant tasks. This often leads to a poorly-paced project, where students have to “rush” to put together an unproductive last-minute work to meet deadlines. Furthermore, when working in group projects, miscommunication often exists due to lack of group meetings, or due to important messages “buried”  in project group chats. This results in group members being unaware of their taskings, as well as the important project timeline and goals.
</p>

<h5>Aim:</h5>
<p>
We hope to provide a platform for one to plan and manage important deadlines and to-dos of his projects. 
We also aim to improve group communication and teamwork, so that group members can easily access important project information and updates of their projects.
</p>

<h5>Target User:</h5>
<p>
Anyone working in any form of individual or group projects. While the source of our motivation is students, our platform can also be utilised by other professionals who are also working in courseworks or projects.
</p>

<h5>App components:</h5>

| Components | Description |
| :------------- |:-------------|
| Authentication and Account Management | Login / Logout feature to ensure the security of each user account |
| Project Management | Allow users to share their project with their project members, and ensure that their project isn’t accessible to outsiders. |
| Project Todo | Prevent confusion on the tasks that are assigned to each group member, and prevent miscommunication of tasks deadlines. |
| Project Calendar | Allow users to be reminded of important deadlines. Help users to manage their time and pace their project. |
| Project Board | Users are able to constantly refer to the “big-picture plan” to ensure that they stay on track for their projects. Group project members can easily update (or be updated on) important messages / announcements for the project. |
| Project Chat Space |To facilitate group discussions and improve teamwork among group members. |

<h5>Program flow:</h5>
<p align="center">
<img src="https://user-images.githubusercontent.com/65223310/113096561-fa8f3080-9227-11eb-8faf-4984e72d22b9.jpeg" width="600" border="10" />
</p>

<h5>Tech Stack:</h5>

| Dependencies | Description |
| :------------- |:-------------|
| `django>=3.0.12` | Backend framework |
| SQLite3 | Database |
| Bootstrap 4 | User Interface and Web Design |
| `Pillow==7.1.2` | Opening, manipulating, and saving many different image file formats |
| `django-ckeditor==5.9.0` | Add Rich text editor into our application |
| `django-bower==5.2.0` | Image library for CKEditor |
| `Jinja2==2.11.2` | Allow usage of templating engine and placeholder inside html file |
