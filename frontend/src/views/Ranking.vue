<template>
    <div class="big-container">
        <div class="page-title">Oshido Ranking</div>
        <div class="celeb-name">{{ name }}</div>
        <div class="ranking-container">
            <div class="ranking-content">
                <div class="ranking-content-line">
                    <div class="ranking-number">1.</div>
                    <div class="ranking-user-name">たけし</div>
                    <div class="ranking-oshido-box">
                        <div class="ranking-oshido-circle"></div>
                        <div class="ranking-oshido">55</div>
                    </div>
                </div>
            </div>
        </div>
        <footer>
            <div class="foot-box">
                <router-link to="/iconlist">[icons]</router-link>
                <div>Designed by Freepik and distributed by Flaticon</div>
            </div>
            <div class="foot-nav">
                <img @click="pageTransition()" src="@/assets/ranking-active.png" class="ranking-icon">
                <img v-if="oshido>=100" src="@/assets/gold-medal.png" class="medal gold-medal medal-1">
                <img v-else src="@/assets/no-medal.png" class="medal no-medal medal-1">
                <img v-if="oshido>=50" src="@/assets/silver-medal.png" class="medal silver-medal medal-2">
                <img v-else src="@/assets/no-medal.png" class="medal no-medal medal-2">
                <img v-if="oshido>=20" src="@/assets/bronze-medal.png" class="medal bronze-medal medal-3">
                <img v-else src="@/assets/no-medal.png" class="medal no-medal medal-3">
                <img src="@/assets/home.png" class="home-icon">
                <img src="@/assets/user.png" class="user-icon">
                <img v-if="sideMenuActive!=true" @click="toggleList" src="@/assets/list.png" class="list-icon">
                <img v-else @click="toggleList" src="@/assets/list-open.png" class="list-icon">
                <img src="@/assets/footer.png" class="footer-img">
                <div v-if="isOshi" class="oshido">{{ watchedContentCount }}</div>
            </div>
        </footer>
    </div>
</template>

<script>
export default {
    el: '#app',
    data() {
        return {
            name: this.$route.params.celebName
        };
    },
    methods: {
        pageTransition: function() {
            this.$router.push({
                name: 'Celebs',
                params: {
                    celebName: this.name
                }
            })
        }
    }
}
</script>

<style>
.page-title {
    position: relative;
    width: 319px;
    height: 53px;
    left: 30px;
    top: 28px;

    text-align: center;
    font-style: normal;
    font-weight: bold;
    font-size: 32px;
    line-height: 53px;
    text-decoration-line: underline;
    color: #FFFFFF;
}

.celeb-name {
    position: relative;
    width: 120px;
    height: 35px;
    text-align: center;
    margin: 35px auto;
    font-style: normal;
    font-weight: bold;
    font-size: 20px;
    line-height: 35px;
    color: #FFFFFF;
}

.ranking-content {
    width: 341px;
    height: 80px;
    margin: 0 auto 25px auto;
    background: #FFFFFF;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    border-radius: 5px;

    transition: 0.5s;
    position: relative;
    z-index: 2;
}

.ranking-content-line {
    position: absolute;
    width: 330px;
    height: 71px;
    left: 2px;
    top: 1px;
    z-index: 3;
    border-radius: 5px;
    border: 3px solid #F4D153;
}

.ranking-number {
    position: absolute;
    left: 15px;
    top: 23px;
    font-size: 24px;
    font-weight: bold;
}

.ranking-user-name {
    position: absolute;
    left: 52px;
    top: 22px;
    font-size: 20px;
}

.ranking-oshido-box {
    position: absolute;
    width: 58px;
    height: 58px;
    left: 250px;
    top: 7px;
    background-color: #F4D153;
    border-radius: 100%;
    z-index: 1;
}

.ranking-oshido-circle {
    position: absolute;
    width: 45px;
    height: 45px;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    margin: auto;
    border: 3px solid #FFFFFF;
    border-radius: 100%;
    padding-right: 1px;
    padding-bottom: 1px;
    z-index: 2;
}

.ranking-oshido {
    position: absolute;
    width: 50px;
    height: 20px;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    margin: auto;
    text-align: center;
    line-height: 1;
    font-size: 20px;
    font-weight: bold;
    color: #FFFFFF;
}
</style>