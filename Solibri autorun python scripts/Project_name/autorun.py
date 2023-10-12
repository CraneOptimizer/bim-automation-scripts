# EXAMPLE OF A TEMPLATE FOR TESTING PURPOSES. USE AT YOUR OWN DISCRETION.
# THIS VERSION IS FOR SOLIBRI AUTORUN ONLY, NO SIMPLEBIM
# FOR INSTRUCTIONS, PLEASE REFER TO SOLIBRI AUTORUN DOCUMENTATION AND 11.10.2023 SOLIBRI AUTORUN WEBINAR RECORDING
# JOONAS KOISTINEN, CRANE OPTIMIZER OY / 11.10.2023
# joonas@craneoptimizer.com

# import python libraries
import glob
import subprocess
import os
import shutil
import sys
import time

# Record the start time
start_time = time.time()

#base directories
dirpath = os.getcwd()
folderName = os.path.basename(dirpath)
smcName = "{0}_federated model".format(folderName)

# directories for original ifc files
ARCifcFiles = dirpath +'\\ifc-original\\architectural\\*.ifc'
STRifcFiles = dirpath +'\\ifc-original\\structural\\*.ifc'
MEPifcFiles = dirpath +'\\ifc-original\\mep\\*.ifc'

# other paths
autorun = dirpath +'\\autorun.xml'
solibriModel = dirpath +'\\smc\\'+ smcName +'.smc'
classifications = dirpath +'\\classifications\\*.classification'
itos = dirpath + '\\ito\\*.ito'

# write to xml batch file
with open(autorun, 'w') as xml:
	print("-write xml file for Solibri Autorun")
	print("-----------------")
	#headers
	xml.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
	xml.write('<batch name="Simple Batch" default="root">\n')
	xml.write('<target name="root">\n')

	#check if smc already created
	if os.path.exists(solibriModel):
		#open existing smc
		xml.write('  <openmodel file="' + solibriModel + '"/>\n')
		
		#update models
		for file in glob.glob(ARCifcFiles):
			xml.write('  <updatemodel file="' + file + '" with="' + file + '"/>\n')

		for file in glob.glob(STRifcFiles):
			xml.write('  <updatemodel file="' + file + '" with="' + file + '"/>\n')

		for file in glob.glob(MEPifcFiles):
			xml.write('  <updatemodel file="' + file + '" with="' + file + '"/>\n')
			
		for file in glob.glob(classifications):
			xml.write('  <openclassification file="' + file + '"/>\n')

		for file in glob.glob(itos):
			xml.write('  <openito file="' + file + '" />\n')
		
	else:
		# if no existing smc, open new models, ITO, classifications etc
		for file in glob.glob(ARCifcFiles):
			xml.write('  <openmodel file="' + file + '" discipline="Architectural" />\n')

		for file in glob.glob(STRifcFiles):
			xml.write('  <openmodel file="' + file + '" discipline="Structural" />\n')
		
		for file in glob.glob(MEPifcFiles):
			xml.write('  <openmodel file="' + file + '" discipline="Building Services" />\n')
			
			
		for file in glob.glob(classifications):
			xml.write('  <openclassification file="' + file + '"/>\n')

		for file in glob.glob(itos):
			xml.write('  <openito file="' + file + '" />\n')
		

# 	#other actions
	xml.write('  <takeoff />\n')
	xml.write('  <itoreport file="'+ dirpath +'\\ito-reports\\ITO-report.xlsx" />\n')
	xml.write('  <savemodel file="'+ solibriModel +'" />\n')
	xml.write('  <closemodel />\n')
	xml.write('  <exit />\n')
	xml.write('</target>\n')
	xml.write('</batch>\n')

print('INFO: Autorun file is ready: ' + autorun)
print()
print("-----------------")
with open(autorun, 'r') as xml:
    print(xml.read())

#command to run solibri with autorun file
subprocess.call(['C:\\Program Files\\Solibri\\SOLIBRI\\Solibri.exe', autorun])

print("--Automation ended--")
# Record the end time
end_time = time.time()
# Calculate the elapsed time
elapsed_time = end_time - start_time
# Convert elapsed time to hours, minutes, and seconds
hours, remainder = divmod(elapsed_time, 3600)
minutes, seconds = divmod(remainder, 60)
print(f"Total processing time: {int(hours)}:{int(minutes)}.{int(seconds)}")
sys.exit()