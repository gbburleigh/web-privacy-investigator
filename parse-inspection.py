import json, pandas, os

def parse_inspection(site, device, filename="inspection-log.ndjson"):
    print(os.listdir(os.getcwd() + f"/data/{site}/'{device}'"))
    dir_ = os.getcwd() + f"/data/{site}/'{device}'"
    dir_ = r'{}'.format(dir_)
    with open(f'{dir_}/{filename}', 'r') as fp:
        lines = []
        for line in fp.readlines():
            j = json.loads(line)
            try:
                data = j['message']['data']
                lines.append(data)
            except:
                pass

    return lines

if __name__=="__main__":
    print(len(parse_inspection('phoenix.edu', 'iPhone4')))
