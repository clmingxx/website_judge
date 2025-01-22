// display.js

// 加载项目详情到模态框
function loadItemDetails(itemName) {
    // 显示模态框
    document.getElementById('item-details-modal').style.display = 'block';

    // 使用 AJAX 请求项目详情
    fetch(`/display/${encodeURIComponent(itemName)}`)
        .then(response => response.text())
        .then(html => {
            // 将返回的 HTML 内容插入到模态框中
            document.getElementById('modal-content').innerHTML = html;
        })
        .catch(error => {
            console.error('加载项目详情失败:', error);
            document.getElementById('modal-content').innerHTML = '<p>加载项目详情失败，请稍后再试。</p>';
        });
}

// 关闭模态框
function closeModal() {
    document.getElementById('item-details-modal').style.display = 'none';
}