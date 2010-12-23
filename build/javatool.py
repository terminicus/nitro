import os
import Options, Build
from Configure import ConfigurationError


def set_options(opt):
    opt.tool_options('javaw')
    opt.add_option('--disable-java', action='store_false', dest='java',
                   help='Disable java (default)', default=True)
    opt.add_option('--with-java-home', action='store', dest='java_home',
                   help='Specify the location of the java home')
    opt.add_option('--require-java', action='store_true', dest='force_java',
               help='Require Java lib/headers (configure option)', default=False)
    

def detect(self):
    if not Options.options.java:
        return
    
    from build import recursiveGlob
    
    if Options.options.java_home:
        self.environ['JAVA_HOME'] = Options.options.java_home 
    
    """
    Check for jni headers and libraries

    On success the environment variable xxx_JAVA is added for uselib
    """
    
    try:
        self.check_tool('javaw')
    except Exception, e:
        if Options.options.force_java:
            raise e
        else:
            return

    if not self.env.CC_NAME and not self.env.CXX_NAME:
        self.fatal('load a compiler first (gcc, g++, ..)')

    try:
        
    
        if not self.env.JAVA_HOME:
            self.fatal('set JAVA_HOME in the system environment')
    
        # jni requires the jvm
        javaHome = self.env['JAVA_HOME'][0]
    
        b = Build.BuildContext()
        b.load_dirs(self.srcdir, self.blddir)
        incDir = b.root.find_dir(javaHome + '/include')
        if not incDir:
            self.fatal('could not find include directory in %r (see config.log)' % javaHome)
        
        incDirs = map(lambda x: os.path.dirname(x),
                      recursiveGlob(incDir.abspath(), ['jni.h', 'jni_md.h']))
    #    f = incDir.ant_glob('**/(jni|jni_md).h', flat=False)
    #    incDirs = [x.parent.abspath() for x in f]
    
        homeDir = b.root.find_dir(javaHome)
        if not homeDir:
            self.fatal('could not find JAVA_HOME directory %r (see config.log)' % javaHome)
        libDirs = map(lambda x: os.path.dirname(x),
                      recursiveGlob(homeDir.abspath(), ['*jvm.so', '*jvm.lib', '*jvm.dll']))
    #    f = homeDir.ant_glob('**/*jvm.(so|dll)', flat=False)
    #    libDirs = [x.parent.abspath() for x in f] or [javaHome]
    
        for i, d in enumerate(libDirs):
            if self.check(header_name='jni.h', define_name='HAVE_JNI_H', lib='jvm',
                    libpath=[d], includes=incDirs, uselib_store='JAVA', uselib='JAVA'):
                break
        else:
            self.fatal('could not find lib jvm in %r (see config.log)' % libDirs)
    except ConfigurationError, ex:
        err = str(ex).strip()
        if err.startswith('error: '):
            err = err[7:]
        if Options.options.force_java:
            self.fatal(err)
        else:
            self.check_message_custom('Java', 'lib/headers', err, color='YELLOW')
