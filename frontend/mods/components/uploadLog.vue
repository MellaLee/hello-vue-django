<template>
	<div class="c-upload-log">
		<el-upload
			drag
			multiple
			accept=".csv"
			:action="uploadUrl"
			:headers="{'X-CSRFToken': csrfToken}">
			<i class="el-icon-upload"></i>
			<div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
			<div class="el-upload__tip" slot="tip">
				* 目的: 以用户为单位，将其该段时间内的访问数据集存入MySQL表sys_urllog
				<br/>
				* 仅支持上传CSV文件
			</div>
		</el-upload>
	</div>
</template>

<script>
import $cookie from '../util/cookie.js';
export default {
	name: 'upload-log',
	data() {
		return {
			csrfToken: '', 
			uploadUrl: '/api/upload/url_log'
		}
	},
	created() {
		this.csrfToken = $cookie.get('csrftoken');
	}
}
</script>
