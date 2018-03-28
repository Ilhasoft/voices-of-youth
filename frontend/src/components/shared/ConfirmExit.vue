<template>
  <div v-show="isVisible" class="div__confirm">
    <div class="opacity"></div>
    <div class="intro">
      <div class="body">
        <p>{{ $t('message.shared.exit.message') }}</p>
        <div class="buttons">
          <a class="button btn-no" @click.prevent="$emit('cancel')">{{ $t('message.shared.exit.no') }}</a>
          <a class="button btn-yes" @click.prevent="$emit('confirm')">{{ $t('message.shared.exit.yes') }}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmExit',

  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style lang="scss" scoped>
.div__confirm {
  position: absolute;
  top: 40%;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
}

.opacity {
  opacity: 0.33;
  z-index: 100000;
  background-color: #000000;
  width: 100%;
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
}

.intro {
  z-index: 100000;
  position: relative;
  margin: auto;
  width: 420px;

  .header {
    padding: 20px;
    background-color: #fff;
    border-top-left-radius: 30px;
    border-top-right-radius: 30px;
    display: table-cell;
    text-align: center;
    width: inherit;
  }

  .body {
    background-color: #fff;
    border-top-left-radius: 30px;
    border-top-right-radius: 30px;
    border-bottom-left-radius: 30px;
    border-bottom-right-radius: 30px;
    padding: 20px;

    p {
      max-height: 250px;
      font-size: 20px;
      line-height: 1.67;
      letter-spacing: -0.4px;
      text-align: center;
      color: #000000;
    }

    .buttons {
      text-align: center;
      margin-top: 15px;

      .btn-no {
        width: 162px;
        height: 36px;
        border-radius: 100px;
        background: #00cbff;
        font-size: 17px;
        font-weight: 500;
        letter-spacing: -0.4px;
        color: #ffffff;
      }

      .btn-yes {
        width: 162px;
        height: 36px;
        border-radius: 100px;
        background: #00cbff;
        font-size: 17px;
        font-weight: 500;
        letter-spacing: -0.4px;
        color: #ffffff;
      }
    }
  }
}
</style>
