import subprocess
import os
import shutil
from time import sleep
pjoin=os.path.join
chdir=os.chdir
rmdir=os.rmdir
rmtree=shutil.rmtree
mkdir=os.mkdir

def rmtree(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        
home=r'c:\home\build\python'
buildhome=pjoin(home,'build')
tools={}
tools['hg']='hg clone -y -q {url} {path}'
tools['git']='git clone -q {url} {path}' 
tools['svn']='svn co -q --non-interactive {url} {path}'
default_commands=[
                  'python setup.py bdist_wininst',
                  lambda name: rmtree( pjoin(buildhome, name) ),
                  lambda name: shutil.copytree(  pjoin( home,name,'dist'), pjoin(buildhome,name)  ),
                  lambda nada: chdir(home),
                  lambda name: rmtree_q( pjoin(home, name,'.git') ),
                  lambda name: rmtree_q( pjoin(home, name) )
                 ]
ipython_commands=default_commands.copy()
ipython_commands.insert(0,'git submodule init')
ipython_commands.insert(1,'git submodule update')
regex_commands=default_commands.copy()
regex_commands.pop(0)
regex_commands.insert(0,lambda name: shutil.copytree( pjoin(home,name,'docs'), pjoin(home,name,'PyPI','docs') ))
regex_commands.insert(1,lambda name: shutil.copytree( pjoin(home,name,'regex_3','Python'), pjoin(home,name,'Python3') ))
regex_files=('_regex.c','_regex.h','_regex_unicode.c','_regex_unicode.h') #whyyy? write a copy directory function with walk()
regex_copy=lambda name,filename: shutil.copyfile( pjoin(home,name,'regex_3','regex',filename), pjoin(home,name,'Python3',filename) )
regex_commands.insert((1-len(default_commands)), lambda name: regex_copy(name,'_regex.c') )
regex_commands.insert((1-len(default_commands)), lambda name: regex_copy(name,'_regex.h') )
regex_commands.insert((1-len(default_commands)), lambda name: regex_copy(name,'_regex_unicode.c') )
regex_commands.insert((1-len(default_commands)), lambda name: regex_copy(name,'_regex_unicode.h') )
regex_commands.insert((1-len(default_commands)),'python PyPI\setup.py bdist_wininst')

modules={}
#modules['pyzmq']={'directory':'pyzmq', 'tool':tools['git'], 'url':'https://github.com/zeromq/pyzmq.git', 'commands':default_commands}
#modules['pycares']={'directory':'pycares', 'tool':tools['git'], 'url':'https://github.com/saghul/pycares.git', 'commands':default_commands}
#these two above ^ i've gotten to build but not automated the process
modules['pygments']={'directory':'pygments', 'tool':tools['hg'], 'url':'https://bitbucket.org/birkenfeld/pygments-main','commands':default_commands}
modules['sphinx']={'directory':'sphinx', 'tool':tools['hg'], 'url':'https://bitbucket.org/birkenfeld/sphinx','commands':default_commands}
modules['nose']={'directory':'nose', 'tool':tools['git'], 'url':'https://github.com/nose-devs/nose.git', 'commands':default_commands}
modules['pexpect']={'directory':'pexpect', 'tool':tools['git'], 'url':'https://github.com/yuzhichang/pexpect.git', 'commands':default_commands}
modules['pyreadline']={'directory':'pyreadline', 'tool':tools['git'], 'url':'https://github.com/pyreadline/pyreadline.git', 'commands':default_commands}
modules['ipython']={'directory':'ipython', 'tool':tools['git'], 'url':'https://github.com/ipython/ipython.git', 'commands':ipython_commands}
modules['distribute']={'directory':'distribute', 'tool':tools['hg'], 'url':'https://bitbucket.org/tarek/distribute', 'commands':default_commands}
modules['pyparsing']={'directory':'pyparsing', 'tool':tools['svn'], 'url':'https://pyparsing.svn.sourceforge.net/svnroot/pyparsing/trunk/src', 'commands':default_commands}
modules['cython']={'directory':'cython', 'tool':tools['git'], 'url':'https://github.com/cython/cython.git', 'commands':default_commands}
modules['tornado']={'directory':'tornado', 'tool':tools['git'], 'url':'https://github.com/facebook/tornado.git', 'commands':default_commands}
modules['paramiko']={'directory':'paramiko', 'tool':tools['git'], 'url':'https://github.com/paramiko/paramiko.git', 'commands':default_commands}
modules['WMI']={'directory':'WMI', 'tool':tools['svn'], 'url':'http://svn.timgolden.me.uk/wmi/trunk/', 'commands':default_commands}
modules['regex']={'directory':'regex', 'tool':tools['hg'], 'url':'https://code.google.com/p/mrab-regex-hg/', 'commands':regex_commands}
modules['pylockfile']={'directory':'pylockfile', 'tool':tools['git'], 'url':'https://github.com/smontanaro/pylockfile.git', 'commands':default_commands}
modules['django']={'directory':'django', 'tool':tools['git'], 'url':'https://github.com/django/django.git', 'commands':default_commands}
modules['numexpr']={'directory':'numexpr', 'tool':tools['hg'], 'url':'https://code.google.com/p/numexpr/', 'commands':default_commands}
modules['bottleneck']={'directory':'bottleneck', 'tool':tools['git'], 'url':'https://github.com/kwgoodman/bottleneck.git', 'commands':default_commands}
modules['pandas']={'directory':'pandas', 'tool':tools['git'], 'url':'https://github.com/pydata/pandas.git', 'commands':default_commands}
#modules['']={'directory':'', 'tool':tools[''], 'url':'', 'commands':default_commands}


for module in modules:
    wm=modules[module]
    modules[module]['tool']=wm['tool'].format(url=wm['url'],path=pjoin(home,wm['directory']) ) 
    
results={}
chdir(home)
for module in modules:
    wm=modules[module]
    wd=pjoin(home,wm['directory'])
    if os.path.isdir(wd):
        rmtree(pjoin(home,wm['directory']))
    mkdir(wd)
    chdir(wd)
    subprocess.check_output( wm['tool'] )
    results[module]={}
    for command in wm['commands']:
        if isinstance(command,str):
            #print('ok', command)
            results[module][command]=subprocess.check_output( command )
        else:
            #print('called', command)
            command(module)
    print('Built: '+module)
