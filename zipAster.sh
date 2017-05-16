#!/bin/bash

echo 'deleting AsterAnalytics child folder'
rm -rf AsterAnalytics

echo 'deleting AsterAnalytics.zip'
rm AsterAnalytics.zip

echo 'creating AsterAnalytics child directory'
mkdir AsterAnalytics

echo 'copying custom-recipes into AsterAnalytics'
cp -R custom-recipes AsterAnalytics/ 

echo 'copying js into AsterAnalytics'
cp -R js AsterAnalytics/

echo 'copying python-lib into AsterAnalytics'
cp -R python-lib AsterAnalytics/

echo 'copying resource into AsterAnalytics'
cp -R resource AsterAnalytics/

echo 'copying plugin.json into AsterAnalytics'
cp plugin.json AsterAnalytics/

echo 'zipping AsterAnalytics'
"C:\Program Files\WinRAR\WinRar.exe" a -ep1 -r "AsterAnalytics.zip" "AsterAnalytics"
