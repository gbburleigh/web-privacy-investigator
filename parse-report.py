import sys, os, glob, json 
import csv
from pprint import pprint
from datetime import datetime
from urllib.parse import urlparse

#Parses inspection files for a list of URLs
def load_inspection_files(urls):

    #Instantiate CSV writer
    with open(f'scan_report:{datetime.today()}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)

        #Column names
        writer.writerow(['url', 'device', 'flagged_behaviour', 'occurences', 'third_party_url', 'third_party_domain', 'behaviour_type'])

        #For each given URL
        for url in urls:
            url_dir = os.getcwd() + f'/data/{url}/'

            #Get all device scans for this URL in our data directory
            for device in os.listdir(url_dir):

                #If we have inspection.json available, use it and continue
                if device == 'inspection-log.ndjson':
                    continue
                try:
                    fp = open(url_dir + f'{device}/inspection.json') 
                except:
                    continue

                #Crawl inspection.json
                with open(url_dir + f'{device}/inspection.json') as fp:

                    #Instantiate json object
                    data = json.load(fp)

                    #Get reports section from inspection
                    reports = data['reports']

                    #Pull out entries
                    keyloggers = reports['key_logging']
                    session_recorders = reports['session_recorders']
                    third_party_trackers = reports['third_party_trackers']
                    canvas_fingerprinters = reports['canvas_fingerprinters']
                    canvas_font_fingerprinters = reports['canvas_font_fingerprinters']

                    #This entry needs work, fix later 
                    if (canvas_font_fingerprinters is not None):
                        print(canvas_font_fingerprinters)

                    behaviour_event_listeners = reports['behaviour_event_listeners']
                    fb_pixel_events = reports['fb_pixel_events']

                    #Key loggers
                    if keyloggers != {}:
                        for key in keyloggers.keys():
                            for i in keyloggers[key]:
                                writer.writerow([url, device, 'key_logging', len(keyloggers[key]), i['post_request_url'], key, f"logging type {i['match_type']}"])
                    
                    #Session recorders
                    if session_recorders != {}:
                        payload = {}
                        for key in session_recorders.keys():
                            if key in payload.keys():
                                payload[key] += 1
                            else:
                                payload[key] = 1
                        for key in payload:
                            writer.writerow([url, device, 'session_recording', payload[key], key, urlparse(key).netloc, f'{len(session_recorders[key])} scripts recording'])
                    
                    #Third party trackers
                    if third_party_trackers != []:
                        payload = {}
                        for entry in third_party_trackers:
                            t = entry['type']
                            u = urlparse(entry['url']).netloc
                            if entry['url'] in payload.keys():
                                if t in payload[entry['url']].keys():
                                    payload[entry['url']][t] += 1
                                else:
                                    payload[entry['url']][t] = 1
                            else:
                                payload[entry['url']] = {}
                                payload[entry['url']][t] = 1
                        for key in payload:
                            for t in payload[key]:
                                writer.writerow([url, device, 'third_party_tracking', payload[key][t], key, urlparse(key).netloc, t])

                    #Canvas fingerprinters
                    if canvas_fingerprinters != {}:
                        if canvas_fingerprinters['data_url'] != {}:
                            for p in canvas_fingerprinters['data_url'].keys():
                                u = urlparse(p).netloc
                                for i in canvas_fingerprinters['data_url'][p]:
                                    writer.writerow([url, device, 'canvas_fingerprinting', len(canvas_fingerprinters['fingerprinters']), p, u, i.split(';')[0]])
                    
                    #Behaviour event listeners
                    if behaviour_event_listeners != {}:
                        payload = {}
                        for key in behaviour_event_listeners.keys():
                            for k in behaviour_event_listeners[key].keys():
                                u = urlparse(k).netloc
                            if key in payload.keys():
                                payload[key] += 1
                            else:
                                payload[key]= 1
                        for key in payload:
                            for k in behaviour_event_listeners[key].keys():
                                writer.writerow([url, device, 'event_listening', len(behaviour_event_listeners[key][k]), k, urlparse(k).netloc, f'{key} event listening'])
                    
                    #Facebook pixel events
                    if fb_pixel_events != []:
                        for e in fb_pixel_events:
                            writer.writerow([url, device, 'facebook_pixel_event', len(fb_pixel_events), e['raw'], urlparse(e['raw']).netloc, e['eventName']])

if __name__ == '__main__':
    load_inspection_files(sys.argv[1:])

