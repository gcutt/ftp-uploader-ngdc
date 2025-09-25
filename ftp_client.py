"""
"""

from ftplib import FTP, error_perm
import os

FTP_HOST = "incoming.ngdc.noaa.gov"
FTP_USER = "anonymous"
FTP_PASS = ""  # Leave blank

def uploadfile(local_path, folder_name):
    filename = os.path.basename(local_path)
    target_dir = f"/pub/incoming/{folder_name}"

    try:
        with FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            print("✅ Logged in to ngdc FTP")

            try:
                ftp.cwd(target_dir)
            except error_perm:
                print("📁 Creating target directory...")
                ftp.cwd("/pub/incoming")
                ftp.mkd(folder_name)
                ftp.cwd(target_dir)

            with open(local_path, "rb") as file:
                ftp.storbinary(f"STOR {filename}", file)
                print(f"🚀 Uploaded {filename} to {target_dir}")
                return f"✅ Uploaded {filename} to {folder_name} successfully"

    except Exception as e:
        print(f"❌ FTP upload failed: \n{e}")
        return f"❌ Upload failed: \n{e}"
    
def uploadfiles(local_paths, folder_name):
    target_dir = f"/pub/incoming/{folder_name}"
    results = []

    try:
        with FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            print("✅ Logged in to NGDC FTP")

            try:
                ftp.cwd(target_dir)
            except error_perm:
                print("📁 Creating target directory...")
                ftp.cwd("/pub/incoming")
                ftp.mkd(folder_name)
                ftp.cwd(target_dir)

            for path in local_paths:
                filename = os.path.basename(path)
                try:
                    with open(path, "rb") as file:
                        ftp.storbinary(f"STOR {filename}", file)
                        print(f"🚀 Uploaded {filename}")
                        results.append(f"✅ {filename}")
                except Exception as e:
                    print(f"❌ Failed to upload {filename}: \n{e}")
                    results.append(f"❌ {filename}: \n{e}")

        return "\n".join(results)

    except Exception as e:
        print(f"❌ FTP session failed: \n{e}")
        return f"❌ FTP session failed: \n{e}"    