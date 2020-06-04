import os


def test_func(in_path, out_format, out_location):
    file_folder_path = os.path.dirname(in_path)
    filename_original = os.path.splitext(os.path.basename(in_path))[0]
    file_ext = os.path.splitext(in_path)[1]
    if out_format == 'original':
        out_ext = file_ext
    else:
        out_ext = out_format
    out_file_name = filename_original + '_ACEScg' + out_ext

    if out_location == 'file':
        output_path = os.path.join(file_folder_path, out_file_name)
        return output_path
    if out_location == 'folder':
        acesFolder_path = os.path.join(file_folder_path, 'ACEScg')
        if not os.path.exists(acesFolder_path):
            os.makedirs(acesFolder_path)
        output_path = os.path.join(acesFolder_path, out_file_name)
        return output_path


if __name__ == '__main__':
    path = r"E:\Images\artist_workshop4k.hdr"
    print(test_func(path, '.exr', 'file'))
    print(test_func(path, '.exr', 'folder'))
