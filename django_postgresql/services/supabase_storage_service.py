import os
from typing import List
import uuid
from dotenv import load_dotenv
from supabase import create_client, Client

# Nạp file .env
load_dotenv()


class SupabaseStorageService:
    def __init__(self):
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
        )

    def list_all_files(self, bucket: str):
        response = self.supabase.storage.from_(bucket).list(
            # "",  # path đến folder cần lấy danh sách, để trống là lấy root
            # {  # Các option tìm kiếm
            #     "limit": 100,
            #     "offset": 0,
            #     "sortBy": {"column": "name", "order": "desc"},
            #     "search": "jon",
            # },
        )
        return response

    def upload_file(self, bucket: str, file_name: str, file, folder_path: str = ""):
        """
        Upload a file to Supabase Storage.

        :param bucket: Bucket name
        :param path: Path inside the bucket (e.g. 'folder/image.jpg')
        :param file: File object (can be request.FILES['file'])
        """
    
        path = f"{folder_path}{uuid.uuid4()}_{file_name}"

        # Response trả về kiểu UploadResponse
        response = self.supabase.storage.from_(bucket).upload(
            path=path,
            file=file.read(),
            file_options={
                "cache-control": "3600",
                "content-type": file.content_type,
                "upsert": "false",
            },
        )
        # convert sang dict rồi return
        response_dict = vars(response)
        response_dict['public_url'] = os.getenv("PUBLIC_URL_IMG") + response_dict.get('full_path')
        return response_dict

    def get_public_url(self, bucket: str, path: str):
        """
        Get public URL of a file.
        """
        return self.supabase.storage.from_(bucket).get_public_url(path)

    # def create_signed_url(self, bucket: str, path: str, expires_in: int = 3600):
    #     """
    #     Create a signed URL (if the file is private).
    #     """
    #     return self.supabase.storage.from_(bucket).create_signed_url(path, expires_in)

    def delete_file(self, bucket: str, path: List[str]):
        """
        Delete a file from Supabase Storage.
        """
        return self.supabase.storage.from_(bucket).remove(path)
