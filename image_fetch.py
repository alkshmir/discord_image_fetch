import re 
import sys
import os

args = sys.argv

# 同じファイル名が存在するかチェック
def duplicate_rename(value, count=1):
    if os.path.exists(value):
        # 存在した場合

        # フルパスから「フルパスタイトル」と「拡張子」を分割
        ftitle, fext = os.path.splitext(value)

        # タイトル末尾に(数値)が在れば削除する。
        newftitle = re.sub(r'_\d+?$', "", ftitle)

        # _1 という文字列を作成
        addPara = '_' + '{}'.format(count)

        # フルパスタイトル + _1 + 拡張子のファイル名を作成
        fpath = os.path.join(newftitle + addPara + fext)

        # リネームしたファイルを表示
        print('Rename: %s' % fpath)

        # 再度渡してリネームしたファイル名が存在しないかチェック
        return (duplicate_rename(fpath, count + 1))
    else:
        # 存在しない場合
        return value

if __name__ == "__main__":
    in_html = args[1]

    dir = args[1][:-5]

    os.makedirs(dir, exist_ok=True)
    with open(in_html, 'r') as f:
        s = f.read()
        
        matched = re.findall(r'src=\"(https?://cdn.discordapp\.com/attachments/.+\.(jpg|png|JPG|PNG))\"', s)

        urls = [m[0] for m in matched]
        filenames = [re.match(".+/(.+?)([\?#;].*)?$", url)[1] for url in urls]
        new_html_filename = os.path.splitext(os.path.basename(in_html))[0] + '_bak.html'
        new_html = s

        for fn, url in zip(filenames, urls):
            path = dir + '/' + fn
            path = duplicate_rename(path)
            os.system("wget {} -O '{}'".format(url, path))

            new_html = new_html.replace(url, path)

    # write new html
    with open(new_html_filename, 'w') as f_new:
        f_new.write(new_html)
