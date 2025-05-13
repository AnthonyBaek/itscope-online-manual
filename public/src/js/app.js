// 전역 변수
let menuData = null;
let currentContent = null;

// DOM이 로드되면 실행
document.addEventListener('DOMContentLoaded', async () => {
    // 메뉴 데이터 로드
    try {
        const response = await fetch('/02_outputs/manual_toc_json.json');
        menuData = await response.json();
        renderMenuTree(menuData);
    } catch (error) {
        console.error('메뉴 데이터 로드 실패:', error);
    }

    // 검색 이벤트 리스너
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    const searchBtn = document.getElementById('searchBtn');
    // input 입력 시 X 버튼 표시/숨김
    searchInput.addEventListener('input', () => {
        if (searchInput.value.length > 0) {
            clearSearchBtn.style.display = 'flex';
        } else {
            clearSearchBtn.style.display = 'none';
        }
    });
    // X 버튼 클릭 시 input 비우고 전체 트리 표시
    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearSearchBtn.style.display = 'none';
        searchMenu('');
        searchInput.focus();
    });
    // 엔터키 입력 시 검색
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const searchTerm = searchInput.value.trim().toLowerCase();
            searchMenu(searchTerm);
        }
    });
    // 돋보기 버튼 클릭 시 검색
    searchBtn.addEventListener('click', () => {
        const searchTerm = searchInput.value.trim().toLowerCase();
        searchMenu(searchTerm);
    });

    // 홈(로고/타이틀) 클릭 시 00_main.md 로드
    document.getElementById('homeLink').addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelectorAll('.menu-item').forEach(item => item.classList.remove('active'));
        loadContent('00_main.md');
        // 해시까지 완전히 제거
        location.hash = '';
        window.history.pushState(null, '', '/src/');
    });
    // 첫 진입 시 00_main.md 자동 로드
    loadContent('00_main.md');

    const printBtn = document.getElementById('printBtn');
    printBtn.addEventListener('click', () => {
        window.print();
    });

    // 리사이저(좌우 드래그) 기능
    const resizer = document.getElementById('resizer');
    const leftMenu = document.querySelector('.left-menu');
    let isResizing = false;
    let startX = 0;
    let startWidth = 0;
    resizer.addEventListener('mousedown', (e) => {
        isResizing = true;
        startX = e.clientX;
        startWidth = leftMenu.offsetWidth;
        resizer.classList.add('active');
        document.body.style.cursor = 'ew-resize';
    });
    document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;
        let newWidth = startWidth + (e.clientX - startX);
        newWidth = Math.max(180, Math.min(600, newWidth));
        leftMenu.style.width = newWidth + 'px';
    });
    document.addEventListener('mouseup', () => {
        if (isResizing) {
            isResizing = false;
            resizer.classList.remove('active');
            document.body.style.cursor = '';
        }
    });

    // 해시 기반 md 파일 로드 함수
    loadMdFromHash();
});

// 해시 변경 시 md 파일 오픈
window.addEventListener('hashchange', () => {
    loadMdFromHash();
});

// 메뉴 트리 렌더링
function renderMenuTree(data, parentElement = document.getElementById('menuTree')) {
    parentElement.innerHTML = '';
    
    data.forEach(item => {
        const menuItem = createMenuItem(item);
        parentElement.appendChild(menuItem);
    });

    // URL 해시가 있으면 해당 메뉴의 경로를 찾아서 펼치기
    const hash = location.hash.slice(1); // '#' 제거
    if (hash) {
        expandMenuPath(hash);
    }
}

// 메뉴 경로 찾아서 펼치기
function expandMenuPath(targetFile) {
    function findAndExpandPath(items, targetFile, path = []) {
        for (const item of items) {
            const currentPath = [...path, item];
            
            if (item.file === targetFile) {
                // 찾은 경로의 모든 부모 메뉴 펼치기
                currentPath.forEach(node => {
                    const menuItem = document.querySelector(`[data-file="${node.file}"]`);
                    if (menuItem) {
                        menuItem.classList.add('expanded');
                        menuItem.classList.add('active');
                    }
                });
                return true;
            }
            
            if (item.children && item.children.length > 0) {
                if (findAndExpandPath(item.children, targetFile, currentPath)) {
                    return true;
                }
            }
        }
        return false;
    }
    
    findAndExpandPath(menuData, targetFile);
}

// 메뉴 아이템 생성
function createMenuItem(item, level = 1) {
    if (level > 4) {
        return null;
    }

    const div = document.createElement('div');
    div.className = `menu-item level-${level}`;
    div.setAttribute('data-file', item.file); // 파일명을 data 속성으로 추가

    // 메뉴 제목 컨테이너
    const titleContainer = document.createElement('div');
    titleContainer.className = 'menu-title-container';
    
    // collapse/expand 항목에만 caret(arrow) SVG 추가, leaf에는 빈 span으로 공간 확보
    let icon;
    if (item.children && item.children.length > 0 && level < 4) {
        icon = document.createElement('span');
        icon.className = 'arrow';
        icon.innerHTML = `<svg width="14" height="14" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;"><path d="M7 5L13 10L7 15" stroke="#1976d2" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
    } else {
        icon = document.createElement('span');
        icon.className = 'arrow-placeholder';
    }
    titleContainer.appendChild(icon);

    // 메뉴 제목
    const title = document.createElement('span');
    title.textContent = item.title;
    title.className = 'menu-title';
    titleContainer.appendChild(title);
    div.appendChild(titleContainer);

    if (item.children && item.children.length > 0 && level < 4) {
        div.classList.add('has-children');
        const children = document.createElement('div');
        children.className = 'children';
        item.children.forEach(child => {
            const childItem = createMenuItem(child, level + 1);
            if (childItem) {
                children.appendChild(childItem);
            }
        });
        div.appendChild(children);
        // 클릭 이벤트 - 접기/펼치기 (화살표 또는 제목 클릭 시)
        titleContainer.addEventListener('click', (e) => {
            e.stopPropagation();
            div.classList.toggle('expanded');
        });
    } else {
        // 4레벨이거나 leaf 노드인 경우 컨텐츠 로드
        div.addEventListener('click', function(e) {
            document.querySelectorAll('.menu-item').forEach(item => {
                item.classList.remove('active');
            });
            div.classList.add('active');
            // 해시 갱신
            const fileBase = item.file.replace(/\.md$/, '');
            location.hash = fileBase;
        });
    }
    return div;
}

// 컨텐츠 로드
async function loadContent(file) {
    try {
        const response = await fetch(`/02_outputs/manual_md/${file}?t=${Date.now()}`);
        let content = await response.text();
        
        // 로고 이미지 처리
        content = content.replace(/!\[\]\(\/03_resources\/solution_link_logo_2505\.png\)/g, 
            '<figure class="logo-figure"><img src="/03_resources/solution_link_logo_2505.png" alt="Solution Link Logo" class="logo-image"></figure>');
        
        // 일반 이미지 마크다운을 figure 태그로 변환
        content = content.replace(/!\[(.*?)\]\((.*?)\)/g, '<figure><img src="$2" alt="$1" class="screenshot"><figcaption>$1</figcaption></figure>');
        
        // 마크다운을 HTML로 변환
        const htmlContent = marked.parse(content);
        // 컨텐츠 영역 업데이트
        document.getElementById('content').innerHTML = htmlContent;
        
        // 모든 이미지에 클릭 이벤트 추가
        document.querySelectorAll('#content img').forEach(img => {
            img.addEventListener('click', function() {
                showScreenshotModal(img.src);
            });
        });
    } catch (error) {
        console.error('컨텐츠 로드 실패:', error);
    }
}

function showScreenshotModal(src) {
    // 오버레이 생성
    const overlay = document.createElement('div');
    overlay.className = 'screenshot-modal-overlay';
    // 이미지 생성
    const img = document.createElement('img');
    img.className = 'screenshot-modal-img';
    img.src = src;
    overlay.appendChild(img);
    // 클릭 시 닫기
    overlay.addEventListener('click', () => {
        overlay.remove();
    });
    document.body.appendChild(overlay);
}

// 메뉴 검색
function searchMenu(searchTerm) {
    if (!searchTerm) {
        renderMenuTree(menuData);
        return;
    }
    function filterTree(node, level = 1) {
        if (level > 4) return null; // 4레벨까지만 탐색
        let matchedChildren = [];
        if (node.children && node.children.length > 0) {
            matchedChildren = node.children
                .map(child => filterTree(child, level + 1))
                .filter(child => child !== null);
        }
        if (node.title.toLowerCase().includes(searchTerm) || matchedChildren.length > 0) {
            return {
                ...node,
                children: matchedChildren
            };
        }
        return null;
    }
    const filtered = menuData
        .map(item => filterTree(item, 1))
        .filter(item => item !== null);
    if (filtered.length === 0) {
        document.getElementById('menuTree').innerHTML = '<div style="padding:24px 0; color:#888; text-align:center;">검색 결과가 없습니다.</div>';
    } else {
        renderMenuTree(filtered);
    }
}

// 해시 기반 md 파일 로드 함수
function loadMdFromHash() {
    const hash = decodeURIComponent(location.hash.replace(/^#/, ''));
    if (hash && /^[\w.\-]+$/.test(hash)) {
        loadContent(hash + '.md');
    } else {
        loadContent('00_main.md');
    }
} 