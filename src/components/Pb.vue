<template>
    <h1>纯几何吧题目检索</h1>
    <br>
    <a-spin size="large" v-if="loading" />
    <a-card title="Search" v-if="!loading" style="width: 100%">
        <a-input v-model:value="value" placeholder="输入标题信息检索" @change="search" />
        <div style="margin-top: 20px;">
            <a-table :columns="columns" :row-key="record => record.key" :data-source="data">
                <template #bodyCell="{ column, record }">
                    <template v-if="column.dataIndex === 'title'">
                        <a :href="record.url" target="_blank">{{ record.title }}</a>
                    </template>
                    <template v-if="column.dataIndex === 'author'">
                        <a href="">{{ record.author }}</a>
                    </template>
                    <template v-if="column.dataIndex === 'tags'">
                        <a-tag v-for="tag in record.tags" :key="tag" :color="tag.length > 5 ? 'geekblue' : 'green'">
                            {{ tag }}
                        </a-tag>
                    </template>
                </template>
            </a-table>
        </div>
    </a-card>
    <a-card title="Contribute" style="width: 100%; margin-top: 30px;">
        <a-typography>
            <h3>贡献标签</h3>
            <a-typography-paragraph>
                该功能目前仍在开发中，预计之后会开发以Issue的形式提交题目标签的功能，敬请期待。
                目前可以手动修改<a href="https://github.com/linsyking/cjhbdb/blob/main/public/pb.json" target="_blank">pb.json</a>文件，然后提交PR。
            </a-typography-paragraph>
            <h3>贡献代码</h3>
            <a-typography-paragraph>
                该项目仍在开发中，大量功能尚未支持。如果你有兴趣参与开发，可以提交PR。
            </a-typography-paragraph>
        </a-typography>
    </a-card>
</template>

<script>
import { defineComponent } from 'vue';
import axios from 'axios';
import { SearchOutlined } from '@ant-design/icons-vue';
const columns = [
    {
        title: 'Title',
        dataIndex: 'title',
        key: 'title',
    },
    {
        title: 'Author',
        dataIndex: 'author',
        key: 'author',
    },
    {
        title: 'Tags',
        dataIndex: 'tags',
        key: 'tags',
    }
];

export default defineComponent({
    components: {
        SearchOutlined
    },
    data() {
        return {
            value: '',
            data: [],
            columns: columns,
            loading: true,
            pbdata: []
        };
    },
    methods: {
        search() {
            const ssid = this.value;
            if (ssid === '') {
                this.data = [];
                return;
            }
            let result = [];
            for (let i = 0; i < this.pbdata.length; i++) {
                if (this.pbdata[i].title.indexOf(ssid) !== -1 || this.pbdata[i].title_pinyin.indexOf(ssid) !== -1 || this.pbdata[i].title_pinyin_first.indexOf(ssid) !== -1) {
                    const obj = this.pbdata[i];
                    result.push({
                        title: obj.title,
                        pid: parseInt(obj.pid),
                        url: "https://tieba.baidu.com/p/" + obj.pid,
                        author: obj.author,
                        tags: obj.tags,
                    });
                }
            }
            // Sort result by pid
            result.sort((a, b) => {
                return b.pid - a.pid;
            });
            this.data = result;
        }
    },
    mounted() {
        axios.get('pb.json').then(res => {
            this.pbdata = res.data;
            this.loading = false;
        }).catch(err => {
            console.log(err);
        })
    }
});
</script>
