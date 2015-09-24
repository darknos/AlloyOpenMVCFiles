import sublime, sublime_plugin, re, os, functools, subprocess, json

TYPES = { 
			"controller" : { 
				"folder" : "/controllers/",
				"ext" : ".js",
				"group" : 0
			},
			"view" : { 
				"folder" : "/views/",
				"ext" : ".xml",
				"group" : 2
			},
			"style" : {
				"folder" : "/styles/",
				"ext" : ".tss",
				"group" : 1
			}
		}

def translateToType(fullpath, command):
		dirName = os.path.dirname(fullpath) + "/"
		baseName, extension = os.path.splitext(os.path.basename(fullpath))
		newDirName = functools.reduce(lambda acc, x: acc.replace( x["folder"], TYPES[command]["folder"]), TYPES.values(), dirName)
		return newDirName + baseName + TYPES[command]["ext"]

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
		
		for key, value in TYPES.items():
			new_window.focus_group(value["group"])
			new_window.open_file(translateToType(fname, key))


class TiSwitchCommand(sublime_plugin.WindowCommand):
	def run(self, *args, **kwargs):
		activeWindow = sublime.active_window();
		activeView = activeWindow.active_view()
		currentFile = activeView.file_name()
		
		if(currentFile is None):
			return

		switchType = kwargs["type"];
		fileSwitchTo = translateToType(currentFile, switchType)

		if not os.path.exists(fileSwitchTo) :
			print("File does not exist");
			return

		if activeWindow.num_groups() == len(TYPES) :
			activeWindow.focus_group(TYPES[switchType]["group"])
		
		activeWindow.open_file(fileSwitchTo)

class TiGenerateRunMenuCommand(sublime_plugin.WindowCommand):
	def run(self, *args, **kwargs):
		text = "".join(subprocess.getoutput("instruments -s devices"))
		device_list = re.split("\n", text);
		devices = []
		for device in device_list:
			true_device = parse_device_string(device)
			if true_device:
				devices.append(true_device)

		# for device in devices:
		# 	#make menu here
		package_path = os.path.join(sublime.packages_path(), "AlloyMVCFiles")
		menu_json_path = package_path + "/Main.sublime-menu"
		with open(menu_json_path, "r") as jsonFile:
			data = json.load(jsonFile)
		print("data", data)

		menu = []

		for device in devices:
			print("opath:", data[0]['children'][0]['children'])
			menu.append({'caption' : device['name'], 'command' : "ti_run" , "args" : {'uuid' : device['uuid']}})

		data[0]['children'][0]['children'] = menu

		with open(menu_json_path, "w") as jsonFile:
			jsonFile.write(json.dumps(data))

		print("package_path", package_path)
		print("devices:", devices)

def parse_device_string(str):
		print(str)
		match =  re.match(r"(.* \((.*)\)) \[([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})\]", str);
		if match :
			return {'uuid' : match.group(3), 'name': match.group(1), 'ios' : match.group(2)}
	
class TiRunCommand(sublime_plugin.WindowCommand):
 	def run(self, *args, **kwargs):
 		print('TI RUN:', kwargs)