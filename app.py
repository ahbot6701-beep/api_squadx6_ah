from flask import Flask, request, jsonify
import os
import json
import requests
import time
import socket
import random
import urllib3
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

urllibny.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# Global constants from original script
xK = b'Yg&tc%DEuh6%Zc^8'
xV = b'6oyZDr22E3ychjM%'

def EnV_VaRiAnT(n):
    d = []
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            b |= 0x80
        d.append(b)
        if not n:
            break
    return bytes(d)

def ProToBuF(Fields):
    p = bytearray()
    for f, v in Fields.items():
        if isinstance(v, bool):
            p.extend(EnV_VaRiAnT((f << 3) | 0))
            p.extend(EnV_VaRiAnT(1 if v else 0))
        elif isinstance(v, int):
            p.extend(EnV_VaRiAnT((f << 3) | 0))
            p.extend(EnV_VaRiAnT(v))
        elif isinstance(v, str):
            d = v.encode()
            p.extend(EnV_VaRiAnT((f << 3) | 2))
            p.extend(EnV_VaRiAnT(len(d)))
            p.extend(d)
        elif isinstance(v, (bytes, bytearray)):
            d = bytes(v)
            p.extend(EnV_VaRiAnT((f << 3) | 2))
            p.extend(EnV_VaRiAnT(len(d)))
            p.extend(d)
    return bytes(p)

def Read_VaRiAnT(data, pos):
    result = 0
    shift = 0
    while pos < len(data):
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7
    return result, pos

def Parse_ProToBuF(data):
    fields = {}
    pos = 0
    n = len(data)
    while pos < n:
        try:
            key, pos = Read_VaRiAnT(data, pos)
        except:
            break
        fn = key >> 3
        wt = key & 0x07
        try:
            if wt == 0:
                val, pos = Read_VaRiAnT(data, pos)
            elif wt == 2:
                ln, pos = Read_VaRiAnT(data, pos)
                val = data[pos:pos + ln]
                pos += ln
            elif wt == 5:
                val = data[pos:pos + 4]
                pos += 4
            elif wt == 1:
                val = data[pos:pos + 8]
                pos += 8
            else:
                break
        except:
            break
        fields.setdefault(fn, []).append(val)
    return fields

def Ua():
    return random.choice(['4.0.18P6','4.0.19P7','4.0.20P1','4.1.0P3','4.1.5P2','4.2.1P8','4.2.3P1','5.0.1B2','5.0.2P4','5.1.0P1','5.2.0B1','5.2.5P3','5.3.0B1','5.3.2P2','5.4.0P1','5.4.3B2','5.5.0P1','5.5.2P3'])

def EnC_PacKeT(HeX, K, V):
    return AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(HeX), 16)).hex()

def DecodE_HeX(H):
    R = hex(H)
    F = str(R)[2:]
    if len(F) == 1:
        F = "0" + F
    return F

def GeneRaTePk(Pk, N, K, V):
    PkEnc = EnC_PacKeT(Pk, K, V)
    _ = DecodE_HeX(int(len(PkEnc) // 2))
    if len(_) == 2:
        HeadEr = N + "000000"
    elif len(_) == 3:
        HeadEr = N + "00000"
    elif len(_) == 4:
        HeadEr = N + "0000"
    elif len(_) == 5:
        HeadEr = N + "000"
    else:
        HeadEr = N + "00000"
    return bytes.fromhex(HeadEr + _ + PkEnc)

def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnV_VaRiAnT(field_header) + EnV_VaRiAnT(value)

def CrEaTe_LenGth(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnV_VaRiAnT(field_header) + EnV_VaRiAnT(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGth(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGth(field, value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    nested_packet = CrEaTe_ProTo(item)
                    packet.extend(CrEaTe_LenGth(field, nested_packet))
    return packet

def OpenSq(K, V):
    fields = {1: 1, 2: {2: '011d', 3: 1, 4: 3, 5: 'ar', 8: {1: 'IDC4', 2: 145, 3: "ME"}, 9: 1, 10: '01030407090a0b12191a201d2729', 11: 1, 13: 1, 14: {1: {6: 56}, 2: 731, 3: '745d59541601024c01015f02020d0905030304570608570d57060d53540402025f5707545301060613050645775945454c18021c051e1a0306491a4760785c53477d735a53486073421b5d5841075642426f5c63610914084e1f005e721f6001467e0c51634263771f5f554642434556660104040f13050445636e74634379505365047256665e405459657766510f615a5250420d11084858416a0d7a470c720065655c5f5a0370584559584a457f43675f460c16024e477a4258430c6050417a45545c47786456597a7a7163545907714109160849667377607d0b4a07657c5c45045f5d784f5b5665096464065875620411050d4d7f7444766661406a6205545d5b5f74507e0b0b535c67580877607d0a1a0148761e795678487f7871465874697177534971666d5a7574677075550d17034503781a675e60787f4d406d7a625d57797d441b47057b026d1a685a0d1102044b0d60040d706067756547767d66777b7f46007346667e43065e5c780813074c5606764057727546596364037054674d590161467f73416209077108', 4: 'w]ZP', 6: 11, 7: '140b7d71715b751011', 8: '1.126.8', 9: 3, 10: 2, 11: '0362625351363559382b505637416456324b796f566c6364724541566d46795954394b384445494d7a4b646d4b4231562f2b5a727775754a307847426c36712b38683863796b56447967524f4e3676493259347a646974684371364b73464d33724e534a4c4274594f3256565a5465786235484c324c39544a7652514c55374a525663696154544d46776e594e4b4c35353150336c5831475150635668615a77396251674b4d30395a4b6a2f4d675a38656d66757a6e4b356f5a6734367841626a7761363273366235636469637867386a6d4e4944594c383638686e756c3044316a4e445636444a4a69614758456154782b5450696c6f69476f58333638497234563266697a63783934436f5562735039765855683438356a626233356a717a5577504365554c55776374534574456d68426c3957453943524873422b76504a39704863323479517a70446c74644779536f6a6a4f573166433343413733374e617255546d734a70355431686b35635853307134557a6f7a6b75684b6d42423067354f4563634b627a68506c585943712f666a59767531624174504d766437486f4e6e39696e53767679796c6156386e315837636b7978384575626b5868414734565069425961556a75667a2b75675a474164356872324c3156615434613143485745702f6b446142364849434b756f705770706c703151373265463252744f62544957487775305a6753474659514266396f6e48744e7a5035336e72457072366f6c5349455354393839414f494858313471384d4a5763546d514267486d6c3456454c617354426d6f2b36764149525752783664617256692f345147566f4c785944593359477a366e513d3d'}, 19: 329, 21: '374f5219', 24: {1: 21}}}
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0515', K, V)

def ChSq(Nu, Uid, K, V):
    fields = {1: 17, 2: {1: int(Uid), 2: 1, 3: int(Nu - 1), 4: 1, 5: '011d', 8: 1}}
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0515', K, V)

def SendSq(Nu, Uid, K, V):
    fields = {1: 2, 2: {1: int(Uid), 2: "ME", 4: int(Nu)}}
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0515', K, V)

def PyL(access_token, open_id):
    P = {}
    P[3] = time.strftime("%Y-%m-%d %H:%M:%S")
    P[4]="free fire"
    P[5]=1
    P[7]="1.132.9"
    P[8]="Android OS 14 / API-34 (UP1A.231005.007/V816.0.15.0.UNQMIXM)"
    P[9]="Handheld"
    P[10]="Grameenphone"
    P[11]="CarrierDataNetwork"
    P[12]=1666
    P[13]=750
    P[14]="352"
    P[15]="ARM64 FP ASIMD AES | 2400 | 8"
    P[16]=5563
    P[17]="Mali-G57 MC2"
    P[18]="OpenGL ES 3.2 v1.r32p1-01eac0.0a0b917d9265b4c01be9925306306139"
    P[19]="Google|9cc73f7a-91f6-40f6-87ec-5b67e597eb8c"
    P[20]="59.152.5.188"
    P[21]="en"
    P[22]=open_id
    P[23]="8"
    P[24]="Handheld"
    P[25]="Xiaomi 2312DRAABI"
    P[26]="BD"
    P[29]=access_token
    P[30]=1
    P[41]="Grameenphone"
    P[42]="Cellular"
    P[57]="7428b253defc164018c604a1ebbfebdf"
    P[60]=109685
    P[61]=58294
    P[62]=797
    P[63]=18000
    P[64]=58818
    P[65]=109685
    P[66]=58818
    P[67]=109685
    P[73]=2
    P[74]="/data/app/~~cqQgpdMykLQEM3odipXatw==/com.dts.freefireth-G6e5yOt1dtuXG5Ambhj18g==/lib/arm64"
    P[76]=1
    P[77]="b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~cqQgpdMykLQEM3odipXatw==/com.dts.freefireth-G6e5yOt1dtuXG5Ambhj18g==/base.apk"
    P[78]=3
    P[79]=2
    P[81]="64"
    P[83]="2019121229"
    P[85]=3
    P[86]="OpenGLES2"
    P[87]=4095
    P[88]=8
    P[89]=b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    P[90]="Dhaka"
    P[91]="C"
    P[92]=8043
    P[93]="android"
    P[94]="KqsHT4XbSZhqerDNUhjbS3DxG/4+I62zQU2tZFJN91kBUICAlZ5yujshLKvjlk/KiShfKfis8EeB1PMhFHIodWPncZC4fCHYF3TcTwNj95aWY/S3"
    P[95]=111207
    P[96]='{"cur_rate":[60,90,120],"support_etc2":false}'
    P[97]=1
    P[98]=1
    P[99]="4"
    P[100]="4"
    P[102]="GQ] e"
    P[103]=1
    P[104]=45174
    P[105]=1
    P[106]="https://dl-bs.ggpolarbear.com/live/ABHotUpdates/|https://core-bs.ggpolarbear.com/live/ABHotUpdates/|a4332cb1c1a84e51dd77441e4856ed5a"
    P[107]="1.9393e7b8e53e8aeb"
    return AES.new(xK, AES.MODE_CBC, xV).encrypt(pad(ProToBuF(P), 16))

def Strip_MajorLogin_Prefix(body):
    if len(body) <= 64:
        return body
    try:
        if 8 in Parse_ProToBuF(body):
            return body
    except:
        pass
    try:
        if 8 in Parse_ProToBuF(body[64:]):
            return body[64:]
    except:
        pass
    return body[64:]

def GeT_AccEss(uid, password):
    url = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
    headers = {"User-Agent": Ua(), "Content-Type": "application/json; charset=utf-8"}
    try:
        R = requests.post(url, headers=headers, json={"client_id": 100067, "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3", "client_type": 2, "device_id": "", "password": password, "response_type": "token", "uid": int(uid)}, verify=False, timeout=15)
    except Exception as e:
        return None
        
    if R.status_code not in (200, 201):
        return None
    try:
        J = R.json()
    except:
        return None
    if J.get("code") != 0:
        return None
    d = J.get("data", {})
    return {"access_token": d.get("access_token"), "open_id": d.get("open_id")}

def MajorLogin(Payload):
    url = "https://loginbp.ppmainecoonghj.com/MajorLogin"
    headers = {"User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)", "Accept": "*/*", "Accept-Encoding": "deflate, gzip", "X-GA-SV": str(int(time.time())), "Authorization": "Bearer ", "X-GA": "v1 1", "ReleaseVersion": "OB55", "Content-Type": "application/x-www-form-urlencoded", "X-Unity-Version": "2018.4.12f1"}
    try:
        R = requests.post(url, headers=headers, data=Payload, verify=False, timeout=15)
    except Exception:
        return None
    return R.content if R.status_code in (200, 201) and R.content else None

def GeTLoginDaTa(client_url, payload, jwt):
    url = f"{client_url}/GetLoginData"
    headers = {"User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)", "Accept": "*/*", "Accept-Encoding": "deflate, gzip", "X-GA-SV": str(int(time.time())), "Authorization": f"Bearer {jwt}", "X-GA": "v1 1", "ReleaseVersion": "OB55", "Content-Type": "application/x-www-form-urlencoded", "X-Unity-Version": "2018.4.12f1"}
    try:
        R = requests.post(url, headers=headers, data=payload, verify=False, timeout=15)
    except Exception:
        return None
    return R.content if R.status_code == 200 and R.content else None

def ExtractMajorLogin(ml_resp):
    body = Strip_MajorLogin_Prefix(ml_resp)
    f = Parse_ProToBuF(body)
    
    def _gv(fields, n):
        v = fields.get(n)
        if v is None:
            return None
        if isinstance(v, list):
            v = v[0]
        return v

    jwt_b = _gv(f, 8)
    url_b = _gv(f, 10)
    ts_v = _gv(f, 21)
    key_b = _gv(f, 22)
    iv_b = _gv(f, 23)
    acct_v = _gv(f, 1)
    
    jwt = jwt_b.decode() if isinstance(jwt_b, bytes) else jwt_b
    url = url_b.decode() if isinstance(url_b, bytes) else url_b
    ts = ts_v if isinstance(ts_v, int) else None
    acct = acct_v if isinstance(acct_v, int) else None
    
    if not jwt or not isinstance(key_b, bytes) or not isinstance(iv_b, bytes):
        return None
    return {"jwt": jwt, "url": url, "ts": ts, "key": key_b, "iv": iv_b, "account_id": acct}

def BuildAuthToken(uid, jwt_str, ts, key, iv, mode="chat"):
    ah = f"{int(uid):x}"
    if len(ah) > 16:
        raise ValueError("uid hex too long")
    ah = ah.zfill(16)
    enc = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(jwt_str.encode(), 16)).hex()
    th = f"{int(ts):x}"
    if len(th) % 2:
        th = "0" + th
    tsz = f"{len(enc)//2:02x}"
    pad_ = "00000" if mode == "chat" else "0000000000000"
    return f"9015{ah}{th}{pad_}{tsz}{enc}"

def _TuneSock(s):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    try:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
    except Exception:
        pass

# Configuration
UID = "8423243994"
PASSWORD = "a51c2d6446fa3dcc710d"

@app.route('/')
def home():
    return jsonify({"message": "API is running", "usage": "Use /connect to connect"})

@app.route('/connect', methods=['GET'])
def connect():
    """
    Connects to the game server using the bot credentials.
    This endpoint accepts an optional uid parameter via query string:
    https://your-render-url/connect?uid=123456
    If no uid is provided, it uses the default UID in the code.
    """
    target_uid = request.args.get('uid')
    
    # Use provided UID or fallback to default
    current_uid = target_uid if target_uid else UID
    
    td = GeT_AccEss(current_uid, PASSWORD)
    if not td:
        return jsonify({"error": "Failed to get access token"}), 500
        
    access_token = td["access_token"]
    open_id = td["open_id"]
    
    login_payload = PyL(access_token, open_id)
    ml = MajorLogin(login_payload)
    if not ml:
        return jsonify({"error": "MajorLogin failed"}), 500
        
    ad = ExtractMajorLogin(ml)
    if not ad:
        return jsonify({"error": "MajorLogin parse failed"}), 500
        
    jwt = ad["jwt"]
    ts = ad["ts"]
    key = ad["key"]
    iv = ad["iv"]
    url = ad["url"] or "https://clientbp.ppmainecoonghj.com"
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        
    ld = GeTLoginDaTa(url, login_payload, jwt)
    if not ld:
        return jsonify({"error": "GetLoginData failed"}), 500
        
    gl = Parse_ProToBuF(ld)
    
    def gv(n):
        v = gl.get(n)
        if v is None:
            return None
        if isinstance(v, list):
            v = v[0]
        return v

    def gs(n):
        v = gv(n)
        return v.decode() if isinstance(v, bytes) else v

    player_name = gs(4) or ""
    func_addr = gs(14)
    info_addr = gs(32)
    
    if not func_addr or not info_addr:
        return jsonify({"error": "Missing IP/Port info"}), 500

    ip_online, port_online = func_addr.split(":")
    ip_chat, port_chat = info_addr.split(":")
    
    account_id = ad["account_id"] or gv(gl, 1) or gv(gl, 5) or 0
    
    return jsonify({
        "player_name": player_name,
        "account_id": account_id,
        "ip_online": ip_online,
        "port_online": port_online,
        "ip_chat": ip_chat,
        "port_chat": port_chat
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))