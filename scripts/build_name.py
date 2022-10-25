import os

branch_name = os.getenv('BUILD_SOURCEBRANCHNAME')

package_name = "ansible_venafi_plugin"
if branch_name != 'master':
    package_name = '%s-%s' % (package_name, branch_name)

# need to update dashes to comply with python convention
package_name = package_name.replace('-','_')

# return custom 
print ("Building package with packageName=%s" % package_name)
print ("##vso[task.setvariable variable=packageName;isOutput=true]%s" % package_name)
