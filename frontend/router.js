import Vue from 'vue';
import VueRouter from 'vue-router';

import $uploadLog from './mods/components/uploadLog.vue';
import $urlList from './mods/components/urlList.vue';
import $label from './mods/components/label.vue';
import $check from './mods/components/check.vue';
import $cluster from './mods/components/cluster.vue';
import $semiSupervised from './mods/components/semiSupervised.vue';

Vue.use(VueRouter);

const routes=[{
	path: '/identify',
	redirect: '/identify/check'
},{
	path: '/train',
	redirect: '/train/upload'
},{
	path: '/',
	redirect: '/train/upload'
},{
	path: '/train/upload',
	component: $uploadLog
}, {
	path: '/train/feature',
	component: $urlList
}, {
	path: '/train/cluster',
	component: $cluster
}, {
	path: '/train/cluster/label',
	component: $label
}, {
	path: '/identify/check/label',
	component: $label
}, {
	path: '/identify/check',
	component: $check
}, {
	path: '/train/semiSupervised',
	component: $semiSupervised
}];

const router = new VueRouter({routes});

export default router;