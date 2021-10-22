echo 'crawl(){ node blacklight-collector/wrapper.js $@ ;}' >> ~/.bashrc 

echo 'inspect(){ python3 parse-inspection.py $@ ;}' >> ~/.bashrc 

echo 'export -f crawl' >> ~/.bashrc 
echo 'export -f inspect' >> ~/.bashrc 