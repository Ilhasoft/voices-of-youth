<template>
  <li>
    <div class="div">
      <div class="item">
        <img :src="file.blob" v-if="file.blob">
        <img :src="file.thumbnail" v-if="file.thumbnail">
      </div>
      <div tabindex="-1" class="media-item-remove close">
        <i class="media-item-button" @click.prevent="$emit('remove-file')">
          <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 25 25">
            <g fill="none" fill-rule="evenodd" transform="translate(-.51 -.758)">
              <circle cx="13" cy="12.849" r="12.067" fill="#070707"/>
              <g stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="3">
                <path d="M17.83 8.34l-9.34 9.34M8.49 8.34l9.34 9.34"/>
              </g>
            </g>
          </svg>
        </i>
      </div>
    </div>
  </li>
</template>

<script>
export default {
  name: 'File',

  props: {
    file: {
      type: Object,
      required: true,
    },
  },

  methods: {
    removeFile() {
      this.$emit('removeFile', this.file);
    },
  },
};
</script>

<style lang="scss" scoped>
.images li .div {
  display: block;
}

.images div .item {
  border-radius: 10px;
  height: 86px;
  width: 86px;
  overflow: hidden;
  position: relative;
}

.images div .item img {
  bottom: 0;
  left: 0;
  margin: auto;
  width: 86px;
  height: 86px;
  position: absolute;
  right: 0;
  top: 0;
}

.media-item-remove {
  outline: none;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  cursor: pointer;
  height: 18px;
  position: absolute;
  right: -5px;
  top: -5px;
  width: 18px;
  display: -webkit-flex;
  display: flex;
  align-items: center;
  -webkit-align-items: center;
  -webkit-justify-content: center;
  justify-content: center;
}

.media-item-button {
  font-size: 16px;
}

.media-item-button:hover {
  color: #333;
  font-weight: bold;
}
</style>
