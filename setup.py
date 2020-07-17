import io
import setuptools

with io.open("README.md", mode='r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="jk-sgp-lib", 
    version="1.6.1",
    author="kami1983",
    author_email="kami@cancanyou.com",
    description="Make Scrapy easier and more versatile.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kami1983/jk_sgp_lib",
    packages=setuptools.find_packages(),
    classifiers=[],
    install_requires=['scrapy', 'simplejson', 'pytz', 'pymysql', 'datetime', 'qcloudsms_py'],
    python_requires='>=2.7',
)