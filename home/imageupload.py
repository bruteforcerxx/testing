import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
  cloud_name="deo4vjnbz",
  api_key="841179487983546",
  api_secret="kZS_toypwznj10Yx5FWOdGC2rfE",
  secure=True
)

upload("https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg", public_id="olympic_flag")

url, options = cloudinary_url("olympic_flag", width=100, height=150, crop="fill")
print(url, options)
