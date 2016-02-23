import os, shutil

pluginDir = xlPlugins
newPlugins = newPlugins
dir = newPlugins+"/plugins"
xlHome = xlHome

if (dir.replace("/plugins", '') == XlHome):

    shutil.rmtree(dir) #remove new plugins directory
    os.system("ln -s " + xlPlugins + " " + dir)  #symlink
    print "Symlinking " + dir + " to " + pluginDir +" !\n"
    print "Your update is complete!"
else:
    shutil.rmtree(dir) #remove new plugins directory
    print "Your update is complete!"