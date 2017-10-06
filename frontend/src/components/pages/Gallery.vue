<template>
  <div>
    <header-index/>
    <div class="internal-page-color">

      <div class="page-container">


<div class="tile is-ancestor">
  <div class="tile is-parent">
    <article class="tile is-child box">
      <p class="title">One</p>
      <p class="subtitle">Subtitle</p>
    </article>
  </div>
  <div class="tile is-parent">
    <article class="tile is-child box">
      <p class="title">Two</p>
      <p class="subtitle">Subtitle</p>
    </article>
  </div>
  <div class="tile is-parent">
    <article class="tile is-child box">
      <p class="title">Three</p>
      <p class="subtitle">Subtitle</p>
    </article>
  </div>
  <div class="tile is-parent">
    <article class="tile is-child box">
      <p class="title">Four</p>
      <p class="subtitle">Subtitle</p>
    </article>
  </div>

  <div class="tile is-parent">
    <article class="tile is-child box">
      <p class="title">Four</p>
      <p class="subtitle">Subtitle</p>
    </article>
  </div>

  <div class="tile is-parent">
    <article class="tile is-child box">
      <p class="title">Four</p>
      <p class="subtitle">Subtitle</p>
    </article>
  </div>
</div>



      </div>
</div>
</div>

    </div>
  </div>
</template>

<script>
import HeaderIndex from '../header/Index';

export default {
  name: 'Gallery',

  components: { HeaderIndex },
};
</script>


<style lang="scss" scoped>
.page-container {
  margin: auto;
  padding: 67px;
}
</style>
