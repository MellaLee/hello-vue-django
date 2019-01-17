<template>
  <div class="c-header">
	<div class="header-brand">
	  <a href="/" class="header-brand-link">
	  	<img src="static/image/logo.png">
	  	<h3 class="header-beand-link-title">基于URL识别恶意访问系统</h3>
	  </a>
	</div>
	<div class="header-nav-toggle">
	  	<img src="static/image/toggle.png" @click="toggleNav">
	</div>
	<div class="header-nav-content">
		<el-input v-model="input" placeholder="输入内容可全局搜索" suffix-icon="el-icon-search" size="small"></el-input>
	</div>
  </div>
</template>

<script>
export default {
	name: 'c-header',
	data() {
		return {
			input: ''
		};
	},
	methods: {
		toggleNav() {
			this.$emit('change');
		}
	}
}
</script>

<style lang="less">
.c-header {
	background: #fff;
	display: flex;
	height: 44px;
	width: 100%;
	padding: 8px 0;
	box-shadow: 0 2px 4px 0 rgba(0,0,0,.1);	
	.header-brand {
		margin-left: 1rem;
		display: flex;
		.header-brand-link {
			display: flex;
			text-decoration: none;
			img {
				margin-top: 9px;
				height: 32px;
			}
			.header-beand-link-title {
				color: #409eff;
				line-height: 12px;
			}
		}
	}
	.header-nav-toggle {
		margin-left: 1rem;
		margin-top: 15px;
		img {
			height: 14px;
			cursor: pointer;
		}
	}
	.header-nav-content {
		margin-left: 1380px;
		margin-top: 9px;
		.el-input {
			margin-right: 5px;
		}
	}
}
</style>