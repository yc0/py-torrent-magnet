import os
import sys
import bencode
import hashlib
import base64
from urllib.parse import urlencode, quote_plus


def make_magnet_from_file(file) :
    with open(file,'rb') as f:
      bt = bencode.decode(f.read(), 'encoding; default is utf-8');
    
    hashcontents = bt.get('info')
    digest = hashlib.sha1(bencode.encode(hashcontents)).digest()
    b32hash = base64.b32encode(digest)
    
    params = {'dn': bt.get('info').get('name'),
	            'tr': bt.get('announce'),
              'xl': bt.get('info').get('length')}

    paramstr = urlencode(params)
    magneturi = 'magnet:?xt=urn:btih:%s&%s' % (b32hash.decode('utf-8'), paramstr)
    return magneturi
    
if __name__ == "__main__":
    path = sys.argv[1]
    print(path)
    torrents = [make_magnet_from_file(os.path.join(path, f)) for f in os.listdir(path) if f.endswith(".torrent")]    
    for t in torrents:
      print(t)
    