import sublime, sublime_plugin

def fixed_set_layout(window, layout):
	#A bug was introduced in Sublime Text 3, sometime before 3053, in that it
	#changes the active group to 0 when the layout is changed. Annoying.
	active_group = window.active_group()
	window.set_layout(layout)
	num_groups = len(layout['cells'])
	window.focus_group(min(active_group, num_groups-1))

class NewWindowWithAlloyFilesCommand(sublime_plugin.WindowCommand):
	def run(self):
		layout = {}
		layout['cells'] = [[0.0,0.0,1.0,1.0],[1.0,0.0,2.0,2.0],[0.0,1.0,1.0,2.0]]
		layout['cols'] = [0.0,0.774979105688,1.0]
		layout['rows'] = [0.0,0.69627419099,1.0]
		fname = sublime.active_window().active_view().file_name()
		sublime.active_window().run_command("new_window")
		new_window = sublime.active_window()
		fixed_set_layout(new_window, layout)
		new_window.focus_group(2)
		new_window.open_file(fname.replace("/controllers/", "/views/").replace(".js", ".xml"))
		new_window.focus_group(1)
		new_window.open_file(fname.replace("/controllers/", "/styles/").replace(".js", ".tss"))				
		new_window.focus_group(0)
		new_window.open_file(fname)		