<template>
  <div class="center-container">
        <div class="center-card">
            <h1>个人中心</h1>

            <div class="center-content">
                <aside class="sidebar">
                    <ul class="menu">
                        <li :class="{active: selected === 'info'}" @click="selected = 'info'">个人信息</li>
                        <li :class="{active: selected === 'posts'}" @click="selected = 'posts'">我发表的博客</li>
                        <li :class="{active: selected === 'favorites'}" @click="selected = 'favorites'">我收藏的博客</li>
                    </ul>
                </aside>

                <main class="main-panel">
                    <section v-if="selected === 'info'" class="panel-section">
                        <div class="info-row"><strong>昵称：</strong><span>{{ userInfo.nickname }}</span></div>
                        <div class="info-row"><strong>账号：</strong><span>{{ userInfo.account }}</span></div>
                        <div class="info-row"><strong>性别：</strong><span>{{ userInfo.gender }}</span></div>
                        <div class="info-row"><strong>注册日期：</strong><span>{{ userInfo.registrationDate }}</span></div>
                    </section>

                    <section v-if="selected === 'posts'" class="panel-section">
                        <ul class="list">
                            <li v-for="post in postsPaged" :key="post.id">
                                <h3>{{ post.title }}</h3>
                                <p class="meta">{{ post.date }} · {{ post.views }} 阅读</p>
                            </li>
                        </ul>

                        <div class="pagination" v-if="postsTotalPages > 1">
                            <button class="page-btn" :disabled="postsPageIndex === 1" @click="changePostsPage(postsPageIndex-1)">上一页</button>
                            <button v-for="p in postsTotalPages" :key="p" class="page-btn" :class="{active: postsPageIndex===p}" @click="changePostsPage(p)">{{ p }}</button>
                            <button class="page-btn" :disabled="postsPageIndex === postsTotalPages" @click="changePostsPage(postsPageIndex+1)">下一页</button>
                        </div>
                    </section>

                    <section v-if="selected === 'favorites'" class="panel-section">
                        <ul class="list">
                            <li v-for="fav in favoritesPaged" :key="fav.id">
                                <h3>{{ fav.title }}</h3>
                                <p class="meta">收藏于 {{ fav.date }}</p>
                            </li>
                        </ul>

                        <div class="pagination" v-if="favoritesTotalPages > 1">
                            <button class="page-btn" :disabled="favoritesPageIndex === 1" @click="changeFavoritesPage(favoritesPageIndex-1)">上一页</button>
                            <button v-for="p in favoritesTotalPages" :key="p" class="page-btn" :class="{active: favoritesPageIndex===p}" @click="changeFavoritesPage(p)">{{ p }}</button>
                            <button class="page-btn" :disabled="favoritesPageIndex === favoritesTotalPages" @click="changeFavoritesPage(favoritesPageIndex+1)">下一页</button>
                        </div>
                    </section>
                </main>
            </div>
        </div>
  </div>
</template>

<script>
export default {
    name: 'Center',
    data() {
        return {
            selected: 'info',
            userInfo: {
                nickname: '用户昵称',
                account: 'user@example.com',
                gender: '男',
                registrationDate: '2024-01-15'
            },
            posts: [
                { id: 1, title: '我的第一篇博客', date: '2024-02-01', views: 120 },
                { id: 2, title: '如何写好一篇技术文章', date: '2024-03-12', views: 85 },
                { id: 3, title: 'Vue 实战总结', date: '2024-05-05', views: 230 }
            ],
            favorites: [
                { id: 1, title: '优秀的前端工程实践', date: '2024-06-10' },
                { id: 2, title: '性能优化技巧汇总', date: '2024-07-02' }
            ]
        }
    }
}
</script>


<style scoped>
.center-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    background: transparent;
}

.center-card {
    background: #f6f1e8;
    border-radius: 0;
    box-shadow: none;
    width: 100vw;
    height: 100vh;
    padding: 20px 40px;
    box-sizing: border-box;
    margin: 0;
    overflow: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
}

.center-card h1 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
}

.center-content {
    display: flex;
    width: 100%;
    max-width: 1200px;
    margin-top: 10px;
    gap: 24px;
}

.sidebar {
    width: 240px;
}

.menu {
    list-style: none;
    padding: 0;
    margin: 0;
    background: rgba(255,255,255,0.06);
    border-radius: 8px;
    overflow: hidden;
}

.menu li {
    padding: 14px 18px;
    cursor: pointer;
    color: #444;
    border-bottom: 1px solid rgba(0,0,0,0.04);
}

.menu li.active {
    background: #667eea;
    color: #fff;
}

.main-panel {
    flex: 1;
    background: rgba(255,255,255,0.5);
    padding: 20px;
    border-radius: 8px;
    min-height: 300px;
    box-sizing: border-box;
}

.panel-section .info-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid rgba(0,0,0,0.04);
}

.list { padding: 0; margin: 0; list-style: none; }
.list li { padding: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.04); }
.list h3 { margin: 0 0 6px 0; font-size: 18px; }
.meta { color: #666; font-size: 13px; }

.info-section {
    margin-bottom: 30px;
}

.info-item {
    display: flex;
    justify-content: space-between;
    padding: 15px 0;
    border-bottom: 1px solid #f0f0f0;
}

.info-item label {
    font-weight: bold;
    color: #666;
    min-width: 80px;
}

.info-item span {
    color: #333;
    flex: 1;
    text-align: right;
}

.action-buttons {
    display: flex;
    gap: 10px;
    justify-content: center;
}

.btn {
    padding: 10px 30px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s;
}

.btn-primary {
    background: #667eea;
    color: white;
}

.btn-primary:hover {
    background: #5568d3;
}

.btn-secondary {
    background: #f0f0f0;
    color: #333;
}

.btn-secondary:hover {
    background: #e0e0e0;
}
</style>