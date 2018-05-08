<template>
    <div id="app">
        <el-row>
            <el-col :span="18" :offset="3">
                <el-container style="border: 1px solid #eee">
                    <el-header>
                        <h3 style="text-align: center">URL恶意访问识别系统</h3>
                    </el-header>

                    <el-main>
                        <el-steps :active="active" finish-status="success" align-center>
                            <el-step v-for="(obj, index) in stepName" :key="index" :title="obj.title" :description="obj.description"></el-step>
                        </el-steps>

                        <el-card style="margin-top:12px">
                            <el-container style="height:400px">
                                <el-main>
                                    <div v-if="!active">
                                        输出以用户为单位，七天内对某域名访问的数据集
                                    </div>
                                    <el-upload v-else-if="active == 1" drag :action="uploadUrl" multiple :headers="{'X-CSRFToken': csrfToken}">
                                        <i class="el-icon-upload"></i>
                                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                                        <div class="el-upload__tip" slot="tip">只能上传excel文件</div>
                                    </el-upload>
                                </el-main>
                                <el-footer>
                                    <el-button-group style="float:right">
                                        <el-button :disabled="!active" icon="el-icon-arrow-left" style="margin: 12px 1px" type="primary" @click="back">上一步</el-button>
                                        <el-button :disabled="active == 3" style="margin: 12px 1px" type="primary" @click="nextStep">
                                            下一步<i class="el-icon-arrow-right el-icon--right"></i>
                                        </el-button>
                                    </el-button-group>
                                </el-footer>
                                </el-container>
                        </el-card>
                    </el-main>
                </el-container>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
    name: 'app',
    data () {
        return {
            active: 0,
            stepName: [
                { title: '数据获取', description: '获取与清洗日志' }, 
                { title: '特征提取', description: '上传URL日志, 量化提取特征'}, 
                { title: '聚类标记', description: '聚类标记'},
                { title: '半监督学习', description: '上传未标记训练集合并进行预测'}],
            uploadUrl: '/api/upload/url_log',
            csrfToken: '', 
        }
    },

    created() {
        this.csrfToken = this.getCookie('csrftoken');
    },

    methods: {
        back(index) {
            if (this.active-- < 0) this.active = 0;
        },
        nextStep(index) {
            if (this.active++ > 2) this.active = 0;
        },
        getCookie(name) {
            let arr,
                reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)")
            if (arr = document.cookie.match(reg)) {
                return decodeURIComponent(arr[2])
            }
        },
    },
}
</script>

<style>
</style>
