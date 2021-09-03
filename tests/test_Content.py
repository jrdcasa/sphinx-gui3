import add_tebe_to_sys_path
from example_sphinx_dir_content_path import example_sphinx_dir_content_path

from src.pycore.Content import Content

Content = Content()

print ('----------------Content.set_source_dir()------------------------')
print (Content.source_dir_path)
Content.set_source_dir(example_sphinx_dir_content_path)
print (Content.source_dir_path)
print ('----------------Content.conf_file_path------------------------')
print (Content.conf_file_path)
print ('----------------Content.index_file_path------------------------')
print (Content.index_file_path)
print ('----------------Content.project_name------------------------')
print (Content.project_name)
print ('----------------Content.get_markup_filenames_list()------------------------')
print (Content.get_markup_filenames_list())
print ('----------------Content.get_markup_filenames_list()------------------------')
Content.create_index_file()
