import add_tebe_to_sys_path

from src.pycore.Document import Document

Document = Document()



print ('Document.has_data - ', Document.has_data())

print ('----------------Document.file_open()------------------------')
Document.file_open('/home/lukasz/Dropbox/PYAPPS_STRUCT/SOURCE_TEBE/source/tests/example_sphinx_dir_content/new.rst')
print (Document.file_path)
print (Document.text)

print ('Document.has_data - ', Document.has_data())

print ('----------------Document.file_save()------------------------')
Document.set_new_text_content('New content')
print (Document.text)
Document.file_save()

print ('----------------Document.file_save_as()------------------------')
Document.set_new_text_content('Some content')
Document.file_save_as('/home/lukasz/Dropbox/PYAPPS_STRUCT/SOURCE_TEBE/source/tests/example_sphinx_dir_content/spam.rst')
print (Document.text)
print (Document.file_path)

print('----------------Document.file_new()------------------------')
Document.file_new('/home/lukasz/Dropbox/PYAPPS_STRUCT/SOURCE_TEBE/source/tests/example_sphinx_dir_content/new.rst')
print (Document.text)
print (Document.file_path)
print (Document.file_name)

print ('----------------Document.is_rst_file(), Document.is_md_file()------------------------')
Document.file_open('/home/lukasz/Dropbox/PYAPPS_STRUCT/SOURCE_TEBE/source/tests/example_sphinx_dir_content/new.rst')
print (Document.file_path)
print (Document.is_md_file())
print (Document.is_rst_file())
Document.file_open('/home/lukasz/Dropbox/PYAPPS_STRUCT/SOURCE_TEBE/example_rst_documentaion/opis.md')
print (Document.file_path)
print (Document.is_md_file())
print (Document.is_rst_file())

print ('----------------Document.file_name------------------------')
print (Document.file_name)

print ('Document.has_data - ', Document.has_data())

print ('----------------Document.reset()------------------------')
print (Document.reset())
print (Document.file_path, Document.text)

print ('Document.has_data - ', Document.has_data())