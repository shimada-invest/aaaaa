# coding: utf-8

"""Boxの認証

アプリケーションの作成:
    1. https://qiita.com/daichiiiiiii/items/d54b856ebaf9f00c528b
    2. https://qiita.com/daichiiiiiii/items/d040babb9e990f682d8a
"""

import json
import os

from boxsdk import Client, JWTAuth
from boxsdk.exception import BoxAPIException


def client(config):
    # コンフィグファイルを辞書に変換
    d = json.load(open(config, "rb"))
    clientID = d["boxAppSettings"]["clientID"]
    clientSecret = d["boxAppSettings"]["clientSecret"]
    publicKeyID = d["boxAppSettings"]["appAuth"]["publicKeyID"]
    privateKey = d["boxAppSettings"]["appAuth"]["privateKey"].encode()
    passphrase = d["boxAppSettings"]["appAuth"]["passphrase"].encode()
    enterpriseID = d["enterpriseID"]
    # 秘密鍵をファイルに保存（2.0以上ならrsa_private_key_dataを使う）
    pem = "%s.pem" % publicKeyID
    open(pem, "wb").write(privateKey)
    # JWT認証オブジェクトを作成
    auth = JWTAuth(
        client_id=clientID,
        client_secret=clientSecret,
        enterprise_id=enterpriseID,
        jwt_key_id=publicKeyID,
        rsa_private_key_file_sys_path=pem,
        rsa_private_key_passphrase=passphrase
    )
    # 認証クライアントを取得
    client = Client(auth)
    os.unlink(pem)  # 秘密鍵を安全のためにunlink
    return client

if __name__ == '__main__':
    import os
    config_json = os.environ.get('BOX_CONFIG')
    box = client(config_json)
    
    from boxsdk.object.collaboration import CollaborationRole
    sasao = box.user(user_id='6234468537')

    folder = box.folder('0').create_subfolder('ライフスタンダード')
    collaboration = folder.collaborate(sasao, CollaborationRole.CO_OWNER)
