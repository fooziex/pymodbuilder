import subprocess
import os,sys
from os.path import join as pjoin
from os import chdir, rmdir, mkdir
import platform
import shutil
from time import sleep
import copy

def rmtree(path,ignore_errors=False):
    if os.path.isdir(path):
        shutil.rmtree(path,ignore_errors=ignore_errors)

build=[]
#build=['pandas']

dontbuild=[]

PROXY=False

home = r'c:\home\build\python'
buildhome = pjoin(home, 'ball')
tools = dict()
tools['hg'] = r'hg clone -y -q {url} {path}'
tools['git'] = r'git clone -q {url} {path}'
tools['svn'] = 'svn co -q --non-interactive --trust-server-cert {url} {path}'
tools['bzr'] = 'bzr branch {url} {path}'
os.environ.putenv('VSPYCOMNTOOLS', 'C:\\Program Files (x86)\\Microsoft Visual Studio 12.0\\Common7\Tools\\')
if PROXY:
    os.environ.putenv('HTTP_PROXY', 'http://localhost:8080')
    os.environ.putenv('HTTPS_PROXY', 'http://localhost:8080')
    subprocess.check_call('proxies-on.bat Q')
else:
    os.environ.putenv('HTTP_PROXY', '')
    os.environ.putenv('HTTPS_PROXY', '')
    os.environ.unsetenv('HTTP_PROXY')
    os.environ.unsetenv('HTTPS_PROXY')
    subprocess.check_call('proxies-off.bat Q')


pyver = str(sys.version_info[0])

default_commands=[
                  'python setup.py bdist_wininst',
                  lambda name: rmtree( pjoin(buildhome, name) ),
                  lambda name: sleep(1),
                  lambda name: shutil.copytree(  pjoin( home,name,'dist'), pjoin(buildhome,name) ),
                  lambda nada: chdir(home),
                  lambda name: rmtree( pjoin(home, name,'.git'), ignore_errors=True ),
                  lambda name: rmtree( pjoin(home, name), ignore_errors=True )
                 ]
ipaddr_commands = copy.copy(default_commands)
ipaddr_commands.pop(0)
ipython_commands = copy.copy(default_commands)
ipython_commands.insert(0, 'python trunk/setup.py bdist_wininst')
ipython_commands = copy.copy(default_commands)
ipython_commands.insert(0, 'git submodule init')
ipython_commands.insert(1, 'git submodule update')
regex_commands = copy.copy(default_commands)
regex_commands.pop(0)
regex_commands.insert(0, lambda name: shutil.copytree(pjoin(home, name, 'docs'), pjoin(home, name, 'PyPI', 'docs')))
regex_commands.insert(1, lambda name: shutil.copytree(pjoin(home, name, 'regex_' + pyver, 'Python'),
                                                      pjoin(home, name, 'Python' + pyver)))
regex_files = (
'_regex.c', '_regex.h', '_regex_unicode.c', '_regex_unicode.h')  # whyyy? write a copy directory function with walk()
regex_copy = lambda name, filename: shutil.copyfile(pjoin(home, name, 'regex_' + pyver, 'regex', filename),
                                                    pjoin(home, name, 'Python' + pyver, filename))
regex_commands.insert((1 - len(default_commands)), lambda name: regex_copy(name, '_regex.c'))
regex_commands.insert((1 - len(default_commands)), lambda name: regex_copy(name, '_regex.h'))
regex_commands.insert((1 - len(default_commands)), lambda name: regex_copy(name, '_regex_unicode.c'))
regex_commands.insert((1 - len(default_commands)), lambda name: regex_copy(name, '_regex_unicode.h'))
regex_commands.insert((1 - len(default_commands)), 'python PyPI\setup.py bdist_wininst')
pywin32_commands = copy.copy(default_commands)
if pyver == '3':
    pywin32_commands.pop(0)
    pywin32_commands.insert(0, 'python setup3.py bdist_wininst')

modules={}
#modules['pycares']={'directory':'pycares', 'tool':tools['git'], 'url':'https://github.com/saghul/pycares.git', 'commands':default_commands}
#pycares need to build c-ares, gives trouble
#modules['matplotlib']={'directory':'matplotlib', 'tool':tools['git'], 'url':'https://github.com/matplotlib/matplotlib.git', 'commands':default_commands}
#modules['selenium']={'directory':'selenium', 'tool':tools['git'], 'url':'https://code.google.com/p/selenium/', 'commands':default_commands}
#modules['lxml']={'directory':'lxml', 'tool':tools['git'], 'url':'https://github.com/lxml/lxml.git', 'commands':default_commands}
#lxml depends on https://git.gnome.org/browse/libxml2 being built and installed
#modules['cx_Freeze']={'directory':'cx_Freeze', 'tool':tools['hg'], 'url':'https://bitbucket.org/anthony_tuininga/cx_freeze', 'commands':default_commands}
#cx_Freeze error building, cannot load manifest
#modules['pywin32']={'directory':'pywin32', 'tool':tools['hg'], 'url':'http://pywin32.hg.sourceforge.net/hgweb/pywin32', 'commands':pywin32_commands}
#pywin32, in CMD dies with a mspdbsrv.exe error. in mingw-bash and vs2013, dies after a long while complaining about the windows kits 8.0 headers, redefining bs
#modules['distribute']={'directory':'distribute', 'tool':tools['hg'], 'url':'https://bitbucket.org/tarek/distribute', 'commands':default_commands}
#distribute is obsoleted by setuptools
#modules['dynd']={'directory':'dynd', 'tool':tools['git'], 'url':'https://github.com/ContinuumIO/dynd-python.git', 'commands':default_commands}
#only build with cmake now
#modules['planet']={'directory':'planet', 'tool':tools['bzr'], 'url':'https://people.gnome.org/~jdub/bzr/planet/devel/trunk/', 'commands':default_commands}
#find repo
#modules['pyfltk']={'directory':'pyfltk', 'tool':tools['svn'], 'url':'https://svn.code.sf.net/p/pyfltk/code/trunk/pyfltk', 'commands':default_commands}
#needs fltk lib // error: package directory 'fltk' does not exist
#modules['pycurl']={'directory':'pycurl', 'tool':tools['git'], 'url':'https://github.com/pycurl/pycurl.git', 'commands':default_commands}
#needs curl lib // Please specify --curl-dir=/path/to/built/libcurl
#modules['hachoir']={'directory':'hachoir', 'tool':tools['hg'], 'url':'https://bitbucket.org/haypo/hachoir', 'commands':default_commands}
#multiple modules to build

#Py2
if( pyver == '2' ):
    modules['xlwt']={'directory':'xlwt', 'tool':tools['git'], 'url':'https://github.com/python-excel/xlwt.git', 'commands':default_commands}
    modules['pyparsing']={'directory':'pyparsing', 'tool':tools['svn'], 'url':'https://pyparsing.svn.sourceforge.net/svnroot/pyparsing/branches/pyparsing_1.5.x/src/', 'commands':default_commands}
    modules['rope']={'directory':'rope', 'tool':tools['hg'], 'url':'https://bitbucket.org/agr/rope', 'commands':default_commands}
    modules['enable']={'directory':'enable', 'tool':tools['git'], 'url':'https://github.com/enthought/enable.git', 'commands':default_commands}
    modules['chaco']={'directory':'chaco', 'tool':tools['git'], 'url':'https://github.com/enthought/chaco.git', 'commands':default_commands}
    modules['pefile']={'directory':'pefile', 'tool':tools['svn'], 'url':'http://pefile.googlecode.com/svn/trunk/', 'commands':default_commands}
    #pefile fails with   File "setup.py", line 5 \ except ImportError, excp:
    modules['configobj']={'directory':'configobj', 'tool':tools['hg'], 'url':'https://code.google.com/p/configobj/', 'commands':default_commands}
    #configobj died with except Exception, e: (^ on the ,) SyntaxError: invalid syntax
    modules['clint']={'directory':'clint', 'tool':tools['git'], 'url':'https://github.com/kennethreitz/clint.git', 'commands':default_commands}
    modules['suds']={'directory':'suds', 'tool':tools['hg'], 'url':'https://bitbucket.org/mirror/suds', 'commands':default_commands}
    #https://bitbucket.org/bernh/suds-python-3-patches/src
    modules['psphere']={'directory':'psphere', 'tool':tools['git'], 'url':'https://github.com/jkinred/psphere.git', 'commands':default_commands}
    #depends on suds
    modules['milk']={'directory':'milk', 'tool':tools['git'], 'url':'https://github.com/luispedro/milk.git', 'commands':default_commands}
    modules['logilab-common']={'directory':'logilab-common', 'tool':tools['hg'], 'url':'http://hg.logilab.org/review/logilab/common/', 'commands':default_commands}
    #dies on 2to3
    modules['isbntools']={'directory':'isbntools', 'tool':tools['git'], 'url':'https://github.com/xlcnd/isbntools.git', 'commands':default_commands}
    #needs 2to3
    modules['val']={'directory':'val', 'tool':tools['git'], 'url':'https://github.com/thisfred/val.git', 'commands':default_commands}
    #needs 2to3
    modules['pycerberus']={'directory':'pycerberus', 'tool':tools['hg'], 'url':'http://www.schwarz.eu/opensource/hg/pycerberus', 'commands':default_commands}
    #dies on 2to3 i think

#Py3
if( pyver == '3' ):
    modules['pyparsing']={'directory':'pyparsing', 'tool':tools['svn'], 'url':'https://pyparsing.svn.sourceforge.net/svnroot/pyparsing/trunk/src/', 'commands':default_commands}
    modules['rope']={'directory':'rope', 'tool':tools['hg'], 'url':'https://bitbucket.org/zjes/rope_py3k', 'commands':default_commands}

if( os.name == 'posix' ):
    modules['termbox']={'directory':'termbox', 'tool':tools['git'], 'url':'https://github.com/nsf/termbox.git', 'commands':default_commands}
    modules['psh']={'directory':'psh', 'tool':tools['git'], 'url':'https://github.com/KonishchevDmitry/psh.git', 'commands':default_commands}
    modules['PySecure']={'directory':'PySecure', 'tool':tools['git'], 'url':'https://github.com/dsoprea/PySecure.git', 'commands':default_commands}


modules['docutils']={'directory':'docutils', 'tool':tools['svn'], 'url':'http://svn.code.sf.net/p/docutils/code/trunk/docutils', 'commands':default_commands}
modules['WMI']={'directory':'WMI', 'tool':tools['svn'], 'url':'http://svn.timgolden.me.uk/wmi/trunk/', 'commands':default_commands}
modules['stagger']={'directory':'stagger', 'tool':tools['svn'], 'url':'http://stagger.googlecode.com/svn/trunk/', 'commands':default_commands}
modules['pyzmq']={'directory':'pyzmq', 'tool':tools['git'], 'url':'https://github.com/zeromq/pyzmq.git', 'commands':default_commands}
modules['pygments']={'directory':'pygments', 'tool':tools['hg'], 'url':'https://bitbucket.org/birkenfeld/pygments-main','commands':default_commands}
modules['sphinx']={'directory':'sphinx', 'tool':tools['hg'], 'url':'https://bitbucket.org/birkenfeld/sphinx','commands':default_commands}
modules['nose']={'directory':'nose', 'tool':tools['git'], 'url':'https://github.com/nose-devs/nose.git', 'commands':default_commands}
#modules['pexpect']={'directory':'pexpect', 'tool':tools['git'], 'url':'https://github.com/pexpect/pexpect.git', 'commands':default_commands}
modules['pexpect']={'directory':'pexpect', 'tool':tools['git'], 'url':'https://github.com/yuzhichang/pexpect.git', 'commands':default_commands}
modules['pyreadline']={'directory':'pyreadline', 'tool':tools['git'], 'url':'https://github.com/pyreadline/pyreadline.git', 'commands':default_commands}
modules['ipython']={'directory':'ipython', 'tool':tools['git'], 'url':'https://github.com/ipython/ipython.git', 'commands':ipython_commands}
modules['cython']={'directory':'cython', 'tool':tools['git'], 'url':'https://github.com/cython/cython.git', 'commands':default_commands}
modules['tornado']={'directory':'tornado', 'tool':tools['git'], 'url':'https://github.com/facebook/tornado.git', 'commands':default_commands}
modules['paramiko']={'directory':'paramiko', 'tool':tools['git'], 'url':'https://github.com/paramiko/paramiko.git', 'commands':default_commands}
modules['regex']={'directory':'regex', 'tool':tools['hg'], 'url':'https://code.google.com/p/mrab-regex-hg/', 'commands':regex_commands}
modules['pylockfile']={'directory':'pylockfile', 'tool':tools['git'], 'url':'https://github.com/smontanaro/pylockfile.git', 'commands':default_commands}
modules['django']={'directory':'django', 'tool':tools['git'], 'url':'https://github.com/django/django.git', 'commands':default_commands}
modules['django-bootstrap']={'directory':'django-bootstrap', 'tool':tools['git'], 'url':'https://github.com/dyve/django-bootstrap-toolkit.git', 'commands':default_commands}
modules['numexpr']={'directory':'numexpr', 'tool':tools['git'], 'url':'https://github.com/pydata/numexpr.git', 'commands':default_commands}
modules['bottleneck']={'directory':'bottleneck', 'tool':tools['git'], 'url':'https://github.com/kwgoodman/bottleneck.git', 'commands':default_commands}
modules['xlrd']={'directory':'xlrd', 'tool':tools['git'], 'url':'https://github.com/python-excel/xlrd.git', 'commands':default_commands}
modules['openpyxl']={'directory':'openpyxl', 'tool':tools['hg'], 'url':'https://bitbucket.org/ericgazoni/openpyxl', 'commands':default_commands}
modules['requests']={'directory':'requests', 'tool':tools['git'], 'url':'https://github.com/kennethreitz/requests.git', 'commands':default_commands}
modules['docopt']={'directory':'docopt', 'tool':tools['git'], 'url':'https://github.com/docopt/docopt.git', 'commands':default_commands}
modules['schema']={'directory':'schema', 'tool':tools['git'], 'url':'https://github.com/halst/schema.git', 'commands':default_commands}
modules['html5lib']={'directory':'html5lib', 'tool':tools['git'], 'url':'https://github.com/html5lib/html5lib-python.git', 'commands':default_commands}
modules['sqlalchemy']={'directory':'sqlalchemy', 'tool':tools['git'], 'url':'https://github.com/zzzeek/sqlalchemy.git', 'commands':default_commands}
modules['jinja2']={'directory':'jinja2', 'tool':tools['git'], 'url':'https://github.com/mitsuhiko/jinja2.git', 'commands':default_commands}
modules['markupsafe']={'directory':'markupsafe', 'tool':tools['git'], 'url':'https://github.com/mitsuhiko/markupsafe.git', 'commands':default_commands}
modules['pip']={'directory':'pip', 'tool':tools['git'], 'url':'https://github.com/pypa/pip.git', 'commands':default_commands}
modules['mako']={'directory':'mako', 'tool':tools['git'], 'url':'http://git.makotemplates.org/mako.git', 'commands':default_commands}
modules['meta']={'directory':'meta', 'tool':tools['git'], 'url':'https://github.com/srossross/Meta.git', 'commands':default_commands}
modules['virtualenv']={'directory':'virtualenv', 'tool':tools['git'], 'url':'https://github.com/pypa/virtualenv.git', 'commands':default_commands}
modules['dateutil']={'directory':'dateutil', 'tool':tools['bzr'], 'url':'lp:dateutil', 'commands':default_commands}
modules['pyramid']={'directory':'pyramid', 'tool':tools['git'], 'url':'https://github.com/Pylons/pyramid.git', 'commands':default_commands}
modules['sqlsoup']={'directory':'sqlsoup', 'tool':tools['hg'], 'url':'https://bitbucket.org/zzzeek/sqlsoup', 'commands':default_commands}
modules['pathlib']={'directory':'pathlib', 'tool':tools['hg'], 'url':'https://bitbucket.org/pitrou/pathlib', 'commands':default_commands}
modules['pyrasite']={'directory':'pyrasite', 'tool':tools['git'], 'url':'https://github.com/lmacken/pyrasite.git', 'commands':default_commands}
modules['pyrasite-gui']={'directory':'pyrasite-gui', 'tool':tools['git'], 'url':'https://github.com/lmacken/pyrasite-gui.git', 'commands':default_commands}
modules['iep']={'directory':'iep', 'tool':tools['hg'], 'url':'https://bitbucket.org/iep-project/iep', 'commands':default_commands}
modules['pyzolib']={'directory':'pyzolib', 'tool':tools['hg'], 'url':'https://bitbucket.org/pyzo/pyzolib', 'commands':default_commands}
modules['httplib2']={'directory':'httplib2', 'tool':tools['git'], 'url':'https://github.com/jcgregorio/httplib2.git', 'commands':default_commands}
modules['psh']={'directory':'psh', 'tool':tools['git'], 'url':'https://github.com/KonishchevDmitry/psh.git', 'commands':default_commands}
modules['guidata']={'directory':'guidata', 'tool':tools['hg'], 'url':'https://code.google.com/p/guidata/', 'commands':default_commands}
modules['guiqwt']={'directory':'guiqwt', 'tool':tools['hg'], 'url':'https://code.google.com/p/guiqwt/', 'commands':default_commands}
modules['formlayout']={'directory':'formlayout', 'tool':tools['hg'], 'url':'https://code.google.com/p/formlayout/', 'commands':default_commands}
modules['spyder']={'directory':'spyder', 'tool':tools['hg'], 'url':'https://code.google.com/p/spyderlib/', 'commands':default_commands}
modules['greenlet']={'directory':'greenlet', 'tool':tools['git'], 'url':'https://github.com/python-greenlet/greenlet.git', 'commands':default_commands}
modules['netaddr']={'directory':'netaddr', 'tool':tools['git'], 'url':'https://github.com/drkjam/netaddr.git', 'commands':default_commands}
modules['setuptools']={'directory':'setuptools', 'tool':tools['hg'], 'url':'https://bitbucket.org/pypa/setuptools', 'commands':default_commands}
modules['simplejson']={'directory':'simplejson', 'tool':tools['git'], 'url':'https://github.com/simplejson/simplejson.git', 'commands':default_commands}
modules['urwid']={'directory':'urwid', 'tool':tools['git'], 'url':'https://github.com/wardi/urwid.git', 'commands':default_commands}
modules['venusian']={'directory':'venusian', 'tool':tools['git'], 'url':'https://github.com/Pylons/venusian.git', 'commands':default_commands}
modules['webob']={'directory':'webob', 'tool':tools['git'], 'url':'https://github.com/Pylons/webob.git', 'commands':default_commands}
modules['repoze.lru']={'directory':'repoze.lru', 'tool':tools['git'], 'url':'https://github.com/repoze/repoze.lru.git', 'commands':default_commands}
modules['translationstring']={'directory':'translationstring', 'tool':tools['git'], 'url':'https://github.com/Pylons/translationstring.git', 'commands':default_commands}
modules['flask']={'directory':'flask', 'tool':tools['git'], 'url':'https://github.com/mitsuhiko/flask.git', 'commands':default_commands}
modules['werkzeug']={'directory':'werkzeug', 'tool':tools['git'], 'url':'https://github.com/mitsuhiko/werkzeug.git', 'commands':default_commands}
modules['itsdangerous']={'directory':'itsdangerous', 'tool':tools['git'], 'url':'https://github.com/mitsuhiko/itsdangerous.git', 'commands':default_commands}
modules['flask-sqlalchemy']={'directory':'flask-sqlalchemy', 'tool':tools['git'], 'url':'https://github.com/mitsuhiko/flask-sqlalchemy.git', 'commands':default_commands}
modules['logbook']={'directory':'logbook', 'tool':tools['git'], 'url':'https://github.com/mitsuhiko/logbook.git', 'commands':default_commands}
modules['webtest']={'directory':'webtest', 'tool':tools['git'], 'url':'https://github.com/Pylons/webtest.git', 'commands':default_commands}
modules['hypatia']={'directory':'hypatia', 'tool':tools['git'], 'url':'https://github.com/Pylons/hypatia.git', 'commands':default_commands}
modules['waitress']={'directory':'waitress', 'tool':tools['git'], 'url':'https://github.com/Pylons/waitress.git', 'commands':default_commands}
modules['pyramid_mailer']={'directory':'pyramid_mailer', 'tool':tools['git'], 'url':'https://github.com/Pylons/pyramid_mailer.git', 'commands':default_commands}
modules['colander']={'directory':'colander', 'tool':tools['git'], 'url':'https://github.com/Pylons/colander.git', 'commands':default_commands}
modules['substanced']={'directory':'substanced', 'tool':tools['git'], 'url':'https://github.com/Pylons/substanced.git', 'commands':default_commands}
modules['six']={'directory':'six', 'tool':tools['hg'], 'url':'https://bitbucket.org/gutworth/six', 'commands':default_commands}
modules['blosc']={'directory':'blosc', 'tool':tools['git'], 'url':'https://github.com/FrancescAlted/python-blosc.git', 'commands':default_commands}
modules['comtypes']={'directory':'comtypes', 'tool':tools['git'], 'url':'https://github.com/enthought/comtypes.git', 'commands':default_commands}
modules['pyhook']={'directory':'pyhook', 'tool':tools['git'], 'url':'http://git.code.sf.net/p/pyhook/code', 'commands':default_commands}
modules['yasv']={'directory':'yasv', 'tool':tools['git'], 'url':'https://github.com/vyalow/yasv.git', 'commands':default_commands}
modules['mpmath']={'directory':'mpmath', 'tool':tools['git'], 'url':'https://github.com/fredrik-johansson/mpmath.git', 'commands':default_commands}
modules['trueskill']={'directory':'trueskill', 'tool':tools['git'], 'url':'https://github.com/sublee/trueskill.git', 'commands':default_commands}
modules['logging_tree']={'directory':'logging_tree', 'tool':tools['git'], 'url':'https://github.com/brandon-rhodes/logging_tree.git', 'commands':default_commands}
modules['distlib']={'directory':'distlib', 'tool':tools['hg'], 'url':'https://bitbucket.org/pypa/distlib', 'commands':default_commands}
modules['tox']={'directory':'tox', 'tool':tools['hg'], 'url':'https://bitbucket.org/hpk42/tox', 'commands':default_commands}
modules['simple_timer']={'directory':'simple_timer', 'tool':tools['hg'], 'url':'https://bitbucket.org/barseghyanartur/timer', 'commands':default_commands}
modules['pyyaml']={'directory':'pyyaml', 'tool':tools['hg'], 'url':'https://bitbucket.org/xi/pyyaml', 'commands':default_commands}
modules['brownie']={'directory':'brownie', 'tool':tools['git'], 'url':'https://github.com/DasIch/brownie.git', 'commands':default_commands}
modules['beautifulsoup']={'directory':'beautifulsoup', 'tool':tools['bzr'], 'url':'lp:beautifulsoup', 'commands':default_commands}
modules['msgpack']={'directory':'msgpack', 'tool':tools['git'], 'url':'https://github.com/msgpack/msgpack-python.git', 'commands':default_commands}
modules['msgpack-rpc']={'directory':'msgpack-rpc', 'tool':tools['git'], 'url':'https://github.com/msgpack-rpc/msgpack-rpc-python.git', 'commands':default_commands}
modules['psutil']={'directory':'psutil', 'tool':tools['hg'], 'url':'https://code.google.com/p/psutil/', 'commands':default_commands}
modules['mahotas']={'directory':'mahotas', 'tool':tools['git'], 'url':'https://github.com/luispedro/mahotas.git', 'commands':default_commands}
modules['duckduckgo']={'directory':'duckduckgo', 'tool':tools['git'], 'url':'https://github.com/crazedpsyc/python-duckduckgo.git', 'commands':default_commands}
modules['pyvbox']={'directory':'pyvbox', 'tool':tools['git'], 'url':'https://github.com/mjdorma/pyvbox.git', 'commands':default_commands}
modules['cx_Freeze']={'directory':'cx_Freeze', 'tool':tools['hg'], 'url':'https://bitbucket.org/anthony_tuininga/cx_freeze', 'commands':default_commands}
modules['pylint']={'directory':'pylint', 'tool':tools['hg'], 'url':'https://bitbucket.org/logilab/pylint', 'commands':default_commands}
modules['blaze']={'directory':'blaze', 'tool':tools['git'], 'url':'https://github.com/ContinuumIO/blaze-core.git', 'commands':default_commands}
modules['pyflakes']={'directory':'pyflakes', 'tool':tools['bzr'], 'url':'lp:pyflakes', 'commands':default_commands}
modules['patsy']={'directory':'patsy', 'tool':tools['git'], 'url':'https://github.com/pydata/patsy.git', 'commands':default_commands}
modules['bcrypt']={'directory':'bcrypt', 'tool':tools['git'], 'url':'https://github.com/dstufft/bcrypt.git', 'commands':default_commands}
modules['django-bcrypt']={'directory':'django-bcrypt', 'tool':tools['hg'], 'url':'https://bitbucket.org/dwaiter/django-bcrypt', 'commands':default_commands}
modules['nltk']={'directory':'nltk', 'tool':tools['git'], 'url':'https://github.com/nltk/nltk.git', 'commands':default_commands}
modules['django-nvd3']={'directory':'django-nvd3', 'tool':tools['git'], 'url':'https://github.com/areski/django-nvd3.git', 'commands':default_commands}
modules['nvd3']={'directory':'nvd3', 'tool':tools['git'], 'url':'https://github.com/areski/python-nvd3.git', 'commands':default_commands}
modules['lz4']={'directory':'lz4', 'tool':tools['git'], 'url':'https://github.com/steeve/python-lz4.git', 'commands':default_commands}
modules['anyjson']={'directory':'anyjson', 'tool':tools['hg'], 'url':'https://bitbucket.org/runeh/anyjson', 'commands':default_commands}
modules['pycrypto']={'directory':'pycrypto', 'tool':tools['git'], 'url':'https://github.com/dlitz/pycrypto', 'commands':default_commands}
modules['hpilo']={'directory':'hpilo', 'tool':tools['git'], 'url':'https://github.com/seveas/python-hpilo.git', 'commands':default_commands}
modules['defusedexpat']={'directory':'defusedexpat', 'tool':tools['hg'], 'url':'https://bitbucket.org/tiran/defusedexpat', 'commands':default_commands}
modules['defusedxml']={'directory':'defusedxml', 'tool':tools['hg'], 'url':'https://bitbucket.org/tiran/defusedxml', 'commands':default_commands}
modules['xmltodict']={'directory':'xmltodict', 'tool':tools['git'], 'url':'https://github.com/martinblech/xmltodict.git', 'commands':default_commands}
modules['vmw.vco']={'directory':'vmw.vco', 'tool':tools['git'], 'url':'https://github.com/sigma/vmw.vco.git', 'commands':default_commands}
modules['py-sdl2']={'directory':'py-sdl2', 'tool':tools['hg'], 'url':'https://bitbucket.org/marcusva/py-sdl2', 'commands':default_commands}
#modules['rptlab']={'directory':'rptlab', 'tool':tools['hg'], 'url':'https://bitbucket.org/rptlab/reportlab', 'commands':default_commands}
modules['sympy']={'directory':'sympy', 'tool':tools['git'], 'url':'https://github.com/sympy/sympy.git', 'commands':default_commands}
#modules['statsmodels']={'directory':'statsmodels', 'tool':tools['git'], 'url':'git://github.com/statsmodels/statsmodels.git', 'commands':default_commands}
#modules['pyaudio']={'directory':'pyaudio', 'tool':tools['git'], 'url':'http://people.csail.mit.edu/hubert/git/pyaudio.git', 'commands':default_commands}
#modules['pytables']={'directory':'pytables', 'tool':tools['git'], 'url':'https://github.com/PyTables/PyTables.git', 'commands':default_commands}
#modules['llvmmath']={'directory':'llvmmath', 'tool':tools['git'], 'url':'https://github.com/ContinuumIO/llvmmath.git', 'commands':default_commands}
#modules['llvmpy']={'directory':'llvmpy', 'tool':tools['git'], 'url':'https://github.com/llvmpy/llvmpy.git', 'commands':default_commands}
#modules['pyopencl']={'directory':'pyopencl', 'tool':tools['git'], 'url':'https://github.com/pyopencl/pyopencl.git', 'commands':default_commands}
#modules['enaml']={'directory':'enaml', 'tool':tools['git'], 'url':'https://github.com/nucleic/enaml.git', 'commands':default_commands}
#modules['atom']={'directory':'atom', 'tool':tools['git'], 'url':'https://github.com/nucleic/atom.git', 'commands':default_commands}
modules['hpOneView']={'directory':'hpOneView', 'tool':tools['git'], 'url':'https://github.com/HewlettPackard/python-hpOneView.git', 'commands':default_commands}
modules['pyglet']={'directory':'pyglet', 'tool':tools['hg'], 'url':'https://code.google.com/p/pyglet/', 'commands':default_commands}
modules['pyvbox']={'directory':'pyvbox', 'tool':tools['git'], 'url':'https://github.com/mjdorma/pyvbox.git', 'commands':default_commands}
modules['pep8']={'directory':'pep8', 'tool':tools['git'], 'url':'https://github.com/jcrocholl/pep8.git', 'commands':default_commands}
modules['astroid']={'directory':'astroid', 'tool':tools['hg'], 'url':'https://bitbucket.org/logilab/astroid', 'commands':default_commands}
modules['pycares']={'directory':'pycares', 'tool':tools['git'], 'url':'https://github.com/saghul/pycares.git', 'commands':default_commands}
modules['flake8']={'directory':'flake8', 'tool':tools['hg'], 'url':'https://bitbucket.org/tarek/flake8', 'commands':default_commands}
modules['mccabe']={'directory':'mccabe', 'tool':tools['git'], 'url':'https://github.com/flintwork/mccabe.git', 'commands':default_commands}
modules['isbn_hyphenate']={'directory':'isbn_hyphenate', 'tool':tools['git'], 'url':'https://github.com/TorKlingberg/isbn_hyphenate.git', 'commands':default_commands}
modules['isbnid']={'directory':'isbnid', 'tool':tools['git'], 'url':'https://code.google.com/p/isbnid/', 'commands':default_commands}
modules['pyisbn']={'directory':'pyisbn', 'tool':tools['git'], 'url':'https://github.com/JNRowe/pyisbn.git', 'commands':default_commands}
modules['cosmic']={'directory':'cosmic', 'tool':tools['git'], 'url':'https://github.com/cosmic-api/cosmic.py.git', 'commands':default_commands}
modules['teleport']={'directory':'teleport', 'tool':tools['git'], 'url':'https://github.com/cosmic-api/teleport.py.git', 'commands':default_commands}
#modules['pyormish']={'directory':'pyormish', 'tool':tools['git'], 'url':'https://github.com/webgovernor/pyormish.git', 'commands':default_commands}
modules['jsonobject']={'directory':'jsonobject', 'tool':tools['git'], 'url':'https://github.com/dannyroberts/jsonobject.git', 'commands':default_commands}
modules['cchardet']={'directory':'cchardet', 'tool':tools['git'], 'url':'https://github.com/PyYoshi/cChardet.git', 'commands':default_commands}
modules['py']={'directory':'py', 'tool':tools['hg'], 'url':'https://bitbucket.org/hpk42/py', 'commands':default_commands}
modules['iowait']={'directory':'iowait', 'tool':tools['bzr'], 'url':'lp:python-iowait', 'commands':default_commands}
modules['hyper']={'directory':'hyper', 'tool':tools['git'], 'url':'https://github.com/Lukasa/hyper.git', 'commands':default_commands}
modules['stage']={'directory':'stage', 'tool':tools['hg'], 'url':'https://bitbucket.org/lcrees/stage', 'commands':default_commands}
modules['evergreen']={'directory':'evergreen', 'tool':tools['git'], 'url':'https://github.com/saghul/evergreen.git', 'commands':default_commands}
modules['cryptacular']={'directory':'cryptacular', 'tool':tools['hg'], 'url':'https://bitbucket.org/dholth/cryptacular', 'commands':default_commands}
modules['testtools']={'directory':'testtools', 'tool':tools['git'], 'url':'https://github.com/testing-cabal/testtools.git', 'commands':default_commands}
modules['fixtures']={'directory':'fixtures', 'tool':tools['bzr'], 'url':'lp:python-fixtures', 'commands':default_commands}
modules['webargs']={'directory':'webargs', 'tool':tools['git'], 'url':'https://github.com/sloria/webargs.git', 'commands':default_commands}
modules['ftputil']={'directory':'ftputil', 'tool':tools['hg'], 'url':'http://hg.sschwarzer.net/ftputil', 'commands':default_commands}
modules['bundle']={'directory':'bundle', 'tool':tools['git'], 'url':'https://github.com/ask/bundle.git', 'commands':default_commands}
modules['htmltemplate']={'directory':'htmltemplate', 'tool':tools['hg'], 'url':'https://bitbucket.org/hhas/htmltemplate', 'commands':default_commands}
modules['ewave']={'directory':'ewave', 'tool':tools['git'], 'url':'https://github.com/melizalab/py-ewave.git', 'commands':default_commands}
modules['wsgikit']={'directory':'wsgikit', 'tool':tools['git'], 'url':'https://github.com/Mikhus/wsgikit.git', 'commands':default_commands}
#modules['pythonnet']={'directory':'pythonnet', 'tool':tools['svn'], 'url':'http://svn.code.sf.net/p/pythonnet/code/trunk/pythonnet', 'commands':default_commands}
modules['jsonschema']={'directory':'jsonschema', 'tool':tools['git'], 'url':'https://github.com/Julian/jsonschema.git', 'commands':default_commands}
modules['jsonpointer']={'directory':'jsonpointer', 'tool':tools['git'], 'url':'https://github.com/stefankoegl/python-json-pointer.git', 'commands':default_commands}
modules['click']={'directory':'click', 'tool':tools['git'], 'url':'https://github.com/mitsuhiko/click.git', 'commands':default_commands}
modules['geoip2']={'directory':'geoip2', 'tool':tools['git'], 'url':'https://github.com/maxmind/GeoIP2-python.git', 'commands':default_commands}
modules['ipython-beautifulsoup']={'directory':'ipython-beautifulsoup', 'tool':tools['git'], 'url':'https://github.com/Psycojoker/ipython-beautifulsoup.git', 'commands':default_commands}
modules['maxminddb']={'directory':'maxminddb', 'tool':tools['git'], 'url':'https://github.com/maxmind/MaxMind-DB-Reader-python.git', 'commands':default_commands}
modules['ipaddr']={'directory':'ipaddr', 'tool':tools['git'], 'url':'https://code.google.com/p/ipaddr-py/', 'commands':ipaddr_commands}
#modules['pythonpy']={'directory':'pythonpy', 'tool':tools['git'], 'url':'https://github.com/Russell91/pythonpy.git', 'commands':default_commands}
modules['conda']={'directory':'conda', 'tool':tools['git'], 'url':'https://github.com/conda/conda.git', 'commands':default_commands}
modules['slugify']={'directory':'slugify', 'tool':tools['git'], 'url':'https://github.com/zacharyvoase/slugify.git', 'commands':default_commands}


#modules['pandas']={'directory':'pandas', 'tool':tools['git'], 'url':'https://github.com/pydata/pandas.git', 'commands':default_commands}

if 'pandas' in build:
    modules = {}
    os.environ.putenv('VSPYCOMNTOOLS', 'C:\\Program Files (x86)\\Microsoft Visual Studio 11.0\\Common7\Tools\\')
    modules['pandas']={'directory':'pandas', 'tool':tools['git'], 'url':'https://github.com/pydata/pandas.git', 'commands':default_commands}


#modules['']={'directory':'', 'tool':tools[''], 'url':'', 'commands':default_commands}

for module in modules:
    wm = modules[module]
    modules[module]['tool'] = wm['tool'].format(url=wm['url'], path=pjoin(home, wm['directory']))


results = {}

build = []

dontbuild = ['bcrypt','defusedexpat','duckduckgo','ftputil','pycares','stagger','bottleneck'.'mako','pyhook','geoip2','ipaddr','pycrypto','lz4','openpyxl']

filtered = []

chdir(home)
for module in modules:
    if (build is not None and len(build) > 0) and module not in build:
        continue
    if (dontbuild is not None and len(dontbuild) > 0) and module in dontbuild and module not in build:
        continue
    wm = modules[module]
    if True in [f in wm['tool'] for f in filtered]:
        continue
    print('Building:  ' + module)
    wd = pjoin(home, wm['directory'])
    if os.path.isdir(wd):
        rmtree(pjoin(home, wm['directory']))
    try:
        subprocess.check_output(wm['tool'])
    except:
        print("Failed on " + wm['tool'])
    chdir(wd)
    results[module] = {}
    for command in wm['commands']:
        if isinstance(command, str):
            results[module][command] = subprocess.check_output(command)
        else:
            command(module)
    print('Built: ' + module)
chdir(home)
