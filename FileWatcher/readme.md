nssm link https://nssm.cc/download
//alternative 2 use nssm-2.24-101-g897c7ad\nssm-2.24-101-g897c7ad\win64 


1 - nssm.exe install "ServiceName" "..pythonpath\venv\Scripts\python.exe" "...filepath\WatcherService.py"

1.e - nssm.exe install "BuroStatik" "C:\Projeler\PythonP\BuroEtabs\venv\Scripts\python.exe" "C:\Projeler\PythonP\BuroEtabs\FileWatcher\WatcherService.py"

**For edit with GUI
2 - nssm.exe edit "Rufai"


**for set Info log file path set
3 - nssm.exe set "Rufai" AppStdout "C:\Projeler\PythonP\BuroEtabs\FileWatcher\WatcherServiceInfo.log"

**for set error log file
4 - nssm.exe set "Rufai" AppStderr "C:\Projeler\PythonP\BuroEtabs\FileWatcher\WatcherService.log"

**stop service
5 - nss stop "ServiceName"

**remove service
6 - nssm remove "ServiceName"