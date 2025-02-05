from domain.manager.minio_manager import MinioManager

minio_manager = MinioManager()
files = minio_manager.get_files('1/')
for file in files:
    print(file.object_name)