
const { collector } = require("./build");
const { join } = require("path");

const URLS = []
const args = process.argv.slice(2);
for (const a of args){
    URLS.push(a);
}

const devices = [false, "iPhone 4", "iPhone 5", "iPhone 6", "iPhone 7", "iPhone 8", "iPhone X", "Galaxy S III", 
"Galaxy S5", "iPad", "iPad Mini", "iPad Pro", "Kindle Fire HDX", "Nexus 5", "Nexus 6", "Nexus 10"];

    (async () => {
        for (const u of URLS){
            for (const d of devices){
                const EMULATE_DEVICE = d;
                // Save the results to a folder
                let OUT_DIR = true;
            
                // The URL to test
                const URL = u;
            
                const defaultConfig = {
                inUrl: `http://${URL}`,
                numPages: 3,
                headless: true,
                emulateDevice: EMULATE_DEVICE,
                };

                let devPath;
                if (!EMULATE_DEVICE){
                    devPath = "Native"
                }
                else{
                    var s = "" + EMULATE_DEVICE;
                    devPath = s.replace(/ /g, '')
                }
                
                process.stdout.write('Collecting ' + u + ' with device ' + devPath);
                const result = await collector(
                OUT_DIR
                    ? { ...defaultConfig, ...{ outDir: join(__dirname, "data", URL, devPath) } }
                    : defaultConfig
                );
                if (OUT_DIR) {
                    process.stdout.clearLine();
                    process.stdout.cursorTo(0);
                    process.stdout.write('Collecting ' + u + ' with device ' + d + ' ...Ok\n');
                }
    }}})();
