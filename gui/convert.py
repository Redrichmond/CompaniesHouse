from subprocess import call

call(['pyuic5', 'ui/main.ui', '-o', '../wMain.py'], shell=True)
call(['pyuic5', 'ui/configuration.ui', '-o', '../wConfiguration.py'], shell=True)
call(['pyuic5', 'ui/about.ui', '-o', '../wAbout.py'], shell=True)

# Resources
call(['pyrcc5', 'ui/resources/main.qrc', '-o', '../main_rc.py'], shell=True)
