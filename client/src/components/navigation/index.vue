/**
* Created by vouill on 11/13/17.
*/

<template>

<div>
  <b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-brand href="#">HOME</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right>
          <template slot="button-content"><em>Menu</em></template>
          <b-dropdown-item v-if="isProfileLoaded" href="/account">User</b-dropdown-item>
          <b-dropdown-item v-if="isAuthenticated" href="/Tasks">Tasks</b-dropdown-item>
          <b-dropdown-item v-if="isAuthenticated" href="#" @click="logout">Logout</b-dropdown-item>
          <b-dropdown-item v-if="!isAuthenticated && !authLoading" href="/login">Login</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
</template>

<style lang="scss" scoped>
  a {
    color: white;
    text-decoration: none;
  }
  .navigation {
    display: flex;
    color: white;
    align-items: center;
    background-color: #ffa035;
    padding: 5px;

    ul{
      display: flex;
      &:first-child{
        flex-grow: 1;
      }
      li {
        padding-right: 1em;
      }
    }
  }
  .brand {
    display: flex;
    align-items: center;

  }
  .logout {
    &:hover {
      cursor: pointer;
    }
  }

</style>

<script>
  import { mapGetters, mapState } from 'vuex'
  import { AUTH_LOGOUT } from 'actions/auth'

  export default {
    name: 'navigation',
    methods: {
      logout: function () {
        this.$store.dispatch(AUTH_LOGOUT).then(() => this.$router.push('/login'))
      }
    },
    computed: {
      ...mapGetters(['getProfile', 'isAuthenticated', 'isProfileLoaded']),
      ...mapState({
        authLoading: state => state.auth.status === 'loading',
        name: state => `${state.user.profile.title} ${state.user.profile.name}`,
      })
    },
  }
</script>
