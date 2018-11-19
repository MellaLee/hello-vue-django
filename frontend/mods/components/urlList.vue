<template>
	<div class="c-url-list">
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
			logTotal: 0	
		}
	},
	created() {
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
		}
	}
}
</script>
