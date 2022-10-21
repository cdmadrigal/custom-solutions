# setting variables required for headless non-interactive executions of jfrog cli
export PACKAGE_NAME=$BUILD_PACKAGENAME
export BUILD_INFO_NAME=IAAS-Share-$BUILD_DEFINITIONNAME
export BUILD_NUMBER=$BUILD_BUILDNUMBER
export CI=true
python setup.py sdist bdist_wheel
