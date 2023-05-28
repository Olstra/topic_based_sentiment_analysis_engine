<template>
    <nav>
        <ul>
            <li>
                <router-link class="my-link" to="/">Home</router-link>
            </li>
            <li>
                <router-link class="my-link" to="/Patient-A">Patient 1</router-link>
            </li>
            <li>
                <router-link class="my-link" to="/Patient-B">Patient 2</router-link>
            </li>
            <li>
                <router-link class="my-link" to="/">About</router-link>
            </li>
        </ul>
    </nav>
</template>

<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
    name: 'NavBar',
})
</script>

<style scoped>
nav {
    width: 100%;
    height: 60px;
    background-color: #333;
    /* Make navbar stick to top */
    position: sticky;
    top: 0;
    /* */
    /* set z-index else Google Chart is on top of navbar when scrolling */
    z-index: 999;
}

.my-link {
    color: white;
    background-color: #333;
    padding: 10px;
    text-decoration: none;
    border-radius: 5px;
    font-size: 20px;
}

ul {
    list-style-type: none;
    margin: 0;
    padding: 0.5rem;
    overflow: hidden;
}

li {
    float: left;
}

li a {
    display: block;
    color: white;
    text-align: center;
    text-decoration: none;
}

li a:hover {
    background-color: grey;
}
</style>