<template>
	<div class="c-upload-log">
		<el-row :gutter="10">
			<el-col :span="12">
				<i class="iconfont icon-tiao"></i>上传数据
			</el-col>
			<el-col :span="12" class="upload">
				<i class="iconfont icon-tiao"></i>已成功上传的列表
			</el-col>
		</el-row>
		<el-row class="upload-content" :gutter="10">
			<el-col :span="12" class="upload left-side">
				<el-steps class="upload-step" direction="vertical" :active="activeItem">
					<el-step title="步骤1：上传RSA公钥"
						description="用于加密用户标识"
						icon="iconfont icon-daochugongyue"
					></el-step>
					<el-step title="步骤2：上传日志文件"
						description="用于训练检测模型"
						icon="el-icon-document"
					></el-step>
				</el-steps>
				<el-upload
					drag
					multiple
					accept=".csv, .xlxs, .txt"
					:action="uploadUrl"
					:headers="{'X-CSRFToken': csrfToken}">
					<i class="el-icon-upload"></i>
					<div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
					<div class="el-upload__tip" slot="tip"> {{ uploadTip[activeItem] }} <br/>* 填充方式为PKCS1_PADDING, 字符集为gb2312编码（简体）</div>
				</el-upload>
			</el-col>
			<el-col :span="12">
				<el-table class="uploaded-table" :data="tableData">
					<el-table-column type="index"></el-table-column>
					<el-table-column prop="file" label="文件名"> </el-table-column>
					<el-table-column prop="user" label="加密后的用户标识"> </el-table-column>
					<el-table-column label="操作" align="right">
						<template slot-scope="scope">
							<el-button type="danger" size="small">删除</el-button>
						</template>
					</el-table-column>
				</el-table>
				<el-pagination class="page"
					background
					layout="prev, pager, next"
					:total="3480">
				</el-pagination>
			</el-col>
		</el-row>
	</div>
</template>

<script>
import $cookie from '../util/cookie.js';
export default {
	name: 'upload-log',
	data() {
		return {
			csrfToken: '', 
			uploadUrl: '/api/upload/url_log',
			uploadTip: {
				1: '* 仅支持PKCS#1格式的.key文件;',
				2: '* 仅支持上传txt,xlsx,csv格式文件'
			},
			tableData: [{
				file: 'urllog-1',
				user: 'xxxxx'
			}]
		}
	},
	computed: {
		activeItem() {
			return this.$store.state.step.curStep;
		}
	},
	created() {
		this.$store.dispatch('setStepNum', 2);
		this.csrfToken = $cookie.get('csrftoken');
	}
}
</script>

<style lang="less">
.c-upload-log {
	.left-side {
		border-right: 0.5px #c0c4cc dashed;
		font-weight: 800;
    	font-size: 14px;
	}
	.upload-content {
		display: flex;
		margin-top: 10px;
		.upload {
			display: flex;
			align-items: center;
			.upload-step {
				height: 500px;
			}
		}
		.iconfont {
			font-size: 25px;
		}
		.page {
			position: fixed;
			bottom: 200px;
			right: 40px
		}
	}
}
</style>

