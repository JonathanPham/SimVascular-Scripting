class sv_model:
	def __init__(self,file_path,GUI=False):
		import sys,os
		import numpy as np 
		try:
			self.clear()
			print('Gathering CSV Data...')
			self.data = np.genfromtxt(file_path, delimiter=',',dtype=str)
			print('Creating project...')
			self.name = os.path.basename(file_path)
			self.data_manager = {'Paths'      :[],
								 'Contours'   :[],
								 'PolyData'   :[],
								 'Solids'     :[],
								 'VTK'        :[],
								 'Mesh'       :[],
								 'Simulation' :[],
								 'Full_Paths' :{},
								 'Path_Points':{},
								 'Path_Contours':{},
								 'Path_PolyData':{},
								 'Path_SampleData':{},
								 'Path_AlignedData':{},
								 'Path_Lofts':{},
								 'Path_AlignedData_Sampled':{}}
		except:
			print('File_path is inaccessible...')
			return 
		self.GUI = GUI
		self.path()
		self.contour()
		self.loft()
		self.solid()

	def __path__(self,sv_path,sv_path_name): #PASSING
		from sv import Path,GUI,Repository
		p = Path.pyPath()
		p.NewObject(sv_path_name)

		self.data_manager['Path_Points'][sv_path_name] = []
		for i in range(len(sv_path[:,0])):
			temp = []
			for j in sv_path[i][:]:
				temp.append(float(j))
			self.data_manager['Path_Points'][sv_path_name].append(temp)
			p.AddPoint(temp)
		p.CreatePath()
		self.data_manager['Paths'].append(sv_path_name)
		if self.GUI == True:
			GUI.ImportPathFromRepos(sv_path_name,'Paths')

	def path(self): #PASSING
		import numpy as np 
		self.path_radii = {}
		ind = int(np.nonzero(self.data[0,:]=='Path')[0]) #will be a limitation later
		path_lengths = self.__path_lengths__(self.data[:,ind])[1:]
		for i in range(len(path_lengths)-1):
			self.__path__(self.data[path_lengths[i]:path_lengths[i+1],1:4],self.data[path_lengths[i],ind])
			self.path_radii[self.data[path_lengths[i],ind]] = self.data[path_lengths[i]:path_lengths[i+1],4] #the radius index is not always garunteed to be in column 4

	def __contour_subfunction__(self,path_object,slice_index,radius):  #PASSING
		from sv import Contour,GUI
		import numpy as np 
		Contour.SetContourKernel('Circle')
		c = Contour.pyContour()
		c.NewObject('C_'+path_object+'_'+str(slice_index),path_object,slice_index)

		c.SetCtrlPtsByRadius(self.data_manager['Full_Paths'][path_object][int(slice_index)],radius) #change later
		c.Create()
		self.data_manager['Contours'].append('C_'+path_object+'_'+str(slice_index))
		self.data_manager['Path_Contours'][path_object].append('C_'+path_object+'_'+str(slice_index))
		c.GetPolyData('C_'+path_object+'_'+str(slice_index)+'p')
		self.data_manager['PolyData'].append('C_'+path_object+'_'+str(slice_index)+'p')
		self.data_manager['Path_PolyData'][path_object].append('C_'+path_object+'_'+str(slice_index)+'p')
		return 'C_'+path_object+'_'+str(slice_index)

	def __contour_path__(self,path_object,slices=None): #PASSING
		from sv import GUI,Path
		path_contour_list = []
		if slices==None:
			r = self.path_radii[path_object]
			slices = len(r)
			p = Path.pyPath()
			p.GetObject(path_object)
			slice_index = []
			object_path = p.GetPathPosPts()
			self.data_manager['Full_Paths'][path_object] = object_path
			for path_point in self.data_manager['Path_Points'][path_object]:
				slice_index.append(object_path.index(path_point))
		else:
			#will require interpolation
			pass 
		print(slice_index)
		for i in range(slices):
			path_contour_list.append(self.__contour_subfunction__(path_object,slice_index[i],float(r[i])))
		if self.GUI == True:
			GUI.ImportContoursFromRepos('Contours_'+path_object,path_contour_list,path_object,'Segmentations')
		return 


	def contour(self):  #PASSING 
		for path_object in self.data_manager['Paths']:
			self.data_manager['Path_Contours'][path_object] = []
			self.data_manager['Path_PolyData'][path_object] = []
			self.data_manager['Full_Paths'][path_object] = None 
			self.__contour_path__(path_object)		
		pass


	def __geometry__(self,path_object,spline=True,NumSegs=60): #PASSING
		from sv import Geom,GUI,Solid
		import math
		for PolyData in self.data_manager['Path_PolyData'][path_object]:
			Geom.SampleLoop(PolyData,NumSegs,PolyData+'s')
			self.data_manager['Path_SampleData'][path_object].append(PolyData+'s')

		for index in range(len(self.data_manager['Path_PolyData'][path_object])-1):
			if index == 0:
				Geom.AlignProfile(self.data_manager['Path_SampleData'][path_object][index],self.data_manager['Path_SampleData'][path_object][index+1],path_object+'alignment'+str(index),0)
				self.data_manager['Path_AlignedData'][path_object].append(self.data_manager['Path_SampleData'][path_object][index])
				self.data_manager['Path_AlignedData'][path_object].append(path_object+'alignment'+str(index))
			else:
				Geom.AlignProfile(self.data_manager['Path_AlignedData'][path_object][index],self.data_manager['Path_SampleData'][path_object][index+1],path_object+'alignment'+str(index),0)
				self.data_manager['Path_AlignedData'][path_object].append(path_object+'alignment'+str(index))
		for profile in self.data_manager['Path_AlignedData'][path_object]:
			self.data_manager['Path_AlignedData_Sampled'][path_object].append(Geom.SampleLoop(profile,NumSegs,profile+'_sampled'))
		if spline == True:
			Geom.LoftSolid(self.data_manager['Path_AlignedData_Sampled'][path_object],path_object+'_loft',60,120,100,20,0,1)
		else:
			pass #will have nurbs lofting later 
		if self.GUI == True:
			pass
		#	GUI.ImportPolyDataFromRepos(path_object+'_loft','Models') #something is wrong with the lofting 
		else:
			pass
		return 

	def loft(self):	#PASSING
		for path_object in self.data_manager['Paths']:
			self.data_manager['Path_SampleData'][path_object] = []
			self.data_manager['Path_Lofts'][path_object] = []
			self.data_manager['Path_AlignedData'][path_object] = []
			self.data_manager['Path_AlignedData_Sampled'][path_object] = []
			self.__geometry__(path_object)
		return 

	def __solid_subprocess__(self,path_object): #PASSING
		from sv import Solid,Repository,VMTKUtils
		Solid.SetKernel('PolyData')
		solid = Solid.pySolidModel()
		solid.NewObject(path_object+'_solid')
		VMTKUtils.Cap_with_ids(path_object+'_loft',path_object+'_capped',0,0)
		solid.SetVtkPolyData(path_object+'_capped')
		# solid.CapSurfToSolid(path_object+'_capped',path_object+'_correct')
		self.data_manager['Solids'].append(path_object+'_capped')

	def __Union__(self): #PASSING #CPofF  ##too much in function #PASSING
		from sv import Geom,Solid,GUI,Geom,Repository
		import os 
		Solid.SetKernel('PolyData')
		Geom.All_union(self.data_manager['Solids'],0,'Model',0.00001) #len(self.data_manager['Solids'])
		print(self.data_manager['Solids'])
		s = Solid.pySolidModel()
		s.GetModel('Model')
		s.GetPolyData('Model_Polydata')
		s.GetBoundaryFaces(45)
		faceids = s.GetFaceIds()
		face_types = []
		self.wall_list = []
		for face in faceids:
			s.GetFacePolyData(face,int(face),0.1)
			face_types.append(self.__face_type__(face))
			if face_types[-1] == 'wall':
				self.wall_list.append(int(face))
			else:
				pass
		s.GetModel('Model')
		os.chdir('/home/zacharysexton/Downloads')
		s.WriteNative(os.getcwd()+'/Model_Solid.vtp')
		return 

	def garbage_union(self): # may be removed later 
		from sv import Geom,Solid,GUI,Geom,Repository
		import os 
		Solid.SetKernel('PolyData')
		s = Solid.pySolidModel()
		for solid_idx in range(len(self.data_manager['Solids'])-1):
			if solid_idx == 0:
				Geom.All_union([self.data_manager['Solids'][solid_idx],self.data_manager['Solids'][solid_idx+1]],1,'temp',0.000001)
				if len(self.data_manager['Solids']) == 2:
					break 
			elif (solid_idx != len(self.data_manager['Solids'])-1) and Repository.Exists('temp_replace')==False:
				Geom.All_union(['temp',self.data_manager['Solids'][solid_idx+1]],1,'temp_replace',0.000001)
				Repository.Delete('temp')
			elif (solid_idx != len(self.data_manager['Solids'])-1) and Repository.Exists('temp')==False:
				Geom.All_union(['temp_replace',self.data_manager['Solids'][solid_idx+1]],1,'temp',0.000001)
				Repository.Delete('temp_replace')
			else:
				if Repository.Exists('temp'):
					Geom.All_union(['temp',self.data_manager['Solids'][solid_idx+1]],1,'Model',0.000001)
				else:
					Geom.All_union(['temp_replace',self.data_manager['Solids'][solid_idx+1]],1,'Model',0.000001)
		return 


	def __subtraction__(self): #PASSING #unused
		from sv import Solid
		temp = Solid.pySolidModel()
		temp.Subtract('temp',self.data_manager['Solids'][0],self.data_manager['Solids'][1])
		return 

	def __face_type__(self,face,threshold=5): #PASSING
		from sv import Solid,Repository
		s = Solid.pySolidModel()
		s.NewObject('temp')
		s.SetVtkPolyData(face)
		s.GetBoundaryFaces(threshold)
		div = s.GetFaceIds()
		if len(div) > 1:
			face_type = 'wall'
		else:
			face_type = 'cap'
		Repository.Delete('temp')
		return face_type

	def solid(self): #PASSING #not integrated
		for path_object in self.data_manager['Paths']:
			self.__solid_subprocess__(path_object)
		pass

	def smooth(): 
		pass

	def mesh(self): #PASSING
		 from sv import MeshObject,GUI,Repository
		 import os
		 MeshObject.SetKernel('TetGen')

		 msh = MeshObject.pyMeshObject()
		 msh.NewObject('Model_mesh')

		 msh.LoadModel(os.getcwd()+'/Model_Solid.vtp')
		 msh.NewMesh()

		 msh.SetMeshOptions('SurfaceMeshFlag',[1])
		 msh.SetMeshOptions('VolumeMeshFlag',[1])
		 msh.SetMeshOptions('GlobalEdgeSize',[0.3])
		 msh.SetMeshOptions('MeshWallFirst',[1])
		 msh.SetWalls(self.wall_list)
		 msh.GenerateMesh()

		 fileName = os.getcwd()+'/Solid_Model.vtk'
		 msh.WriteMesh(fileName)
		 msh.GetUnstructuredGrid('ug')
		 Repository.WriteVtkUnstructuredGrid('ug','ascii',fileName)

		 GUI.ImportUnstructedGridFromRepos('ug')
		 # Need to write the mesh complete folder on demand for live scripts 

	def pre():
		pass
		# locate svPreSolver 

	def sim():
		pass
		# locate svSolver 

	def post():
		pass
		# locate svPostSolver

	def __format_xml__(self,xml_element): #PASSING
		from xml.etree import ElementTree
		from xml.dom import minidom

		xml_string = ElementTree.tostring(xml_element,encoding='utf8')
		reparsed_xml = minidom.parseString(xml_string)
		return reparsed_xml.toprettyxml(indent="  ")

	def Export_XML(self,faceids,face_types): #PASSING 
		from xml.etree.ElementTree import Element, SubElement, Comment, tostring
		import os 
		print('Writing XML...')
		model = Element('model')
		model.set("type","PolyData")
		timestep = SubElement(model,'timestep')
		timestep.set("id","0")
		model_element = SubElement(timestep,'model_element')
		model_element.set("type","PolyData")
		model_element.set("num_samlping","100")
		model_element.set("use_uniform","1")
		model_element.set("method","spline")
		model_element.set("sampling","60")
		model_element.set("sample_per_seg","12")        #set all attributes at once in next iteration of code
		model_element.set("use_linear_sample","1")
		model_element.set("linear_multiplier","10")
		model_element.set("use_fft","0")
		model_element.set("num_modes","20")
		model_element.set("u_degree","2")
		model_element.set("v_dergee","2")
		model_element.set("u_knot_type","derivative")
		model_element.set("v_knot_type","average")
		model_element.set("u_parametric_type","centripetal")
		model_element.set("v_parametric_type","chord")
		segmentations = SubElement(model_element,'segmentations')
		faces = SubElement(model_element,'faces')
		for i in range(len(faceids)):
			face = SubElement(faces,'face')
			face.set("id",faceids[i])
			face.set("name","Model_"+faceids[i])
			face.set("type",face_types[i])
			face.set("visible","true")
			face.set("opacity","1")
			face.set("color1","1")
			face.set("color2","1")
			face.set("color3","1")
		blend_radii = SubElement(model_element,'blend_radii')
		blend_param = SubElement(model_element,'blend_param')
		blend_param.set("blend_iters","2")
		blend_param.set("sub_blend_iters","3")
		blend_param.set("cstr_smooth_iters","2")
		blend_param.set("lap_smooth_iters","50")
		blend_param.set("subdivision_iters","1")
		blend_param.set("decimation","0.01")
		#print(tostring(model,encoding='utf8').decode('utf8')) #make optional setting
		os.chdir('/home/zacharysexton/Downloads')
		xml_file = open("Model_Solid.xml","w")
		xml_file.write(self.__format_xml__(model))
		print('Done')
		return 


	def __path_lengths__(self,path_vector): #PASSING
		temp = []
		for i in range(len(path_vector)):
			if (path_vector[i].isspace()==False and path_vector[i] != ''):
				temp.append(i)
			elif i == len(path_vector)-1:
				temp.append(i+1)
			else:
				pass 
		return temp

	def __linear_interp__(first_value,second_value,first_slice,second_slice):
		pass

	def clear(self): #PASSING #will need improvement
		from sv import Repository
		if len(Repository.List()) == 0:
			print('Repository Empty')
		else:
			for i in Repository.List():
				Repository.Delete(i)
			print('Repository Cleared')
			for key in self.data_manager.keys():
				self.data_manager[key] = []
			print('Data Manager Cleared')

	def oneDsolver(self):
		# match all coordinates
		pass 

	def connectivity(self): # WAITING
		pass


	def write1D_files(self): #BUILDING
		import time
		filename = time.asctime()+'_model.in'
		modelname = filename.replace(' ','')
		modelname = modelname.replace('.in','_Stready_RCR_')
		solver_file = open(filename,'w+')
		print('Writing 1D model...')
		solver_file.write("# =====================================\n")
		solver_file.write("# GenericPy_Steady MODEL - UNITS IN CGS\n")
		solver_file.write("# =====================================\n\n")
		solver_file.write("# ==========\n# MODEL CARD\n# ==========\n")
		solver_file.write("# - Name of the model (string)\n\n")
		solver_file.write("MODEL "+modelname+"\n\n")
		solver_file.write("# ==========\n# NODE CARD\n# ==========\n")
		solver_file.write("# - Node Name (double)\n# - Node X Coordinate \
			              (double)\n# - Node Y Coordinate (double)\n# - \
			              Node Z Coordinate (double)\n\n")
		for node in NODES:
			solver_file.write("NODE {} {} {} {}\n".format(node.id,node.x,node.y,node.z))
		solver_file.write("\n\n")
		solver_file.write("# ==========\n# JOINT CARD\n# ==========\n")
		solver_file.write("# - Joint Name (string)\n# - Joint Node \
			              (double)\n# - Joint Inlet Name (string)\n# - \
			              Joint Outlet Name (string)\n\n")
		solver_file.write("# ================================\n")
		solver_file.write("# JOINTINLET AND JOINTOUTLET CARDS\n")
		solver_file.write("# ================================\n")
		solver_file.write("# - Inlet/Outlet Name (string)\n# - Total\
		 				   Number of segments (int)\n# - List of \
		 				   segments (list of int)\n\n")

class node:
	import weakref
	_instances = set()
	def __init__(self,coordinates,unique_id):
		import weakref
		self.position = coordinates
		self.id = unique_id # integer
		self.input = {} # node id of parent
		self.output = {} # node is of daughter
		self.inlet = False
		self.outlet = False
		self._instances.add(weakref(self))
	def move():
		pass # not implemented yet
	@classmethod
	def getinstances(cls):
		set_return = set()
		for pointer in cls._instances:
			obj = pointer()
			if obj is not None:
				yield obj
			else:
				set_return.add(pointer)
			cls._instances -= set_return 
