import subprocess
import os
import shutil
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
#'cd '+os.path.join('{home}','{directory}'),
default_commands=['python setup.py bdist_wininst',lambda name: rmtree( pjoin(buildhome ,name) ),lambda name: shutil.copytree( pjoin(pjoin(home,name),'dist'), pjoin(buildhome,name) )]
ipython_commands=default_commands.copy()
ipython_commands.insert(0,'git submodule init')
ipython_commands.insert(1,'git submodule update')
modules={}
modules['pygments']={'directory':'pygments', 'tool':tools['hg'], 'url':'https://bitbucket.org/birkenfeld/pygments-main','commands':default_commands}
modules['sphinx']={'directory':'sphinx', 'tool':tools['hg'], 'url':'https://bitbucket.org/birkenfeld/sphinx','commands':default_commands}
modules['nose']={'directory':'nose', 'tool':tools['git'], 'url':'https://github.com/nose-devs/nose.git', 'commands':default_commands}
modules['pexpect']={'directory':'pexpect', 'tool':tools['git'], 'url':'https://github.com/yuzhichang/pexpect.git', 'commands':default_commands}
modules['pyzmq']={'directory':'pyzmq', 'tool':tools['git'], 'url':'https://github.com/zeromq/pyzmq.git', 'commands':default_commands}
modules['pyreadline']={'directory':'pyreadline', 'tool':tools['git'], 'url':'https://github.com/pyreadline/pyreadline.git', 'commands':default_commands}
modules['ipython']={'directory':'ipython', 'tool':tools['git'], 'url':'https://github.com/ipython/ipython.git', 'commands':ipython_commands}
modules['distribute']={'directory':'distribute', 'tool':tools['hg'], 'url':'https://bitbucket.org/tarek/distribute', 'commands':default_commands}
modules['pyparsing']={'directory':'pyparsing', 'tool':tools['svn'], 'url':'https://pyparsing.svn.sourceforge.net/svnroot/pyparsing/trunk/src', 'commands':default_commands}
modules['cython']={'directory':'cython', 'tool':tools['git'], 'url':'https://github.com/cython/cython.git', 'commands':default_commands}
modules['tornado']={'directory':'tornado', 'tool':tools['git'], 'url':'https://github.com/facebook/tornado.git', 'commands':default_commands}
#modules['pycares']={'directory':'pycares', 'tool':tools['git'], 'url':'https://github.com/saghul/pycares.git', 'commands':default_commands}
modules['paramiko']={'directory':'paramiko', 'tool':tools['git'], 'url':'https://github.com/paramiko/paramiko.git', 'commands':default_commands}
modules['WMI']={'directory':'WMI', 'tool':tools['svn'], 'url':'http://svn.timgolden.me.uk/wmi/trunk/', 'commands':default_commands}
#modules['']={'directory':'', 'tool':tools[''], 'url':'', 'commands':default_commands}

for module in modules:
    wm=modules[module]
    modules[module]['tool']=wm['tool'].format(url=wm['url'],path=pjoin(home,wm['directory']) ) 
    
results={}
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
            print('ok')
            results[module][command]=subprocess.check_output( command )
        else:
            command(module)
