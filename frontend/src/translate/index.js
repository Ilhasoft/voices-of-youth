import Vue from 'vue';
import VueI18n from 'vue-i18n';
import helper from '@/helper';
import messages from './languages';

Vue.use(VueI18n);

const language = helper.getItem('language');
const defaults = ['en'];

export default new VueI18n({
  locale: defaults.indexOf(language) === 1 ? language : 'en',
  messages,
});
