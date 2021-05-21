from exif import Image

image = Image("test.jpg")

image.gps_latitude = (41.0, 29.0, 57.48)
image.gps_latitude_ref = "N"
image.gps_longitude = (81.0, 41.0, 39.84)
image.gps_longitude_ref = "W"
image.gps_altitude = 199.034  # in meters
image.gps_altitude_ref = GpsAltitudeRef.ABOVE_SEA_LEVEL

with open('modified_image.jpg', 'wb') as new_image_file:
    new_image_file.write(my_image.get_file())