<template>
  <div>
    <header-index/>
    <div class="page-container">

      <pagination
        :pagination="pagination"
        :currentPage="currentPage"
        :nextPage="nextPage"
        :previousPage="previousPage"
        @goPreviousPage="goPreviousPage"
        @goNextPage="goNextPage"
        @loadItens="moreImages"
      />

      <div class="columns" :key="key" v-for="(value, key) in imagesList">
        <div class="column" :key="key" v-for="(image, key) in imagesList[key]">
          <div class="card">
            <div class="card-image">
              <figure class="image">
                <img :src="image.file" alt="" @click.prevent="openReport(image.report_id)">
              </figure>
            </div>
            
            <div class="card-content">
              <div class="media">
                <div class="media-content">
                  <p class="title">{{ image.report }}</p>
                </div>
            </div>

            <div class="content">
              <img :src="image.created_by.avatar" class="avatar" alt="">
              <small>{{ image.created_by.first_name }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <pagination
      :pagination="pagination"
      :currentPage="currentPage"
      :nextPage="nextPage"
      :previousPage="previousPage"
      @goPreviousPage="goPreviousPage"
      @goNextPage="goNextPage"
      @loadItens="moreImages"
    />
  </div>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import router from '@/router/';
import HeaderIndex from '@/components/header/Index';
import Pagination from '@/components/shared/Pagination';

export default {
  name: 'Gallery',

  components: { HeaderIndex, Pagination },

  beforeCreate: () => {
    document.body.className = 'grey';
  },

  beforeDestroy: () => {
    document.body.className = 'white';
  },

  mounted() {
    this.getGalleryImages();
  },

  computed: {
    ...mapGetters({
      imagesList: 'galleryImages',
      pagination: 'galleryPagination',
      currentPage: 'galleyCurrentPage',
      nextPage: 'galleryNextUrl',
      previousPage: 'galleryPreviousUrl',
      currentProject: 'getCurrentProject',
    }),
  },

  methods: {
    ...mapActions([
      'getGalleryImages',
      'setSideBarConfigs',
      'getReport',
    ]),

    moreImages(nextPage) {
      this.getGalleryImages({ page: nextPage });
    },

    goPreviousPage() {
      if (this.previousPage) {
        this.getGalleryImages({ page: this.currentPage - 1 });
      }
    },

    goNextPage() {
      if (this.nextPage) {
        this.getGalleryImages({ page: this.currentPage + 1 });
      }
    },

    openReport(id) {
      router.push({ name: 'project', params: { path: this.currentProject.path } });
      this.setSideBarConfigs({
        tabActived: 'ReportDetail',
        isActived: true,
      }).then(() => {
        this.getReport(id);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.page-container {
  margin: auto;
  padding: 20px 67px;

  .card {
    border-radius: 10px;
    box-shadow: none;

    figure {
      display: table;
      margin: auto;
    }
  }

  .image img {
    max-width: 100%;
    cursor: pointer;
  }

  .title {
    font-size: 18px;
    font-weight: 500;
    letter-spacing: -0.5px;
    text-align: left;
    color: #000000;
    margin-bottom: 1px;
  }

  .subtitle {
    margin: 10px 0px 5px;
    font-size: 14px;
    letter-spacing: -0.3px;
    text-align: left;
    color: #000000;
  }

  .avatar {
    width: 25px;
    height: 25px;
    float: left;
    margin-right: 5px;
  }

  .image {
    padding: 12px;
  }

  small {
    font-size: 14px;
    letter-spacing: -0.4px;
    text-align: left;
    color: #000000;
  }
}
</style>
