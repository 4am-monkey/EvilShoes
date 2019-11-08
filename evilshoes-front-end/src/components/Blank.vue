<template>
    <div class='x-blank'></div>
</template>

<script>
export default {
    name: 'x-blank',
    mounted(){
        window.console.log('=============')
        this.$router.push({path: '/'});
    }
}
</script>

<style>

</style>