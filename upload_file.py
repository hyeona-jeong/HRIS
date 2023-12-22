from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file

class UploadFile():
    def __init__(self):
        # 231221 구글 드라이브 인증 및 API 서비스 생성 by 정현아
        store = file.Storage('storage.json')
        creds = store.get()
        self.drive = build('drive', 'v3', http=creds.authorize(Http()))
        self.folder_id = "1wHyY-KnAWI8m3kAXUzxo8Tt2OyEC_2g1" 
        
    def upload_file(self, file_path):
        fname = file_path
        metadata={'name':fname, 'parents': [self.folder_id], 'mimeType':None}
        res = self.drive.files().create(body=metadata, media_body=fname).execute()
        if res:
            file_id = res.get("id")
            
            # 파일을 공유 가능하도록 권한설정
            self.drive.permissions().create(
                fileId = file_id,
                body={'type': 'anyone', 'role':'reader'}
            ).execute()
            share_link = f'https://drive.google.com/uc?id={file_id}'
            return share_link