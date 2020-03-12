
def id_image_path(instance, filename):
    return f"ID_image/{instance.id}/{instance.title}/{filename}"


def profile_image_path(instance, filename):
    return f"profile/{instance.id}/{instance.user.username}/{filename}"