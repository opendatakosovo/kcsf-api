
from os.path import os


# Allowed file to upload 
def allowedFiles():
	return ('text/csv', 'text/x-csv')

# Rename and upload files, throw exceptions if it fails to do that
def getFileName(filePath, prefix, dir):
	try:
		if filePath.filename != '':
			dataFileName = 'cso-'+ prefix + '.' + filePath.filename.split('.')[len(filePath.filename.split('.')) - 1]
			filePath.save(os.path.join(dir, dataFileName))
			return dataFileName
	except Exception as e:
		raise Exception("File path is not set")

	