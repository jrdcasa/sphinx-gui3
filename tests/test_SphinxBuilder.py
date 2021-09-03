import add_tebe_to_sys_path
from example_sphinx_dir_content_path import example_sphinx_dir_content_path

from src.pycore.Content import Content
from src.pycore.SphinxBuilder import SphinxBuilder

Content = Content()
SphinxBuilder = SphinxBuilder()
SphinxBuilder.assign_content_object(Content)


print(SphinxBuilder.tmp_html_dir)
print(SphinxBuilder.tmp_html_dir)

Content.set_source_dir(example_sphinx_dir_content_path)

print(SphinxBuilder.get_available_themes())

#SphinxBuilder.build_html()
SphinxBuilder.build_pdf()