<template>
	<div class="c-url-list">
		<i class="iconfont icon-tiao"></i>提取特征
		<el-form class="feature-form" :inline="true" :model="form">
			<el-form-item label="访问正常时间">
				<el-time-picker is-range v-model="form.time"
					range-separator="至"
					start-placeholder="开始时间"
					end-placeholder="结束时间"
					placeholder="选择时间范围">
				</el-time-picker>
			</el-form-item>
			<el-form-item label="时间窗口">
				<el-select v-model="form.window" placeholder="时间窗口">
				<el-option label="5分钟" value="5"></el-option>
				<el-option label="10分钟" value="10"></el-option>
				<el-option label="15分钟" value="15"></el-option>
				<el-option label="20分钟" value="20"></el-option>
				<el-option label="25分钟" value="25"></el-option>
				<el-option label="30分钟" value="30"></el-option>
				</el-select>
			</el-form-item>
			 <el-form-item label="设备类型参数">
				<el-input type="textarea" v-model="form.deviceList" placeholder="参数之间请以半角逗号分隔,形如deviceType,dname,_device"></el-input>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="onSubmit">开始量化特征</el-button>
			</el-form-item>
		</el-form>
		
		<i class="iconfont icon-tiao"></i>特征量化结果
		<el-table :data="tableData">
			<el-table-column prop="user" label="用户"></el-table-column>
			<el-table-column sortable prop="url" label="访问域名"></el-table-column>
			<el-table-column sortable prop="similarEuc" label="特征D"></el-table-column>
			<el-table-column sortable prop="urlArgsEntropy" label="特征H"></el-table-column>
			<el-table-column sortable prop="abnormalTimeProbability" label="特征Ptime"></el-table-column>
			<el-table-column sortable prop="sameArgsDiversity" label="特征Puri"></el-table-column>
			<el-table-column sortable prop="webClassify" label="特征Cweb"></el-table-column>
		</el-table>
		<el-pagination
		  style="float:right"
		  @size-change="handleSizeChange"
		  @current-change="handlePageChange"
		  :current-page.sync="page"
		  :page-sizes="[10, 20, 50, 100]"
		  :page-size="size"
		  layout="sizes, prev, pager, next"
		  :total="logTotal"
		></el-pagination>
	</div>
</template>

<script>
import $api from '../io/app.js';
export default {
	name: 'url-list',
	data() {
		return {
			tableData:[],
			page: 1,
			size: 10,
			logTotal: 0,
			form: {
				time: '',
				window: '',
				deviceList: ''
			}	
		}
	},
	created() {
		this.$store.dispatch('setStepNum', 0);
		this.fetchTable();
	},
	methods: {
		fetchTable() {
			let params = {
				page: this.page,
				size: this.size
			};
			$api.fetchUrlList(params).then(res => {
				this.tableData = res.list;
				this.logTotal = res.total;
			});
		},
		handleSizeChange(val) {
			this.size = val;
			this.page = 1;
			this.fetchTable();
		},
		handlePageChange() {
			this.fetchTable();
		},
		onSubmit() {
			//TODO
		}
	}
}
</script>

<style lang="less">
.c-url-list {
	.feature-form {
		margin-left: 13px;
		margin-top: 5px;
		.el-textarea {
			width: 500px;
			.el-textarea__inner {
				height: 40px;
			}
		}
	}
}
</style>
