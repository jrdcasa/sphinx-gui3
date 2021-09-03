import os
import add_tebe_to_sys_path
from example_sphinx_dir_content_path import example_sphinx_dir_content_path

from src.pycore.Content import Content
from src.pycore.Rst2PdfBuilder import Rst2PdfBuilder

Rst2PdfBuilder = Rst2PdfBuilder()

source_rst_filname_path = os.path.join(example_sphinx_dir_content_path, 'features.rst')
out_pdf_filname_path = os.path.join(example_sphinx_dir_content_path, 'features.pdf')

Rst2PdfBuilder.build_pdf_from_rst_file(source_rst_filname_path, out_pdf_filname_path)