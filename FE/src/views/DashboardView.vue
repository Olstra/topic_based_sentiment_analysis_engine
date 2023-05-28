<template>
    <NavBar/>
    <div>
     <h1>Dashboard</h1>
      <div>
    <label for="my-input"> Nach Patienten suchen: </label>
    <input id="my-input" type="text" v-model="myText">
      </div>
    </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import NavBar from "@/components/Navbar.vue";

export default defineComponent({
    name: 'DashboardView',
    components: {NavBar},
    data() {
        return {
            myText: "",
        }
    },
    methods: {}
})
</script>

<style scoped>
div {
    padding-left: 2%;
    padding-right: 2%;
}
</style>