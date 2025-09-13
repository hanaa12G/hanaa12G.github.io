import sys
if __name__ == "__main__":
    url = sys.argv[1]
    id_start = url.find('/d/') + len('/d/')
    id_end   = url.find('/', id_start)
    id_ = url[id_start:id_end]
    print(f'https://drive.google.com/thumbnail?id={id_}&sz=w1920-h1080')
