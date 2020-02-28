import collections
import time
import hmac
import json
import base64
def gen_api_request(request_src, secretkey):
    '''generate signature, then output the request data with signature and timestamp'''
    timestamp = int(round(time.time() * 1000))  # get current timestamp
    def Ord(request_src_dic):
        request_src_dic = collections.OrderedDict(request_src_dic)
        for  key, value in request_src_dic.items():
            if isinstance(value,dict):
                request_src_dic[key] = collections.OrderedDict(value)
        return collections.OrderedDict(request_src_dic)

    request_src_dic = json.loads(request_src)
    request_src_dic['params']['timestamp'] = timestamp
    #print(request_src_dic)
    request_src_dic = Ord(request_src_dic) # transfer json string to python dic object
    #print(type(request_src_dic))
    message = json.dumps(request_src_dic, separators=(',', ':'))
    hamc_src = hmac.new(bytes(secretkey, encoding='utf-8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    sig = base64.b64encode(hamc_src.digest()).decode('utf-8')
    request_src_dic['params']['signature'] = sig
    #print(type(request_src_dic))
    request_data = json.dumps(request_src_dic, separators=(
    ',', ':'))  # remove the characters 'space 'which is round at the ',' and ':', to ovoid generate the signature
    #print(message)
    #print (request_data)
    return request_data

request_src ='{"jsonrpc":"2.0","method":"getStakerInfo","params":{"chainType":"WAN", "blockNumber":6243066},"id":1}'
request_src='{"jsonrpc":"2.0","method":"getTransactionReceipt","params":{"chainType":"WAN", "txHash":"0x8bc24b488109839049a0e7e719eef6e382979323e4842e5b7410e78b701f4f2c"},"id":1}'
request_src = '{"jsonrpc":"2.0","method":"getBalance","params":{"address":"0xe659b7c9d33563103b206bd7fce7d53a5eeaaeed", "chainType":"WAN"},"id":1}'
secretkey = "dff3ed491f59de5e12026652c2aff088243bd15825b9994ca93f347b85610263"
print(gen_api_request(request_src,secretkey))

with open('./result.json','r') as f:
    a = json.load(f)

print(len(a['result']))