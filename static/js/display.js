// 主界面定时刷新逻辑
let refreshInterval = null;

function startAutoRefresh() {
    // 每10秒刷新一次页面
    refreshInterval = setInterval(() => {
        window.location.reload();  // 刷新页面
    }, 10000);  // 10000毫秒 = 10秒
}

function stopAutoRefresh() {
    // 停止刷新
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
}

// 页面加载时开始自动刷新
window.onload = startAutoRefresh;

// 加载项目详情到模态框
function loadItemDetails(itemName) {
    const modal = document.getElementById('item-details-modal');
    modal.style.display = 'block'; // 确保弹窗可见
    modal.classList.add('show'); // 添加 show 类以触发动画

    // 暂停主界面的自动刷新
    stopAutoRefresh();

    // 使用 AJAX 请求项目详情
    fetch(`/display/${encodeURIComponent(itemName)}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('modal-content').innerHTML = html; // 插入 HTML 内容

            // 初始化自动滚动
            const scoreContainer = document.querySelector('.score-container');
            if (scoreContainer) {
                console.log("开始自动滚动...");
                startAutoScroll(scoreContainer);
            }
        })
        .catch(error => {
            console.error('加载项目详情失败:', error);
            document.getElementById('modal-content').innerHTML = '<p>加载项目详情失败，请稍后再试。</p>';
        });
}

// 关闭模态框
function closeModal() {
    const modal = document.getElementById('item-details-modal');
    modal.classList.add('hide'); // 添加 hide 类以触发动画

    // 动画结束后清理类并隐藏弹窗
    modal.addEventListener('animationend', () => {
        modal.classList.remove('show', 'hide'); // 移除所有相关类
        modal.style.display = 'none'; // 隐藏弹窗

        // 停止自动滚动
        const scoreContainer = document.querySelector('.score-container');
        if (scoreContainer) {
            console.log("停止自动滚动...");
            stopAutoScroll(scoreContainer);
        }

        // 恢复主界面的自动刷新
        startAutoRefresh();

        // 弹窗关闭时手动刷新一次页面
        window.location.reload();
    }, { once: true });
}

// 自动滚动逻辑
function startAutoScroll(container) {
    // 滚动速度动态计算：10秒内完成滚动到底部
    const scrollDuration = 10000; // 10秒
    let scrollInterval;

    // 滚动函数
    function scrollContent() {
        const maxHeight = container.scrollHeight - container.clientHeight;
        const currentScroll = container.scrollTop;

        // 检查是否需要滚动
        if (maxHeight <= 0) {
            console.log("内容高度不足以滚动，停止滚动...");
            stopAutoScroll(container);
            return;
        }

        // 动态计算每帧滚动距离
        const scrollStep = maxHeight / (scrollDuration / 10); // 每10ms滚动的距离

        // 滚动到底部后返回顶部
        if (currentScroll >= maxHeight) {
            console.log("滚动到底部，返回顶部...");
            container.scrollTop = 0;
        } else {
            // 确保 scrollTop 的值正确更新
            container.scrollTop += scrollStep;
            if (container.scrollTop === currentScroll) {
                console.log("滚动未生效，强制设置 scrollTop...");
                container.scrollTop = currentScroll + 1; // 强制滚动
            }
        }
    }

    // 确保不会重复创建定时器
    if (container.scrollInterval) {
        clearInterval(container.scrollInterval);
    }

    // 开始滚动
    scrollInterval = setInterval(scrollContent, 10); // 每10ms滚动一次
    container.scrollInterval = scrollInterval; // 将定时器绑定到容器对象上

    // 鼠标悬停时暂停滚动
    container.addEventListener('mouseenter', () => {
        console.log("鼠标悬停，暂停滚动...");
        clearInterval(scrollInterval);
    });

    // 鼠标移出时恢复滚动
    container.addEventListener('mouseleave', () => {
        console.log("鼠标移出，恢复滚动...");
        scrollInterval = setInterval(scrollContent, 10);
        container.scrollInterval = scrollInterval; // 重新绑定定时器
    });
}

// 停止自动滚动
function stopAutoScroll(container) {
    if (container.scrollInterval) {
        clearInterval(container.scrollInterval);
        container.scrollInterval = null; // 确保定时器引用被清除
    }
    console.log("自动滚动已停止");
}