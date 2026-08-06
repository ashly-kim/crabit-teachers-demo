#!/usr/bin/env python3
"""classin/index.html 하나에서 v1 · v2 전용 페이지를 뽑는다.

index.html은 두 시나리오를 모두 담은 내부 검토용이다. 외부 공유용으로는
버전 전환기가 없고 다른 버전에 접근할 수 없는 페이지가 따로 필요해서,
여기서 정적으로 생성한다.

    python3 build-variants.py

  v1/index.html  LMS Heavy 고정 (내부용)
  v2/index.html  Simple Integration 고정 (클래스인 공유용)

index.html을 고친 뒤에는 이 스크립트를 다시 돌려야 v1·v2에 반영된다.
"""
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'index.html')

# 버전 전환 세그먼트 (nav 칩 안)
SEG = re.compile(
    r'\s*<span class="ci-verseg".*?</span>\s*(?=</div>)', re.S)


def build(version, title_suffix):
    html = open(SRC, encoding='utf-8').read()

    # 1) 전환기 UI 제거
    html, n = SEG.subn('\n    ', html)
    assert n == 1, f'버전 세그먼트를 찾지 못했습니다 ({n})'

    # 2) 다른 버전 랜딩 페이지 통째로 제거
    drop_id = 'page-classin-intro-v2' if version == 'heavy' else 'page-classin-intro'
    start = html.index(f'<div id="{drop_id}" style="display:none;">')
    depth, i = 0, start
    while True:
        m = re.compile(r'<div\b|</div>').search(html, i)
        depth += 1 if m.group() == '<div' else -1
        i = m.end()
        if depth == 0:
            break
    html = html[:start] + html[i:]

    # 3) 버전을 고정하고 전환 함수를 무력화
    html = html.replace(
        "  let _cinVersion = 'heavy';",
        f"  let _cinVersion = '{version}';   // 이 빌드는 버전 고정")
    html = html.replace(
        "  function setCinVersion(v) {\n    _cinVersion = v;",
        "  function setCinVersion() { return; }\n  function _setCinVersionUnused(v) {\n    _cinVersion = v;")

    # 4) 저장된 버전을 다시 읽어오지 않게
    html = html.replace(
        "    try { v = localStorage.getItem('crabitCinVersion') || 'heavy'; } catch (e) {}",
        f"    v = '{version}';")

    # 5) 제목
    html = html.replace(
        '<title>크래빗 티처스 · 클래스인 연동 데모</title>',
        f'<title>크래빗 티처스 · 클래스인 연동 데모 ({title_suffix})</title>')

    out_dir = os.path.join(HERE, 'v1' if version == 'heavy' else 'v2')
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8').write(html)

    # 6) 에셋은 상위 폴더에 있으므로 <base>로 한 번에 해결한다.
    #    src/href/CSS url()/JS 문자열 경로를 개별로 고치면 빠뜨리기 쉽다.
    path = os.path.join(out_dir, 'index.html')
    fixed = open(path, encoding='utf-8').read().replace(
        '<meta charset="UTF-8">',
        '<meta charset="UTF-8">\n<base href="../">', 1)
    open(path, 'w', encoding='utf-8').write(fixed)

    size = os.path.getsize(os.path.join(out_dir, 'index.html'))
    print(f'{out_dir}/index.html  {size//1024}KB  ({title_suffix})')


if __name__ == '__main__':
    build('heavy', 'LMS Heavy')
    build('simple', 'Simple Integration')
