import re 
import sys
import os

args = sys.argv

# 同じファイル名が存在するかチェック
def duplicate_rename(value, already_written_files, count=1):
    # フルパスから「フルパスタイトル」と「拡張子」を分割
    ftitle, fext = os.path.splitext(value)
    m = re.match(r'(.+)_(\d+?)$', ftitle)
    # if matched
    if m is not None:
        #print(m[2])
        count = int(m[2]) + 1
    
    # タイトル末尾に_(数値)が在れば削除する。
    newftitle = re.sub(r'_\d+?$', "", ftitle)

    while(value in already_written_files):        
        # _1 という文字列を作成
        addPara = '_' + '{}'.format(count)

        # フルパスタイトル + _1 + 拡張子のファイル名を作成
        value = os.path.join(newftitle + addPara + fext)

        # リネームしたファイルを表示
        #print('Rename: %s' % value)

        count += 1
    return value

if __name__ == "__main__":
    in_html = args[1]

    backup_dir = 'backuped'
    image_dir = backup_dir + '/' + os.path.splitext(os.path.basename(in_html))[0]

    os.makedirs(image_dir, exist_ok=True)
    with open(in_html, 'r') as f:
        s = f.read()
        
        matched = re.findall(r'src=\"(https?://cdn.discordapp\.com/attachments/.+\.(jpg|png|JPG|PNG))\"', s)

        urls = [m[0] for m in matched]
        img_filenames = [re.match(".+/(.+?)([\?#;].*)?$", url)[1] for url in urls]
        new_html_filename = backup_dir + '/' + os.path.splitext(os.path.basename(in_html))[0] + '_bak.html'
        new_html = s

        already_written_files = []
        for fn, url in zip(img_filenames, urls):
            path = image_dir + '/' + fn
            path = duplicate_rename(path, already_written_files)
            already_written_files.append(path)
            #os.system("wget {} -O '{}'".format(url, path))

            # htmlから見た画像ディレクトリの場所
            image_path_from_html = os.path.splitext(os.path.basename(in_html))[0] + '/' + os.path.basename(path)
            new_html = new_html.replace(url, image_path_from_html)

    # write new html
    with open(new_html_filename, 'w') as f_new:
        f_new.write(new_html)
