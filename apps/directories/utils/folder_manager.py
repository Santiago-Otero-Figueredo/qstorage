from django.conf import settings

import os, shutil, errno

def create_folder(folder_instance:'Folder'):
 
    MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", None)

    user_path = f'{folder_instance.owner_user.pk}'
    ancestors = folder_instance.get_ancestors().values_list('name', flat=True)

    list_path = [user_path]

    if ancestors:
        list_path = list_path + ancestors[1::] + [folder_instance.name]

    path_folder = "/".join(list_path)
    media_patch_folder = os.path.join(MEDIA_ROOT, path_folder)
  
    os.umask(0)
    os.makedirs(media_patch_folder, mode=0o777)

    folder_instance.route = f'{path_folder}/'


def update_children_folders(folder_instance:'Folder', rename_folder=True):

    print(folder_instance)

    if rename_folder:
        MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", None)

        if folder_instance.is_leaf():
            route_children = folder_instance.route.split('/')
        else:
            first_children = folder_instance.get_first_child()
            route_children = first_children.route.split('/')
        
        route_children = route_children[:-1]
        old_path_children = "/".join(route_children)

        media_patch_children_folder = os.path.join(MEDIA_ROOT, old_path_children)

        if folder_instance.is_leaf() and not folder_instance.is_root():        
            media_patch_children_folder = os.path.join(media_patch_children_folder, folder_instance.old_name)

        media_patch_parent_folder = os.path.join(MEDIA_ROOT, folder_instance.route, folder_instance.name)
        
        print(media_patch_parent_folder)
        print(media_patch_children_folder)

        os.rename(media_patch_children_folder, media_patch_parent_folder)

    children_folders = folder_instance.get_children()
    children_folders.update(route =f'{folder_instance.route}{folder_instance.name}/')

    if folder_instance.get_children_count() > 0:
        for children in children_folders:
            update_children_folders(children, rename_folder=False)
