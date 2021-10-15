# web-privacy-investigator

<h3>Running the inspection parser</h3>

#Make sure you have node.js and npm installed

#Clone the blacklight-collector repository on to your system and install

'''
npm install
npm run build
'''

#Place wrapper.js and parse-inspection.py in the blacklight-collector base directory i.e. path_you_cloned_into/blacklight-collector/

#Run wrapper.js with URLs passed in as command line arguments

'''
node wrapper.js example.com
'''

#Run the inspection parser by commandline with device and url passed in as arguments, or use later by calling parse_inspection(site, device)

'''
python3 parse_inspection.py example.com iPhone4
'''
