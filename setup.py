from setuptools import setup

setup  (name='auacm',
        version='0.1',
        description='Command-line interface to the Auburn ACM website',
        author='Brandon Morris',
        author_email='brandon.morris95@gmail.com',
        packages=['auacm'],
        scripts=['bin/auacm'],
        install_requires=['requests'],
        url = 'https://github.com/BrandonLMorris/auacm-cli',
        download_url = 'https://github.com/BrandonLMorris/auacm-cli/tarball/0.1',
        keywords = ['competitive', 'icpc', 'auacm', 'auburn']
        )
