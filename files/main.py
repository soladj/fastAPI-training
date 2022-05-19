from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/files/")
async def create_file(file: bytes = File(default=None)):
    """Only receive a bytes for the image. Do not receive metadata about that.

    Args:
        file (bytes, optional): Bytes of the file. Defaults to File(default=None).

    Returns:
        file_size: Size of the file.
    """
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile): #Better
    """This is the best option to receive files.
    To read that can use file.file.read() method.

    Args:
        file (UploadFile): File object with metadata

    Returns:
        filename: Name of the file.
    """
    return {"filename": file.filename}
