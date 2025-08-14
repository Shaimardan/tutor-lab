import io
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Generator

try:
    from urllib3.response import BaseHTTPResponse  # type: ignore[attr-defined]
except ImportError:
    from urllib3.response import HTTPResponse as BaseHTTPResponse

from minio import Minio
from minio.deleteobjects import DeleteObject
from minio.error import S3Error

from config import REMOTE_MINIO_URL, minio_config


class BaseStorageClient(ABC):
    @abstractmethod
    def put_object(
        self, file_name: str, file_data: bytes, content_type: str, bucket_name: str
    ) -> dict[str, str]:
        pass

    @abstractmethod
    def fput_object(
        self, file_name: str, file_path: str, content_type: str, bucket_name: str
    ) -> None:
        pass

    @abstractmethod
    def get_file(self, bucket_name: str, object_name: str) -> BaseHTTPResponse:
        pass

    @abstractmethod
    def delete_file(self, object_name: str) -> None:
        pass

    @abstractmethod
    def get_bucket_name(self) -> str:
        pass

    @abstractmethod
    def file_exists(self, bucket_name: str, object_name: str) -> bool:
        pass

    @abstractmethod
    def list_objects(self, prefix: str | None, recursive: bool = True) -> Generator:
        pass

    @abstractmethod
    def delete_batch_files(self, file_names: list[str]) -> None:
        pass

    @abstractmethod
    def generate_presigned_url(self, bucket_name: str, object_name: str, expiry: int = 3600) -> str:
        """Generate a temporary link for a file.

        Args:
            bucket_name: bucket name.
            object_name: position in minio.
            expiry: Link lifetime in minit (default 3600 = 1 hour).

        Returns: Temporary link.
        """
        pass


class MinIOClient(BaseStorageClient):
    def __init__(self, bucket_name: str):
        self.client = Minio(
            minio_config.MINIO_ENDPOINT,
            access_key=minio_config.MINIO_ROOT_USER,
            secret_key=minio_config.MINIO_ROOT_PASSWORD.get_secret_value(),
            secure=minio_config.MINIO_SECURE,
        )
        self.bucket_name = bucket_name

        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def put_object(
        self, file_name: str, file_data: bytes, content_type: str, bucket_name: str
    ) -> dict[str, str]:
        try:
            file_stream = io.BytesIO(file_data)
            self.client.put_object(
                bucket_name,
                file_name,
                file_stream,
                len(file_data),
                content_type=content_type,
            )
        except S3Error as e:
            Exception(500, str(e))
        return {"filename": file_name}

    def fput_object(
        self, file_name: str, file_path: str, content_type: str, bucket_name: str
    ) -> None:
        try:
            self.client.fput_object(
                bucket_name=bucket_name,
                object_name=file_name,
                file_path=file_path,
                content_type=content_type,
            )
        except S3Error as e:
            raise Exception(500, str(e))

    def get_file(self, bucket_name: str, object_name: str) -> BaseHTTPResponse:
        try:
            return self.client.get_object(bucket_name, object_name)
        except S3Error as e:
            if e.code == "NoSuchKey":
                Exception(400, "File not found")
            else:
                Exception(500, str(e))
        return b""

    def generate_presigned_url(self, bucket_name: str, object_name: str, expiry: int = 3600) -> str:
        url = self.client.presigned_get_object(bucket_name, object_name, timedelta(minutes=expiry))
        minio_url = f"http://{minio_config.MINIO_ENDPOINT}"
        remote_url = f"http://{REMOTE_MINIO_URL}"
        return url.replace(minio_url, remote_url)

    def delete_file(self, object_name: str) -> None:
        try:
            self.client.remove_object(self.bucket_name, object_name)
        except S3Error as e:
            Exception(500, str(e))

    def delete_batch_files(self, file_names: list[str]) -> None:
        errors = []
        objects_to_delete = [DeleteObject(file_name) for file_name in file_names]
        for error in self.client.remove_objects(self.bucket_name, objects_to_delete):
            errors.append(error)
        if errors:
            raise Exception(f"Failed to delete files: {errors}")

    def get_bucket_name(self) -> str:
        return bucket_name

    def file_exists(self, bucket_name: str, object_name: str) -> bool:
        try:
            self.client.stat_object(bucket_name, object_name)
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            raise Exception(500, str(e))

    def list_objects(self, prefix: str | None, recursive: bool = True) -> Generator:
        """Возвращает генератор объектов из указанного бакета с возможностью фильтрации по префиксу.

        Args:
            prefix (str | None): Префикс для фильтрации объектов. Если None, фильтрация не применяется.
            recursive (bool): Определяет, нужно ли искать объекты рекурсивно. По умолчанию True.

        Returns:
            Генератор.

        """
        objects = self.client.list_objects(self.bucket_name, prefix=prefix, recursive=recursive)
        return objects


bucket_name = "polyplan-configs-bucket"
minio_client = MinIOClient(bucket_name)
